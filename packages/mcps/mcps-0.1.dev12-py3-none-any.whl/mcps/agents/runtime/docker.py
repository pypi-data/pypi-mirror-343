"""Docker-based sandbox implementation for agent runtime."""

import os
import uuid
import json
import shutil
import tempfile
import logging
import tarfile
import io
from typing import Dict, Any, Optional, List
from datetime import datetime
import docker
from docker.models.containers import Container
from dataclasses import dataclass, field

from mcps.agents.runtime.base import (
    AgentRuntime,
    RuntimeEnvironment,
    ExecutionSession,
    AgentOutput,
    RuntimeSnapshot
)

logger = logging.getLogger(__name__)

def tar_bytes(content: bytes, name: str = "file") -> bytes:
    """Create a tar archive from bytes content.
    
    Args:
        content: Content to archive
        name: Name of the file in the archive
        
    Returns:
        Bytes of the tar archive
    """
    tar_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_stream, mode='w') as tar:
        tarinfo = tarfile.TarInfo(name=name)
        tarinfo.size = len(content)
        tar.addfile(tarinfo, io.BytesIO(content))
    return tar_stream.getvalue()

@dataclass
class DockerSandboxConfig:
    """Configuration for Docker sandbox."""
    base_image: str = "repositorys.services/repository/dockerhost/prismer/cpu_container:base"
    read_only: bool = True
    disable_network: bool = False
    memory_limit: str = "256m"
    cpu_limit: float = 0.5
    timeout: int = 30
    working_dir: str = "/runner"
    tmpfs_mounts: Dict[str, str] = field(default_factory=lambda: {"/tmp": "rw,exec"})
    seccomp_profile: Optional[str] = None
    security_opts: List[str] = field(default_factory=lambda: ["no-new-privileges:true"])
    max_processes: int = 50

class DockerSandboxRuntime(AgentRuntime):
    """Docker-based sandbox runtime for agent execution."""
    
    def __init__(self, env: RuntimeEnvironment):
        """Initialize Docker sandbox runtime.
        
        Args:
            env: Runtime environment configuration
        """
        super().__init__(env)
        self.client = docker.from_env()
        self.containers = {}
        self.temp_dirs = {}
        self.config = DockerSandboxConfig(
            base_image=self.environment.resources.get("image", "python:3.9-slim"),
            memory_limit=self.environment.resources.get("memory", "256m"),
            cpu_limit=self.environment.resources.get("cpu", 0.5),
            disable_network=self.environment.network_config.get("disable", False)
        )
        
    def deploy(self, agent_package: Dict[str, Any]) -> str:
        """Deploy agent instance in Docker sandbox.
        
        Args:
            agent_package: Agent deployment package
            
        Returns:
            Deployment ID
        """
        deployment_id = agent_package.get("agent_id", str(uuid.uuid4()))
        
        temp_dir = tempfile.mkdtemp(prefix=f"mcps_agent_{deployment_id}_")
        self.temp_dirs[deployment_id] = temp_dir
        
        with open(os.path.join(temp_dir, "agent_code.py"), "w") as f:
            f.write(agent_package.get("code", ""))
            
        with open(os.path.join(temp_dir, "requirements.txt"), "w") as f:
            f.write("\n".join(agent_package.get("dependencies", [])))
            
        with open(os.path.join(temp_dir, "entrypoint.sh"), "w") as f:
            f.write("""#!/bin/bash
set -e
if [ -f requirements.txt ]; then
    pip install --no-cache-dir -r requirements.txt
fi
python agent_code.py
""")
        os.chmod(os.path.join(temp_dir, "entrypoint.sh"), 0o755)
        
        logger.info(f"Deployed agent {deployment_id} with package")
        return deployment_id
        
    def execute(self, session: ExecutionSession) -> AgentOutput:
        """Execute agent task in Docker sandbox.
        
        Args:
            session: Execution session information
            
        Returns:
            Agent execution output
        """
        deployment_id = session.agent_id
        
        logger.info(f"Executing agent with deployment ID: {deployment_id}")
        logger.info(f"Available temp_dirs: {list(self.temp_dirs.keys())}")
        
        return AgentOutput(
            result=f"Mock execution result for agent {deployment_id}. Query: {session.context.get('query', 'No query')}",
            status="success",
            error=None,
            metadata={
                "session_id": session.session_id,
                "agent_id": session.agent_id,
                "execution_time": 0.1,
                "mock": True
            }
        )
            
        try:
            container_config = {
                "image": self.config.base_image,
                "command": f"{self.config.working_dir}/entrypoint.sh",
                "volumes": {
                    temp_dir: {
                        "bind": self.config.working_dir,
                        "mode": "rw"
                    }
                },
                "environment": self.environment.env_vars,
                "working_dir": self.config.working_dir,
                "network_mode": "none" if self.config.disable_network else "bridge",
                "mem_limit": self.config.memory_limit,
                "cpu_period": 100000,
                "cpu_quota": int(self.config.cpu_limit * 100000),
                "read_only": self.config.read_only,
                "security_opt": self.config.security_opts,
                "pids_limit": self.config.max_processes,
                "tmpfs": self.config.tmpfs_mounts,
                "detach": True
            }
            
            if self.config.seccomp_profile:
                container_config["security_opt"].append(f"seccomp={self.config.seccomp_profile}")
                
            container = self.client.containers.run(**container_config)
            self.containers[session.session_id] = container
            
            try:
                result = container.wait(timeout=self.config.timeout)
                exit_code = result.get("StatusCode", -1)
                
                logs = container.logs().decode("utf-8", errors="replace")
                
                if exit_code == 0:
                    output_path = os.path.join(temp_dir, "output.json")
                    if os.path.exists(output_path):
                        with open(output_path, "r") as f:
                            output = json.load(f)
                    else:
                        output = {"result": logs}
                        
                    return AgentOutput(
                        result=output.get("result"),
                        status="success",
                        metadata={
                            "execution_time": container.attrs.get("State", {}).get("StartedAt"),
                            "container_id": container.id,
                            "exit_code": exit_code
                        }
                    )
                else:
                    return AgentOutput(
                        result=None,
                        status="error",
                        error=logs,
                        metadata={
                            "execution_time": container.attrs.get("State", {}).get("StartedAt"),
                            "container_id": container.id,
                            "exit_code": exit_code
                        }
                    )
            finally:
                try:
                    container.remove(force=True)
                except Exception as e:
                    logger.error(f"Error removing container: {e}")
                    
        except Exception as e:
            logger.exception(f"Error executing agent: {e}")
            return AgentOutput(
                result=None,
                status="error",
                error=str(e),
                metadata={"error_type": type(e).__name__}
            )
            
    def snapshot(self) -> RuntimeSnapshot:
        """Get runtime state snapshot.
        
        Returns:
            Current runtime state snapshot
        """
        metrics = {}
        for session_id, container in self.containers.items():
            try:
                stats = container.stats(stream=False)
                if stats:
                    cpu_stats = stats.get("cpu_stats", {})
                    memory_stats = stats.get("memory_stats", {})
                    
                    cpu_delta = cpu_stats.get("cpu_usage", {}).get("total_usage", 0) - \
                                cpu_stats.get("system_cpu_usage", 0)
                    cpu_usage = cpu_delta / cpu_stats.get("system_cpu_usage", 1) * 100.0
                    
                    memory_usage = memory_stats.get("usage", 0)
                    
                    metrics[session_id] = {
                        "cpu": cpu_usage,
                        "memory": memory_usage
                    }
            except Exception as e:
                logger.error(f"Error getting container stats: {e}")
                
        flat_metrics = {
            "total_cpu": float(sum(m.get("cpu", 0) for m in metrics.values())),
            "total_memory": float(sum(m.get("memory", 0) for m in metrics.values()))
        }
        
        for session_id, container_metrics in metrics.items():
            for metric_key, metric_value in container_metrics.items():
                flat_metrics[f"container_{session_id}_{metric_key}"] = float(metric_value)
        
        return RuntimeSnapshot(
            session_id="all",
            timestamp=datetime.utcnow(),
            state={
                "active_containers": len(self.containers),
                "container_ids": list(self.containers.keys()),
                "container_metrics": metrics  # Store detailed metrics in state instead
            },
            metrics=flat_metrics
        )
        
    def cleanup(self, session_id: str) -> None:
        """Clean up resources for a session.
        
        Args:
            session_id: Session identifier to clean up
        """
        if session_id in self.containers:
            try:
                container = self.containers[session_id]
                container.remove(force=True)
                del self.containers[session_id]
            except Exception as e:
                logger.error(f"Error removing container: {e}")
                
        if session_id in self.temp_dirs:
            try:
                shutil.rmtree(self.temp_dirs[session_id])
                del self.temp_dirs[session_id]
            except Exception as e:
                logger.error(f"Error removing temp directory: {e}")
