from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from .base import ServiceRegistry, ServiceRegistration

class InMemoryServiceRegistry(ServiceRegistry):
    """In-memory implementation of service registry"""
    
    def __init__(self):
        self._services: Dict[str, ServiceRegistration] = {}
    
    def register(self, service: ServiceRegistration) -> str:
        """Register a new service
        
        Args:
            service: Service registration information
            
        Returns:
            Service ID
        """
        service_id = str(uuid.uuid4())
        now = datetime.now()
        
        registration = ServiceRegistration(
            service_id=service_id,
            name=service.name,
            description=service.description,
            version=service.version,
            category=service.category,
            metadata=service.metadata,
            endpoint=service.endpoint,
            protocol=service.protocol,
            created_at=now,
            updated_at=now,
            status="active",
            owner=service.owner,
            tags=service.tags
        )
        
        self._services[service_id] = registration
        return service_id
    
    def update(self, service_id: str, updates: Dict[str, Any]) -> ServiceRegistration:
        """Update service registration
        
        Args:
            service_id: Service identifier
            updates: Dictionary of fields to update
            
        Returns:
            Updated service registration
        """
        if service_id not in self._services:
            raise KeyError(f"Service {service_id} not found")
            
        service = self._services[service_id]
        updated_fields = {}
        
        for field, value in updates.items():
            if hasattr(service, field):
                updated_fields[field] = value
        
        updated_fields['updated_at'] = datetime.now()
        updated_service = ServiceRegistration(**{
            **service.__dict__,
            **updated_fields
        })
        
        self._services[service_id] = updated_service
        return updated_service
    
    def deregister(self, service_id: str) -> None:
        """Deregister a service
        
        Args:
            service_id: Service identifier to deregister
        """
        if service_id not in self._services:
            raise KeyError(f"Service {service_id} not found")
            
        del self._services[service_id]
    
    def get(self, service_id: str) -> Optional[ServiceRegistration]:
        """Get service registration by ID
        
        Args:
            service_id: Service identifier
            
        Returns:
            Service registration if found, None otherwise
        """
        return self._services.get(service_id)
    
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
        services = self._services.values()
        
        if category:
            services = [s for s in services if s.category == category]
        if status:
            services = [s for s in services if s.status == status]
        if owner:
            services = [s for s in services if s.owner == owner]
            
        return list(services)
    
    def search(self, query: str, limit: int = 10) -> List[ServiceRegistration]:
        """Search services using text query
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of matching service registrations
        """
        query = query.lower()
        matches = []
        
        for service in self._services.values():
            if (query in service.name.lower() or
                query in service.description.lower() or
                query in service.category.lower() or
                any(query in tag.lower() for tag in service.tags)):
                matches.append(service)
                
        return sorted(matches, key=lambda x: x.updated_at, reverse=True)[:limit] 