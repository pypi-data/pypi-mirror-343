from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ServicePolicy:
    """Service policy configuration"""
    policy_id: str
    name: str
    description: str
    rules: Dict[str, Any]
    priority: int
    enabled: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class HealthCheck:
    """Service health check configuration"""
    check_id: str
    service_id: str
    check_type: str  # http, tcp, custom
    endpoint: str
    interval: int  # seconds
    timeout: int  # seconds
    retries: int
    enabled: bool

@dataclass
class HealthStatus:
    """Service health status"""
    service_id: str
    status: str  # healthy, unhealthy, degraded
    last_check: datetime
    details: Dict[str, Any]
    metrics: Dict[str, float]

class ServiceGovernor(ABC):
    """Base class for service governance implementations"""
    
    @abstractmethod
    def enforce_policies(self, service_id: str) -> bool:
        """Enforce policies for a service
        
        Args:
            service_id: Service identifier
            
        Returns:
            True if policies are enforced successfully
        """
        pass
    
    @abstractmethod
    def monitor_health(self, service_id: str) -> HealthStatus:
        """Monitor service health
        
        Args:
            service_id: Service identifier
            
        Returns:
            Current health status
        """
        pass
    
    @abstractmethod
    def add_policy(self, policy: ServicePolicy) -> str:
        """Add a new service policy
        
        Args:
            policy: Policy configuration
            
        Returns:
            Policy ID
        """
        pass
    
    @abstractmethod
    def update_policy(self, policy_id: str, updates: Dict[str, Any]) -> ServicePolicy:
        """Update an existing policy
        
        Args:
            policy_id: Policy identifier
            updates: Dictionary of fields to update
            
        Returns:
            Updated policy
        """
        pass
    
    @abstractmethod
    def remove_policy(self, policy_id: str) -> None:
        """Remove a policy
        
        Args:
            policy_id: Policy identifier to remove
        """
        pass
    
    @abstractmethod
    def get_policies(self, service_id: Optional[str] = None) -> List[ServicePolicy]:
        """Get policies with optional service filter
        
        Args:
            service_id: Optional service identifier to filter by
            
        Returns:
            List of matching policies
        """
        pass
    
    @abstractmethod
    def configure_health_check(self, check: HealthCheck) -> str:
        """Configure health check for a service
        
        Args:
            check: Health check configuration
            
        Returns:
            Health check ID
        """
        pass
    
    @abstractmethod
    def get_health_status(self, service_id: str) -> HealthStatus:
        """Get current health status for a service
        
        Args:
            service_id: Service identifier
            
        Returns:
            Current health status
        """
        pass 