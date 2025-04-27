from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class RuntimeEnvironment:
    """Runtime environment configuration"""
    container_type: str  # docker, k8s, etc.
    resources: Dict[str, Any]  # CPU, memory, GPU requirements
    network_config: Dict[str, Any]
    env_vars: Dict[str, str]

@dataclass
class ExecutionSession:
    """Session information for agent execution"""
    session_id: str
    agent_id: str
    start_time: datetime
    context: Dict[str, Any]
    tools: List[str]

@dataclass
class AgentOutput:
    """Standardized agent output"""
    result: Any
    status: str
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RuntimeSnapshot:
    """Runtime state snapshot"""
    session_id: str
    timestamp: datetime
    state: Dict[str, Any]
    metrics: Dict[str, float]

class AgentRuntime(ABC):
    """Base class for agent runtime implementations"""
    
    def __init__(self, env: RuntimeEnvironment):
        self.environment = env
    
    @abstractmethod
    def deploy(self, agent_package: Dict[str, Any]) -> str:
        """Deploy agent instance
        
        Args:
            agent_package: Agent deployment package
            
        Returns:
            Deployment ID
        """
        pass
    
    @abstractmethod
    def execute(self, session: ExecutionSession) -> AgentOutput:
        """Execute agent task
        
        Args:
            session: Execution session information
            
        Returns:
            Agent execution output
        """
        pass
    
    @abstractmethod
    def snapshot(self) -> RuntimeSnapshot:
        """Get runtime state snapshot
        
        Returns:
            Current runtime state snapshot
        """
        pass
    
    @abstractmethod
    def cleanup(self, session_id: str) -> None:
        """Clean up resources for a session
        
        Args:
            session_id: Session identifier to clean up
        """
        pass  