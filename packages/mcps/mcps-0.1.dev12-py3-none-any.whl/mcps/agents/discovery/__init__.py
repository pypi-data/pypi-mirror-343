"""Agent discovery components for MCPS.

This module provides agent discovery capabilities for finding
and managing agent instances in the system.
"""

from .base import (
    AgentDiscoverer,
    AgentMetadata,
    AgentMatch
)
from .local import LocalAgentDiscoverer


__all__ = [
    'AgentDiscoverer',
    'AgentMetadata',
    'AgentMatch',
    'LocalAgentDiscoverer'
]     