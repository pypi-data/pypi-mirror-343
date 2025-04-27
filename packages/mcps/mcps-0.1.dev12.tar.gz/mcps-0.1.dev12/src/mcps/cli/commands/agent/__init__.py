"""Agent CLI commands for MCPS."""

from mcps.cli.commands.agent.discovery import (
    AgentListCommand,
    AgentQueryCommand,
    AgentCapabilitiesCommand,
    AgentInfoCommand
)
from mcps.cli.commands.agent.lifecycle import (
    AgentDeployCommand,
    AgentStartCommand,
    AgentStopCommand,
    AgentRunCommand,
    AgentCleanupCommand,
    AgentStatusCommand,
    AgentPullCommand
)

__all__ = [
    'AgentListCommand',
    'AgentQueryCommand',
    'AgentCapabilitiesCommand',
    'AgentInfoCommand',
    'AgentDeployCommand',
    'AgentStartCommand',
    'AgentStopCommand',
    'AgentRunCommand',
    'AgentCleanupCommand',
    'AgentStatusCommand',
    'AgentPullCommand'
]
