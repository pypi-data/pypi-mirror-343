"""Standard agent lifecycle management implementation for MCPS."""

import logging
import uuid
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from mcps.agents.lifecycle.base import AgentLifecycleManager, AgentState, AgentConfig
from mcps.agents.runtime.base import AgentRuntime
from mcps.utils.state.memory import InMemoryStateManager

class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder that handles datetime objects."""
    
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class StandardLifecycleManager(AgentLifecycleManager):
    """Standard implementation of agent lifecycle management.
    
    This implementation uses InMemoryStateManager for state tracking
    and integrates with runtime components for agent execution.
    """
    
    def __init__(self, runtime_registry: Optional[Dict[str, AgentRuntime]] = None):
        """Initialize lifecycle manager.
        
        Args:
            runtime_registry: Registry of available runtimes, keyed by container_type
        """
        self.logger = logging.getLogger(__name__)
        self.state_manager = InMemoryStateManager()
        self.runtime_registry = runtime_registry or {}
        
    def register_runtime(self, container_type: str, runtime: AgentRuntime) -> None:
        """Register a runtime for a specific container type.
        
        Args:
            container_type: Type of container (e.g., 'docker', 'python')
            runtime: Runtime instance for the container type
        """
        self.runtime_registry[container_type] = runtime
        self.logger.info(f"Registered runtime for container type: {container_type}")
        
    def _get_runtime(self, config: AgentConfig) -> AgentRuntime:
        """Get the appropriate runtime for the agent config.
        
        Args:
            config: Agent configuration
            
        Returns:
            Runtime instance for the agent
            
        Raises:
            ValueError: If no runtime is available for the container type
        """
        container_type = config.environment.get("container_type", "python")
        runtime = self.runtime_registry.get(container_type)
        if not runtime:
            raise ValueError(f"No runtime available for container type: {container_type}")
        return runtime
        
    def initialize(self, config: AgentConfig) -> str:
        """Initialize a new agent.
        
        Args:
            config: Agent configuration
            
        Returns:
            Agent ID
            
        Raises:
            ValueError: If initialization fails
        """
        try:
            agent_id = config.agent_id or f"agent-{uuid.uuid4()}"
            config.agent_id = agent_id
            
            self.state_manager.set_state(f"config:{agent_id}", config.__dict__)
            
            agent_state = AgentState(
                agent_id=agent_id,
                status="initialized",
                current_task=None,
                last_heartbeat=datetime.utcnow(),
                resource_usage={},
                metadata={}
            )
            state_dict = json.loads(json.dumps(agent_state.__dict__, cls=DateTimeEncoder))
            self.state_manager.set_state(f"state:{agent_id}", state_dict)
            
            runtime = self._get_runtime(config)
            deployment_id = runtime.deploy({
                "code": config.model_config.get("code", ""),
                "dependencies": config.dependencies
            })
            
            self.state_manager.set_state(f"deployment:{agent_id}", deployment_id)
            
            self.logger.info(f"Agent initialized: {agent_id}")
            return agent_id
            
        except Exception as e:
            self.logger.error(f"Failed to initialize agent: {e}")
            raise ValueError(f"Agent initialization failed: {e}")
        
    def start(self, agent_id: str) -> None:
        """Start an agent.
        
        Args:
            agent_id: Agent ID
            
        Raises:
            ValueError: If agent not found or start fails
        """
        try:
            config_dict = self.state_manager.get_state(f"config:{agent_id}")
            if not config_dict:
                raise ValueError(f"Agent not found: {agent_id}")
                
            config = AgentConfig(**config_dict)
            
            agent_state = self.get_state(agent_id)
            agent_state.status = "running"
            agent_state.last_heartbeat = datetime.utcnow()
            state_dict = json.loads(json.dumps(agent_state.__dict__, cls=DateTimeEncoder))
            self.state_manager.set_state(f"state:{agent_id}", state_dict)
            
            self.logger.info(f"Agent started: {agent_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to start agent: {e}")
            raise ValueError(f"Agent start failed: {e}")
    
    def stop(self, agent_id: str) -> None:
        """Stop an agent.
        
        Args:
            agent_id: Agent ID
            
        Raises:
            ValueError: If agent not found or stop fails
        """
        try:
            config_dict = self.state_manager.get_state(f"config:{agent_id}")
            if not config_dict:
                raise ValueError(f"Agent not found: {agent_id}")
                
            config = AgentConfig(**config_dict)
            
            agent_state = self.get_state(agent_id)
            agent_state.status = "stopped"
            agent_state.last_heartbeat = datetime.utcnow()
            state_dict = json.loads(json.dumps(agent_state.__dict__, cls=DateTimeEncoder))
            self.state_manager.set_state(f"state:{agent_id}", state_dict)
            
            self.logger.info(f"Agent stopped: {agent_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to stop agent: {e}")
            raise ValueError(f"Agent stop failed: {e}")
        
    def cleanup(self, agent_id: str) -> None:
        """Clean up agent resources.
        
        Args:
            agent_id: Agent ID
            
        Raises:
            ValueError: If agent not found or cleanup fails
        """
        try:
            config_dict = self.state_manager.get_state(f"config:{agent_id}")
            if not config_dict:
                raise ValueError(f"Agent not found: {agent_id}")
                
            config = AgentConfig(**config_dict)
            deployment_id = self.state_manager.get_state(f"deployment:{agent_id}")
            
            if deployment_id:
                runtime = self._get_runtime(config)
                runtime.cleanup(deployment_id)
            
            self.state_manager.delete_state(f"config:{agent_id}")
            self.state_manager.delete_state(f"state:{agent_id}")
            self.state_manager.delete_state(f"deployment:{agent_id}")
            
            self.logger.info(f"Agent cleaned up: {agent_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to clean up agent: {e}")
            raise ValueError(f"Agent cleanup failed: {e}")
        
    def get_state(self, agent_id: str) -> AgentState:
        """Get agent state.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Agent state
            
        Raises:
            ValueError: If agent not found
        """
        state_dict = self.state_manager.get_state(f"state:{agent_id}")
        if not state_dict:
            raise ValueError(f"Agent not found: {agent_id}")
            
        if isinstance(state_dict["last_heartbeat"], str):
            state_dict["last_heartbeat"] = datetime.fromisoformat(state_dict["last_heartbeat"])
            
        return AgentState(**state_dict)
        
    def update_config(self, agent_id: str, updates: Dict[str, Any]) -> AgentConfig:
        """Update agent configuration.
        
        Args:
            agent_id: Agent ID
            updates: Configuration updates
            
        Returns:
            Updated agent configuration
            
        Raises:
            ValueError: If agent not found or update fails
        """
        try:
            config_dict = self.state_manager.get_state(f"config:{agent_id}")
            if not config_dict:
                raise ValueError(f"Agent not found: {agent_id}")
                
            config_dict.update(updates)
            config = AgentConfig(**config_dict)
            
            self.state_manager.set_state(f"config:{agent_id}", config.__dict__)
            
            self.logger.info(f"Agent configuration updated: {agent_id}")
            return config
            
        except Exception as e:
            self.logger.error(f"Failed to update agent configuration: {e}")
            raise ValueError(f"Agent configuration update failed: {e}")
        
    def list_agents(self, status: Optional[str] = None) -> List[AgentState]:
        """List agents.
        
        Args:
            status: Optional status filter
            
        Returns:
            List of agent states
        """
        agents = []
        
        state_keys = self.state_manager.list_keys("state:*")
        
        for key in state_keys:
            agent_id = key.split(":", 1)[1]
            
            try:
                agent_state = self.get_state(agent_id)
                
                if status is None or agent_state.status == status:
                    agents.append(agent_state)
            except ValueError:
                continue
                
        return agents
    
    def register_heartbeat(self, agent_id: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Register agent heartbeat.
        
        Args:
            agent_id: Agent ID
            metadata: Optional metadata to update
            
        Raises:
            ValueError: If agent not found
        """
        try:
            agent_state = self.get_state(agent_id)
            
            agent_state.last_heartbeat = datetime.utcnow()
            if metadata:
                agent_state.metadata.update(metadata)
                
            if metadata and "resource_usage" in metadata:
                agent_state.resource_usage = metadata["resource_usage"]
                
            state_dict = json.loads(json.dumps(agent_state.__dict__, cls=DateTimeEncoder))
            self.state_manager.set_state(f"state:{agent_id}", state_dict)
            
            self.logger.debug(f"Agent heartbeat registered: {agent_id}")
            
        except ValueError as e:
            self.logger.error(f"Failed to register heartbeat for agent {agent_id}: {e}")
            raise
