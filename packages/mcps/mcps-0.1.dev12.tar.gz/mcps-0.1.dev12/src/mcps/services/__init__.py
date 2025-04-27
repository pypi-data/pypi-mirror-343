"""Service management components for MCPS.

This module provides service discovery, registration, and governance capabilities
for managing distributed services in the MCPS framework.
"""

from .discovery.base import ServiceDiscoverer, ServiceDescriptor
from .discovery.registry_based import RegistryBasedDiscoverer
from .registry.base import ServiceRegistry, ServiceRegistration
from .registry.memory import InMemoryServiceRegistry
from .governance.base import (
    ServiceGovernor,
    ServicePolicy,
    HealthCheck,
    HealthStatus
)

__all__ = [
    'ServiceDiscoverer',
    'ServiceDescriptor',
    'RegistryBasedDiscoverer',
    'ServiceRegistry',
    'ServiceRegistration',
    'InMemoryServiceRegistry',
    'ServiceGovernor',
    'ServicePolicy',
    'HealthCheck',
    'HealthStatus'
] 