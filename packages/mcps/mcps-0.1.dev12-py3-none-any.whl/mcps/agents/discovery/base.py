from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class AgentMetadata:
    """Agent metadata information"""
    agent_id: str
    name: str
    description: str
    version: str
    capabilities: List[str]
    required_tools: List[str]
    model_type: str  # e.g., "gpt-4", "claude-3", etc.
    created_at: datetime
    updated_at: datetime
    owner: str
    tags: List[str]
    config: Dict[str, Any]

@dataclass
class AgentMatch:
    """Agent match result with confidence score"""
    agent: AgentMetadata
    confidence: float  # 0.0 to 1.0
    required_tools: List[str]
    estimated_cost: Optional[float] = None

class AgentDiscoverer(ABC):
    """Base class for agent discovery implementations"""
    
    @abstractmethod
    def find_by_query(self, query: str, top_k: int = 3) -> List[AgentMatch]:
        """Find agents using natural language query
        
        Args:
            query: Natural language query string
            top_k: Number of top results to return
            
        Returns:
            List of matching agents with confidence scores
        """
        pass
    
    @abstractmethod
    def find_by_capabilities(self, capabilities: List[str]) -> List[AgentMatch]:
        """Find agents by required capabilities
        
        Args:
            capabilities: List of required capability strings
            
        Returns:
            List of matching agents with confidence scores
        """
        pass
    
    @abstractmethod
    def get_agent(self, agent_id: str) -> AgentMetadata:
        """Get agent metadata by ID
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Agent metadata
        """
        pass
    
    @abstractmethod
    def register_agent(self, metadata: AgentMetadata) -> str:
        """Register a new agent
        
        Args:
            metadata: Agent metadata
            
        Returns:
            Agent ID
        """
        pass
    
    @abstractmethod
    def update_agent(self, agent_id: str, updates: Dict[str, Any]) -> AgentMetadata:
        """Update agent metadata
        
        Args:
            agent_id: Agent identifier
            updates: Dictionary of fields to update
            
        Returns:
            Updated agent metadata
        """
        pass 