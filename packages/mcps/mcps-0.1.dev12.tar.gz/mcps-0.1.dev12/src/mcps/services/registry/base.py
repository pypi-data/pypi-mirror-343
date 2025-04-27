from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ServiceRegistration:
    """Service registration information"""
    service_id: str
    name: str
    description: str
    version: str
    category: str
    metadata: Dict[str, Any]
    endpoint: str
    protocol: str
    created_at: datetime
    updated_at: datetime
    status: str  # active, inactive, deprecated
    owner: str
    tags: List[str]

class ServiceRegistry(ABC):
    """Base class for service registry implementations"""
    
    @abstractmethod
    def register(self, service: ServiceRegistration) -> str:
        """Register a new service
        
        Args:
            service: Service registration information
            
        Returns:
            Service ID
        """
        pass
    
    @abstractmethod
    def update(self, service_id: str, updates: Dict[str, Any]) -> ServiceRegistration:
        """Update service registration
        
        Args:
            service_id: Service identifier
            updates: Dictionary of fields to update
            
        Returns:
            Updated service registration
        """
        pass
    
    @abstractmethod
    def deregister(self, service_id: str) -> None:
        """Deregister a service
        
        Args:
            service_id: Service identifier to deregister
        """
        pass
    
    @abstractmethod
    def get(self, service_id: str) -> Optional[ServiceRegistration]:
        """Get service registration by ID
        
        Args:
            service_id: Service identifier
            
        Returns:
            Service registration if found, None otherwise
        """
        pass
    
    @abstractmethod
    def list_services(self, 
                     category: Optional[str] = None,
                     status: Optional[str] = None,
                     owner: Optional[str] = None) -> List[ServiceRegistration]:
        """List registered services with optional filters
        
        Args:
            category: Filter by service category
            status: Filter by service status
            owner: Filter by service owner
            
        Returns:
            List of matching service registrations
        """
        pass
    
    @abstractmethod
    def search(self, query: str, limit: int = 10) -> List[ServiceRegistration]:
        """Search services using text query
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of matching service registrations
        """
        pass 