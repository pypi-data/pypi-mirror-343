"""Local file-based agent discoverer for MCPS."""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from mcps.agents.discovery.base import AgentDiscoverer, AgentMetadata, AgentMatch

logger = logging.getLogger(__name__)

class LocalAgentDiscoverer(AgentDiscoverer):
    """Local file-based agent discoverer that loads agents from a directory."""
    
    def __init__(self, data_dir: str):
        """Initialize with the path to the data directory.
        
        Args:
            data_dir: Path to directory containing agent data
        """
        self.data_dir = data_dir
        self.agents = {}
        self._load_agents()
        
    def _load_agents(self) -> None:
        """Load agents from the data directory."""
        logger.info(f"Loading agents from {self.data_dir}")
        
        if not os.path.exists(self.data_dir):
            logger.warning(f"Data directory does not exist: {self.data_dir}")
            return
            
        for agent_dir in os.listdir(self.data_dir):
            agent_path = os.path.join(self.data_dir, agent_dir)
            
            if not os.path.isdir(agent_path):
                continue
                
            config_path = os.path.join(agent_path, "config.json")
            
            if not os.path.exists(config_path):
                logger.warning(f"No config.json found in {agent_path}")
                continue
                
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
                    
                agent_id = config.get("agent_id")
                
                if not agent_id:
                    logger.warning(f"No agent_id found in {config_path}")
                    continue
                    
                try:
                    created_at = datetime.fromisoformat(config.get("created_at", "").replace("Z", "+00:00"))
                    updated_at = datetime.fromisoformat(config.get("updated_at", "").replace("Z", "+00:00"))
                except ValueError:
                    logger.warning(f"Invalid datetime format in {config_path}")
                    created_at = datetime.now()
                    updated_at = datetime.now()
                    
                metadata = AgentMetadata(
                    agent_id=agent_id,
                    name=config.get("name", ""),
                    description=config.get("description", ""),
                    version=config.get("version", ""),
                    capabilities=config.get("capabilities", []),
                    required_tools=config.get("required_tools", []),
                    model_type=config.get("model_type", ""),
                    created_at=created_at,
                    updated_at=updated_at,
                    owner=config.get("owner", ""),
                    tags=config.get("tags", []),
                    config=config.get("config", {})
                )
                
                self.agents[agent_id] = metadata
                logger.info(f"Loaded agent: {agent_id}")
                
            except Exception as e:
                logger.error(f"Error loading agent from {config_path}: {e}")
                
        logger.info(f"Loaded {len(self.agents)} agents")
        
    def find_by_query(self, query: str, top_k: int = 3) -> List[AgentMatch]:
        """Find agents using natural language query.
        
        This implementation uses a simple keyword matching approach.
        
        Args:
            query: Natural language query string
            top_k: Number of top results to return
            
        Returns:
            List of matching agents with confidence scores
        """
        matches = []
        
        for agent_id, metadata in self.agents.items():
            score = 0.0
            
            keywords = query.lower().split()
            
            for keyword in keywords:
                if keyword in metadata.name.lower():
                    score += 0.5
                if keyword in metadata.description.lower():
                    score += 0.3
                if keyword in " ".join(metadata.capabilities).lower():
                    score += 0.2
                if keyword in " ".join(metadata.tags).lower():
                    score += 0.1
                    
            if score > 0:
                matches.append(AgentMatch(
                    agent=metadata,
                    confidence=min(score, 1.0),  # Normalize to 0.0-1.0
                    required_tools=metadata.required_tools,
                    estimated_cost=None
                ))
                
        matches.sort(key=lambda m: m.confidence, reverse=True)
        return matches[:top_k]
    
    def find_by_capabilities(self, capabilities: List[str]) -> List[AgentMatch]:
        """Find agents by required capabilities.
        
        Args:
            capabilities: List of required capability strings
            
        Returns:
            List of matching agents with confidence scores
        """
        matches = []
        
        for agent_id, metadata in self.agents.items():
            matching_capabilities = set(capabilities).intersection(set(metadata.capabilities))
            
            if matching_capabilities:
                score = len(matching_capabilities) / len(capabilities)
                
                matches.append(AgentMatch(
                    agent=metadata,
                    confidence=score,
                    required_tools=metadata.required_tools,
                    estimated_cost=None
                ))
                
        matches.sort(key=lambda m: m.confidence, reverse=True)
        return matches
    
    def get_agent(self, agent_id: str) -> AgentMetadata:
        """Get agent metadata by ID.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Agent metadata
            
        Raises:
            ValueError: If agent not found
        """
        if agent_id not in self.agents:
            raise ValueError(f"Agent not found: {agent_id}")
            
        return self.agents[agent_id]
    
    def register_agent(self, metadata: AgentMetadata) -> str:
        """Register a new agent.
        
        Args:
            metadata: Agent metadata
            
        Returns:
            Agent ID
        """
        agent_id = metadata.agent_id
        self.agents[agent_id] = metadata
        return agent_id
    
    def update_agent(self, agent_id: str, updates: Dict[str, Any]) -> AgentMetadata:
        """Update agent metadata.
        
        Args:
            agent_id: Agent identifier
            updates: Dictionary of fields to update
            
        Returns:
            Updated agent metadata
            
        Raises:
            ValueError: If agent not found
        """
        if agent_id not in self.agents:
            raise ValueError(f"Agent not found: {agent_id}")
            
        metadata = self.agents[agent_id]
        
        for key, value in updates.items():
            if hasattr(metadata, key):
                setattr(metadata, key, value)
                
        metadata.updated_at = datetime.now()
                
        return metadata
        
    def list_agents(self) -> List[AgentMetadata]:
        """List all available agents.
        
        Returns:
            List of agent metadata
        """
        return list(self.agents.values())
