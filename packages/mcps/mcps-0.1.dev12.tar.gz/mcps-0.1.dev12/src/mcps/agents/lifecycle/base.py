from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class AgentState:
    """Agent state information"""
    agent_id: str
    status: str  # initializing, running, stopped, error
    current_task: Optional[str]
    last_heartbeat: datetime
    resource_usage: Dict[str, float]
    metadata: Dict[str, Any]

@dataclass
class AgentConfig:
    """Agent configuration"""
    agent_id: str
    name: str
    version: str
    model_config: Dict[str, Any]
    resource_limits: Dict[str, Any]
    environment: Dict[str, str]
    dependencies: List[str]
    startup_timeout: int  # seconds
    shutdown_timeout: int  # seconds

class AgentLifecycleManager(ABC):
    """Base class for agent lifecycle management"""
    
    @abstractmethod
    def initialize(self, config: AgentConfig) -> str:
        """Initialize a new agent
        
        Args:
            config: Agent configuration
            
        Returns:
            Agent ID
        """
        pass
    
    @abstractmethod
    def start(self, agent_id: str) -> None:
        """Start an agent
        
        Args:
            agent_id: Agent identifier
        """
        pass
    
    @abstractmethod
    def stop(self, agent_id: str) -> None:
        """Stop an agent
        
        Args:
            agent_id: Agent identifier
        """
        pass
    
    @abstractmethod
    def cleanup(self, agent_id: str) -> None:
        """Clean up agent resources
        
        Args:
            agent_id: Agent identifier
        """
        pass
    
    @abstractmethod
    def get_state(self, agent_id: str) -> AgentState:
        """Get current agent state
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Current agent state
        """
        pass
    
    @abstractmethod
    def update_config(self, agent_id: str, updates: Dict[str, Any]) -> AgentConfig:
        """Update agent configuration
        
        Args:
            agent_id: Agent identifier
            updates: Dictionary of fields to update
            
        Returns:
            Updated agent configuration
        """
        pass
    
    @abstractmethod
    def list_agents(self, status: Optional[str] = None) -> List[AgentState]:
        """List agents with optional status filter
        
        Args:
            status: Optional status to filter by
            
        Returns:
            List of matching agent states
        """
        pass
    
    @abstractmethod
    def register_heartbeat(self, agent_id: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Register agent heartbeat
        
        Args:
            agent_id: Agent identifier
            metadata: Optional heartbeat metadata
        """
        pass 