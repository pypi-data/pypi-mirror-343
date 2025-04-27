"""Service registry components for MCPS.

This module provides service registration and discovery capabilities
for managing service instances in the MCPS framework.
"""

from .base import ServiceRegistry, ServiceRegistration
from .memory import InMemoryServiceRegistry

__all__ = [
    'ServiceRegistry',
    'ServiceRegistration',
    'InMemoryServiceRegistry'
] 