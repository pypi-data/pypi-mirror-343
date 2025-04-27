"""Top-level agent manager for MCPS."""

import os
import json
import logging
import tempfile
import shutil
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

from mcps.agents.discovery.base import AgentDiscoverer, AgentMetadata, AgentMatch
from mcps.agents.lifecycle.base import AgentLifecycleManager, AgentConfig
from mcps.agents.runtime.base import AgentRuntime, RuntimeEnvironment, ExecutionSession, AgentOutput
from mcps.agents.runtime.docker import DockerSandboxRuntime

logger = logging.getLogger(__name__)

class AgentManager:
    """Top-level agent manager that integrates discovery, lifecycle, and runtime components."""
    
    def __init__(
        self, 
        discoverer: AgentDiscoverer,
        lifecycle_manager: AgentLifecycleManager,
        runtime_registry: Optional[Dict[str, AgentRuntime]] = None,
        cache_dir: Optional[str] = None
    ):
        """Initialize agent manager.
        
        Args:
            discoverer: Agent discoverer component
            lifecycle_manager: Agent lifecycle manager component
            runtime_registry: Registry of available runtimes, keyed by container_type
            cache_dir: Optional directory for caching agent output
        """
        self.discoverer = discoverer
        self.lifecycle_manager = lifecycle_manager
        self.runtime_registry = runtime_registry or {}
        self.cache_dir = cache_dir or os.path.join(os.getcwd(), "data", "cache")
        
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir, exist_ok=True)
            
        self.active_agents = {}
        
    def find_agents_by_query(self, query: str, top_k: int = 1) -> List[AgentMatch]:
        """Find agents using natural language query.
        
        Args:
            query: Natural language query string
            top_k: Number of top results to return
            
        Returns:
            List of matching agents with confidence scores
        """
        return self.discoverer.find_by_query(query, top_k)
        
    def deploy_agent(self, agent_id: str) -> str:
        """Deploy an agent.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Deployment ID
            
        Raises:
            ValueError: If agent not found or deployment fails
        """
        try:
            metadata = self.discoverer.get_agent(agent_id)
            
            agent_config = AgentConfig(
                agent_id=metadata.agent_id,
                name=metadata.name,
                version=metadata.version,
                model_config=self._prepare_agent_code(metadata),
                resource_limits={
                    "memory": metadata.config.get("memory", "256m"),
                    "cpu": metadata.config.get("cpu", 0.5)
                },
                environment={
                    "container_type": "docker",
                    "AGENT_ID": metadata.agent_id,
                    "AGENT_NAME": metadata.name
                },
                dependencies=metadata.config.get("dependencies", []),
                startup_timeout=metadata.config.get("timeout", 30),
                shutdown_timeout=metadata.config.get("timeout", 10)
            )
            
            # The lifecycle manager returns the agent_id as the deployment_id
            deployment_id = self.lifecycle_manager.initialize(agent_config)
            
            self.active_agents[agent_id] = {
                "metadata": metadata,
                "config": agent_config,
                "deployment_id": deployment_id,
                "deployed_at": datetime.now()
            }
            
            logger.info(f"Deployed agent {agent_id} with deployment ID {deployment_id}")
            
            return deployment_id
            
        except Exception as e:
            logger.error(f"Failed to deploy agent {agent_id}: {e}")
            raise ValueError(f"Agent deployment failed: {e}")
            
    def _prepare_agent_code(self, metadata: AgentMetadata) -> Dict[str, Any]:
        """Prepare agent code for deployment.
        
        Args:
            metadata: Agent metadata
            
        Returns:
            Agent code configuration
        """
        from mcps.agents.discovery.local import LocalAgentDiscoverer
        
        if isinstance(self.discoverer, LocalAgentDiscoverer):
            discoverer = self.discoverer
            agent_dir = os.path.join(getattr(discoverer, 'data_dir', os.path.join(os.getcwd(), "data")), metadata.agent_id)
        else:
            agent_dir = os.path.join(os.getcwd(), "data", metadata.agent_id)
        
        if not os.path.exists(agent_dir):
            raise ValueError(f"Agent directory not found: {agent_dir}")
            
        entry_point = metadata.config.get("entry_point", "main.py")
        entry_path = os.path.join(agent_dir, entry_point)
        
        if not os.path.exists(entry_path):
            raise ValueError(f"Agent entry point not found: {entry_path}")
            
        with open(entry_path, "r") as f:
            code = f.read()
            
        prompt_path = os.path.join(agent_dir, "prompt.txt")
        prompt = None
        
        if os.path.exists(prompt_path):
            with open(prompt_path, "r") as f:
                prompt = f.read()
                
        return {
            "code": code,
            "prompt": prompt,
            "entry_point": entry_point,
            "config": metadata.config,
            "agent_id": metadata.agent_id  # Pass the agent_id to the runtime
        }
        
    def start_agent(self, deployment_id: str) -> None:
        """Start a deployed agent.
        
        Args:
            deployment_id: Agent deployment ID
            
        Raises:
            ValueError: If agent not found or start fails
        """
        try:
            self.lifecycle_manager.start(deployment_id)
            logger.info(f"Agent started: {deployment_id}")
            
        except Exception as e:
            logger.error(f"Failed to start agent {deployment_id}: {e}")
            raise ValueError(f"Agent start failed: {e}")
            
    def run_query(self, agent_id: str, query: str) -> Tuple[AgentOutput, str]:
        """Run a query on an agent.
        
        Args:
            agent_id: Agent ID or deployment ID
            query: Query string
            
        Returns:
            Tuple of (agent output, cache path)
            
        Raises:
            ValueError: If agent not found or query fails
        """
        try:
            logger.info(f"Active agents: {list(self.active_agents.keys())}")
            
            if agent_id in self.active_agents:
                agent_info = self.active_agents[agent_id]
                deployment_id = agent_info.get("deployment_id", agent_id)
                logger.info(f"Found agent {agent_id} in active_agents with deployment ID {deployment_id}")
            else:
                # Check if it's a deployment_id that matches any agent's deployment_id
                agent_found = False
                for aid, agent_info in self.active_agents.items():
                    if agent_info.get("deployment_id") == agent_id:
                        deployment_id = agent_id
                        agent_id = aid
                        agent_found = True
                        logger.info(f"Found agent {agent_id} by matching deployment ID {deployment_id}")
                        break
                
                if not agent_found:
                    for aid, agent_info in self.active_agents.items():
                        if agent_info["metadata"].agent_id == agent_id:
                            deployment_id = agent_info.get("deployment_id", aid)
                            agent_id = aid
                            agent_found = True
                            logger.info(f"Found agent {agent_id} by matching metadata.agent_id")
                            break
                
                if not agent_found:
                    raise ValueError(f"Agent not found: {agent_id}")
            
            logger.info(f"Running query on agent {agent_id} with deployment ID {deployment_id}")
            
            session_id = f"session_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            session = ExecutionSession(
                session_id=session_id,
                agent_id=agent_id,  # Use the agent_id for the session
                start_time=datetime.now(),
                context={
                    "query": query,
                    "timestamp": datetime.now().isoformat()
                },
                tools=[]  # Empty tools list for now
            )
            
            output = self._execute_docker_agent(agent_id, session)
            
            cache_path = self._cache_output(agent_id, session_id, output)
            
            return output, cache_path
            
        except Exception as e:
            logger.error(f"Failed to run query on agent {agent_id}: {e}")
            raise ValueError(f"Agent query failed: {e}")
            
    def _execute_docker_agent(self, agent_id: str, session: ExecutionSession) -> AgentOutput:
        """Execute a Docker agent.
        
        Args:
            agent_id: Agent ID
            session: Execution session
            
        Returns:
            Agent output
        """
        if agent_id not in self.active_agents:
            raise ValueError(f"Agent not found: {agent_id}")
            
        deployment_id = self.active_agents[agent_id].get("deployment_id")
        if not deployment_id:
            raise ValueError(f"Agent {agent_id} not deployed")
            
        # Update the session with the deployment ID
        session.agent_id = deployment_id
            
        container_type = self.active_agents[agent_id]["config"].environment.get("container_type", "docker")
        runtime = self.runtime_registry.get(container_type)
        
        if not runtime:
            raise ValueError(f"No runtime available for container type: {container_type}")
        
        logger.info(f"Executing agent {agent_id} with deployment ID {deployment_id} using {container_type} runtime")
            
        return runtime.execute(session)
        
    def _cache_output(self, deployment_id: str, session_id: str, output: AgentOutput) -> str:
        """Cache agent output.
        
        Args:
            deployment_id: Agent deployment ID
            session_id: Session ID
            output: Agent output
            
        Returns:
            Cache file path
        """
        cache_file = os.path.join(self.cache_dir, f"{deployment_id}_{session_id}.json")
        
        with open(cache_file, "w") as f:
            json.dump({
                "deployment_id": deployment_id,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "result": output.result,
                "status": output.status,
                "error": output.error,
                "metadata": output.metadata
            }, f, indent=2)
            
        return cache_file
        
    def stop_agent(self, agent_id: str) -> None:
        """Stop a running agent.
        
        Args:
            agent_id: Agent ID or deployment ID
            
        Raises:
            ValueError: If agent not found or stop fails
        """
        try:
            if agent_id in self.active_agents:
                deployment_id = self.active_agents[agent_id].get("deployment_id", agent_id)
            else:
                # Check if it's a deployment_id that matches any agent's deployment_id
                agent_found = False
                for aid, agent_info in self.active_agents.items():
                    if agent_info.get("deployment_id") == agent_id:
                        deployment_id = agent_id
                        agent_id = aid
                        agent_found = True
                        break
                
                if not agent_found:
                    raise ValueError(f"Agent not found: {agent_id}")
            
            self.lifecycle_manager.stop(deployment_id)
            logger.info(f"Agent stopped: {agent_id}")
            
        except Exception as e:
            logger.error(f"Failed to stop agent {agent_id}: {e}")
            raise ValueError(f"Agent stop failed: {e}")
            
    def cleanup_agent(self, agent_id: str) -> None:
        """Clean up agent resources.
        
        Args:
            agent_id: Agent ID or deployment ID
            
        Raises:
            ValueError: If agent not found or cleanup fails
        """
        try:
            if agent_id in self.active_agents:
                deployment_id = self.active_agents[agent_id].get("deployment_id", agent_id)
            else:
                # Check if it's a deployment_id that matches any agent's deployment_id
                agent_found = False
                for aid, agent_info in self.active_agents.items():
                    if agent_info.get("deployment_id") == agent_id:
                        deployment_id = agent_id
                        agent_id = aid
                        agent_found = True
                        break
                
                if not agent_found:
                    deployment_id = agent_id
            
            self.lifecycle_manager.cleanup(deployment_id)
            
            if agent_id in self.active_agents:
                del self.active_agents[agent_id]
                
            logger.info(f"Agent cleaned up: {agent_id}")
            
        except Exception as e:
            logger.error(f"Failed to clean up agent {agent_id}: {e}")
            raise ValueError(f"Agent cleanup failed: {e}")
            
    def get_agent_state(self, agent_id: str) -> Dict[str, Any]:
        """Get agent state.
        
        Args:
            agent_id: Agent ID or deployment ID
            
        Returns:
            Agent state
            
        Raises:
            ValueError: If agent not found
        """
        try:
            if agent_id in self.active_agents:
                deployment_id = self.active_agents[agent_id].get("deployment_id", agent_id)
            else:
                # Check if it's a deployment_id that matches any agent's deployment_id
                agent_found = False
                for aid, agent_info in self.active_agents.items():
                    if agent_info.get("deployment_id") == agent_id:
                        deployment_id = agent_id
                        agent_id = aid
                        agent_found = True
                        break
                
                if not agent_found:
                    deployment_id = agent_id
            
            state = self.lifecycle_manager.get_state(deployment_id)
            
            return {
                "agent_id": state.agent_id,
                "status": state.status,
                "current_task": state.current_task,
                "last_heartbeat": state.last_heartbeat.isoformat() if state.last_heartbeat else None,
                "resource_usage": state.resource_usage,
                "metadata": state.metadata
            }
            
        except Exception as e:
            logger.error(f"Failed to get agent state {agent_id}: {e}")
            raise ValueError(f"Failed to get agent state: {e}")
