"""Service discovery components for MCPS.

This module provides service discovery mechanisms for locating and
connecting to services in the MCPS framework.
"""

from .base import ServiceDiscoverer, ServiceDescriptor
from .registry_based import RegistryBasedDiscoverer

__all__ = [
    'ServiceDiscoverer',
    'ServiceDescriptor',
    'RegistryBasedDiscoverer'
] 