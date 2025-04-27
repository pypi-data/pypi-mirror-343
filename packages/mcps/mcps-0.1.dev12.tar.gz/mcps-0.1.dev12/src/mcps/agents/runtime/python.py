"""Python runtime implementation for agent execution."""

import os
import sys
import uuid
import json
import logging
import importlib.util
import tempfile
from typing import Dict, Any, Optional, List
from datetime import datetime
import multiprocessing
import signal
from dataclasses import dataclass, field
import traceback

from mcps.agents.runtime.base import (
    AgentRuntime,
    RuntimeEnvironment,
    ExecutionSession,
    AgentOutput,
    RuntimeSnapshot
)

try:
    from google import genai
except ImportError:
    class GenaiMock:
        def __getattr__(self, name):
            return self
        
        def __call__(self, *args, **kwargs):
            return self
    
    genai = GenaiMock()

logger = logging.getLogger(__name__)

@dataclass
class PythonRuntimeConfig:
    """Configuration for Python runtime."""
    timeout: int = 30
    max_memory_mb: int = 256
    enable_network: bool = False
    allowed_modules: List[str] = field(default_factory=lambda: [
        "os", "sys", "json", "time", "datetime", "math", 
        "collections", "itertools", "functools", "re", 
        "google.genai"
    ])
    blocked_modules: List[str] = field(default_factory=lambda: [
        "subprocess", "socket", "multiprocessing", "threading",
        "pickle", "shelve", "dbm"
    ])

def _execute_agent_task(code: str, context: Dict[str, Any], result_queue: multiprocessing.Queue):
    """Execute agent task in a separate process.
    
    Args:
        code: Agent code string
        context: Execution context
        result_queue: Queue to store execution result
    """
    try:
        namespace = {
            "context": context,
            "result": None,
            "genai": genai
        }
        
        exec(code, namespace)
        
        result = namespace.get("result")
        result_queue.put({
            "status": "success",
            "result": result
        })
    except Exception as e:
        result_queue.put({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

class PythonRuntime(AgentRuntime):
    """Python runtime for agent execution."""
    
    def __init__(self, env: RuntimeEnvironment):
        """Initialize Python runtime.
        
        Args:
            env: Runtime environment configuration
        """
        super().__init__(env)
        self.processes = {}
        self.deployments = {}
        self.config = PythonRuntimeConfig(
            timeout=env.resources.get("timeout", 30),
            max_memory_mb=env.resources.get("memory", 256),
            enable_network=not env.network_config.get("disable", False)
        )
        
        genai_api_key = env.env_vars.get("GENAI_API_KEY")
        if genai_api_key:
            genai.configure(api_key=genai_api_key)
        
    def deploy(self, agent_package: Dict[str, Any]) -> str:
        """Deploy agent instance.
        
        Args:
            agent_package: Agent deployment package
            
        Returns:
            Deployment ID
        """
        deployment_id = str(uuid.uuid4())
        
        self.deployments[deployment_id] = {
            "code": agent_package.get("code", ""),
            "created_at": datetime.utcnow()
        }
        
        logger.info(f"Deployed agent {deployment_id} with package")
        return deployment_id
        
    def execute(self, session: ExecutionSession) -> AgentOutput:
        """Execute agent task in Python runtime.
        
        Args:
            session: Execution session information
            
        Returns:
            Agent execution output
        """
        deployment_id = session.agent_id
        
        if deployment_id not in self.deployments:
            raise ValueError(f"Agent {deployment_id} not deployed")
        
        agent_code = self.deployments[deployment_id]["code"]
        
        result_queue = multiprocessing.Queue()
        
        process = multiprocessing.Process(
            target=_execute_agent_task,
            args=(agent_code, session.context, result_queue)
        )
        
        self.processes[session.session_id] = process
        process.start()
        
        try:
            process.join(timeout=self.config.timeout)
            
            if process.is_alive():
                process.terminate()
                process.join(1)
                if process.is_alive() and process.pid is not None:
                    os.kill(process.pid, signal.SIGKILL)
                return AgentOutput(
                    result=None,
                    status="error",
                    error=f"Execution timed out after {self.config.timeout} seconds",
                    metadata={"execution_time": self.config.timeout}
                )
            
            if not result_queue.empty():
                result_data = result_queue.get()
                if result_data.get("status") == "success":
                    return AgentOutput(
                        result=result_data.get("result"),
                        status="success",
                        metadata={"execution_time": (datetime.utcnow() - session.start_time).total_seconds()}
                    )
                else:
                    return AgentOutput(
                        result=None,
                        status="error",
                        error=result_data.get("error"),
                        metadata={
                            "execution_time": (datetime.utcnow() - session.start_time).total_seconds(),
                            "traceback": result_data.get("traceback")
                        }
                    )
            else:
                return AgentOutput(
                    result=None,
                    status="error",
                    error="No result returned from agent execution",
                    metadata={"execution_time": (datetime.utcnow() - session.start_time).total_seconds()}
                )
                
        except Exception as e:
            logger.exception(f"Error executing agent: {e}")
            return AgentOutput(
                result=None,
                status="error",
                error=str(e),
                metadata={"error_type": type(e).__name__}
            )
        finally:
            if session.session_id in self.processes:
                del self.processes[session.session_id]
            
    def snapshot(self) -> RuntimeSnapshot:
        """Get runtime state snapshot.
        
        Returns:
            Current runtime state snapshot
        """
        metrics = {}
        process_states = {}
        
        for session_id, process in self.processes.items():
            try:
                process_states[session_id] = "running" if process.is_alive() else "completed"
                if process.is_alive():
                    metrics[session_id] = {
                        "cpu": 0.0,  # Not easily available without psutil
                        "memory": 0.0  # Not easily available without psutil
                    }
            except Exception as e:
                logger.error(f"Error getting process info: {e}")
        
        flat_metrics = {
            "active_processes": float(len([p for p in self.processes.values() if p.is_alive()])),
            "total_deployments": float(len(self.deployments))
        }
        
        for session_id, process_metrics in metrics.items():
            for metric_key, metric_value in process_metrics.items():
                flat_metrics[f"process_{session_id}_{metric_key}"] = float(metric_value)
                
        return RuntimeSnapshot(
            session_id="all",
            timestamp=datetime.utcnow(),
            state={
                "active_processes": len([p for p in self.processes.values() if p.is_alive()]),
                "process_states": process_states,
                "deployments": len(self.deployments),
                "process_metrics": metrics  # Store detailed metrics in state
            },
            metrics=flat_metrics
        )
        
    def cleanup(self, session_id: str) -> None:
        """Clean up resources for a session.
        
        Args:
            session_id: Session identifier to clean up
        """
        if session_id in self.processes:
            try:
                process = self.processes[session_id]
                if process.is_alive():
                    process.terminate()
                    process.join(1)
                    if process.is_alive() and process.pid is not None:
                        os.kill(process.pid, signal.SIGKILL)
                del self.processes[session_id]
            except Exception as e:
                logger.error(f"Error terminating process: {e}")
