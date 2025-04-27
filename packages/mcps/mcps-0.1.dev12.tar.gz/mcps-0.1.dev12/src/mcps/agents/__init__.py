"""Agent management components for MCPS.

This module provides agent discovery, lifecycle management, and runtime
environment capabilities for managing intelligent agents in the MCPS framework.
"""

from .discovery.base import AgentDiscoverer, AgentMetadata, AgentMatch
from .discovery.local import LocalAgentDiscoverer
from .runtime.base import (
    AgentRuntime,
    RuntimeEnvironment,
    ExecutionSession,
    AgentOutput,
    RuntimeSnapshot
)
from .runtime.docker import DockerSandboxRuntime, DockerSandboxConfig
from .runtime.python import PythonRuntime, PythonRuntimeConfig
from .runtime.resource import ResourceGovernor, ResourceQuota
from .lifecycle.base import (
    AgentLifecycleManager,
    AgentState,
    AgentConfig
)
from .lifecycle.standard import StandardLifecycleManager
from .agent_manager import AgentManager

__all__ = [
    'AgentDiscoverer',
    'AgentMetadata',
    'AgentMatch',
    'LocalAgentDiscoverer',
    'AgentRuntime',
    'RuntimeEnvironment',
    'ExecutionSession',
    'AgentOutput',
    'RuntimeSnapshot',
    'DockerSandboxRuntime',
    'DockerSandboxConfig',
    'PythonRuntime',
    'PythonRuntimeConfig',
    'ResourceGovernor',
    'ResourceQuota',
    'AgentLifecycleManager',
    'AgentState',
    'AgentConfig',
    'StandardLifecycleManager',
    'AgentManager'
]       