"""Command-line interface components for MCPS.

This module provides command-line interface capabilities including
command management and plugin system for the MCPS framework.
"""

from .base import (
    BaseCommand,
    BasePlugin,
    PluginManager,
    CommandContext,
    CommandResult,
    PluginMetadata
)
from .commands.basic import HelpCommand, VersionCommand, ConfigCommand
from .plugins.manager import DefaultPluginManager

__all__ = [
    'BaseCommand',
    'BasePlugin',
    'PluginManager',
    'CommandContext',
    'CommandResult',
    'PluginMetadata',
    'HelpCommand',
    'VersionCommand',
    'ConfigCommand',
    'DefaultPluginManager'
] 