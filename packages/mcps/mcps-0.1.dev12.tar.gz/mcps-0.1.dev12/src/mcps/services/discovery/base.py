from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ServiceDescriptor:
    """Service metadata descriptor"""
    service_id: str
    name: str
    description: str
    version: str
    category: str
    metadata: Dict[str, Any]
    endpoint: str
    protocol: str

class ServiceDiscoverer(ABC):
    """Base class for service discovery implementations"""
    
    @abstractmethod
    def find_by_nlp(self, query: str, top_k: int = 3) -> List[ServiceDescriptor]:
        """Find services using natural language query
        
        Args:
            query: Natural language query string
            top_k: Number of top results to return
            
        Returns:
            List of matching service descriptors
        """
        pass
    
    @abstractmethod
    def find_by_metadata(self, filters: Dict[str, Any]) -> List[ServiceDescriptor]:
        """Find services using structured metadata filters
        
        Args:
            filters: Dictionary of metadata filters
            
        Returns:
            List of matching service descriptors
        """
        pass
    
    @abstractmethod
    def get_service(self, service_id: str) -> ServiceDescriptor:
        """Get service descriptor by ID
        
        Args:
            service_id: Unique service identifier
            
        Returns:
            Service descriptor for the requested service
        """
        pass 