from typing import List, Dict, Any
from .base import ServiceDiscoverer, ServiceDescriptor
from ..registry.base import ServiceRegistry

class RegistryBasedDiscoverer(ServiceDiscoverer):
    """Service discoverer implementation that uses the service registry"""
    
    def __init__(self, registry: ServiceRegistry):
        self.registry = registry
    
    def find_by_nlp(self, query: str, top_k: int = 3) -> List[ServiceDescriptor]:
        """Find services using natural language query
        
        Args:
            query: Natural language query string
            top_k: Number of top results to return
            
        Returns:
            List of matching service descriptors
        """
        # Use the registry's search functionality
        registrations = self.registry.search(query, limit=top_k)
        
        # Convert registrations to descriptors
        return [self._registration_to_descriptor(reg) for reg in registrations]
    
    def find_by_metadata(self, filters: Dict[str, Any]) -> List[ServiceDescriptor]:
        """Find services using structured metadata filters
        
        Args:
            filters: Dictionary of metadata filters
            
        Returns:
            List of matching service descriptors
        """
        # Extract known filter fields
        category = filters.get('category')
        status = filters.get('status')
        owner = filters.get('owner')
        
        # Use the registry's list_services with filters
        registrations = self.registry.list_services(
            category=category,
            status=status,
            owner=owner
        )
        
        # Convert registrations to descriptors
        return [self._registration_to_descriptor(reg) for reg in registrations]
    
    def get_service(self, service_id: str) -> ServiceDescriptor:
        """Get service descriptor by ID
        
        Args:
            service_id: Unique service identifier
            
        Returns:
            Service descriptor for the requested service
        """
        registration = self.registry.get(service_id)
        if not registration:
            raise KeyError(f"Service {service_id} not found")
            
        return self._registration_to_descriptor(registration)
    
    def _registration_to_descriptor(self, registration: 'ServiceRegistration') -> ServiceDescriptor:
        """Convert a service registration to a service descriptor
        
        Args:
            registration: Service registration object
            
        Returns:
            Service descriptor object
        """
        return ServiceDescriptor(
            service_id=registration.service_id,
            name=registration.name,
            description=registration.description,
            version=registration.version,
            category=registration.category,
            metadata=registration.metadata,
            endpoint=registration.endpoint,
            protocol=registration.protocol
        ) 