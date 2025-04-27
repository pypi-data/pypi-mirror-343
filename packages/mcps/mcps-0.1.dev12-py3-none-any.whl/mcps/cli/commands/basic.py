"""Basic CLI commands for MCPS."""

import sys
import argparse
from typing import List, Optional, Dict, Any
import os

from mcps import __version__
from mcps.cli.base import BaseCommand, CommandContext, CommandResult

class HelpCommand(BaseCommand):
    """Display help information about MCPS commands."""

    name = "help"
    description = "Display help information about MCPS commands"
    
    @property
    def usage(self) -> str:
        """Get command usage information."""
        return "mcps help [command]"
    
    def validate_args(self, args: List[str], options: Dict[str, Any]) -> bool:
        """Validate command arguments.
        
        Args:
            args: Command arguments
            options: Command options
            
        Returns:
            True if arguments are valid
        """
        # Help command accepts 0 or 1 argument (the command name)
        return len(args) <= 1

    def execute(self, context: CommandContext) -> CommandResult:
        """Execute the help command."""
        parser = argparse.ArgumentParser(
            description="MCPS - Multi-Component Platform System"
        )
        parser.add_argument(
            "command",
            nargs="?",
            help="Command to get help for"
        )
        args = parser.parse_args(context.args)

        if args.command:
            # Show help for specific command
            return self._show_command_help(args.command)
        else:
            # Show general help
            return self._show_general_help()

    def _show_general_help(self) -> CommandResult:
        """Show general help information."""
        help_text = """
MCPS - Multi-Component Platform System

Usage:
    mcps <command> [options]

Available commands:
    help        Display this help message
    version     Show version information
    config      Manage MCPS configuration
    service     Manage services
    agent       Manage agents
    tool        Manage tools

Use 'mcps help <command>' to get help for a specific command.
        """
        return CommandResult(success=True, output=help_text)

    def _show_command_help(self, command: str) -> CommandResult:
        """Show help for a specific command."""
        # Add command-specific help here
        command_help = {
            "version": "Show MCPS version information",
            "config": "Manage MCPS configuration settings",
            "service": "Manage MCPS services and instances",
            "agent": "Manage MCPS agents and their lifecycle",
            "tool": "Manage MCPS tools and their execution"
        }

        if command in command_help:
            return CommandResult(success=True, output=f"{command}: {command_help[command]}")
        else:
            return CommandResult(success=False, error=f"Unknown command: {command}")

class VersionCommand(BaseCommand):
    """Display version information."""

    name = "version"
    description = "Display version information"
    
    @property
    def usage(self) -> str:
        """Get command usage information."""
        return "mcps version"
    
    def validate_args(self, args: List[str], options: Dict[str, Any]) -> bool:
        """Validate command arguments.
        
        Args:
            args: Command arguments
            options: Command options
            
        Returns:
            True if arguments are valid
        """
        # Version command doesn't accept any arguments
        return len(args) == 0

    def execute(self, context: CommandContext) -> CommandResult:
        """Execute the version command."""
        version_info = f"""
MCPS version: {__version__}
Python version: {sys.version.split()[0]}
Platform: {sys.platform}
        """
        return CommandResult(success=True, output=version_info)

class ConfigCommand(BaseCommand):
    """Manage MCPS configuration."""

    name = "config"
    description = "Manage MCPS configuration"
    
    @property
    def usage(self) -> str:
        """Get command usage information."""
        return "mcps config <action> [key] [value]"
    
    def validate_args(self, args: List[str], options: Dict[str, Any]) -> bool:
        """Validate command arguments.
        
        Args:
            args: Command arguments
            options: Command options
            
        Returns:
            True if arguments are valid
        """
        # Config command requires at least one argument (the action)
        if len(args) < 1:
            return False
            
        action = args[0]
        if action == "list":
            return len(args) == 1
        elif action == "get":
            return len(args) == 2
        elif action == "set":
            return len(args) == 3
        else:
            return False

    def execute(self, context: CommandContext) -> CommandResult:
        """Execute the config command."""
        parser = argparse.ArgumentParser(description="Manage MCPS configuration")
        parser.add_argument(
            "action",
            choices=["get", "set", "list"],
            help="Configuration action to perform"
        )
        parser.add_argument(
            "key",
            nargs="?",
            help="Configuration key"
        )
        parser.add_argument(
            "value",
            nargs="?",
            help="Configuration value (for set action)"
        )
        args = parser.parse_args(context.args)

        if args.action == "list":
            return self._list_config()
        elif args.action == "get":
            if not args.key:
                return CommandResult(success=False, error="Key is required for get action")
            return self._get_config(args.key)
        elif args.action == "set":
            if not args.key or not args.value:
                return CommandResult(success=False, error="Both key and value are required for set action")
            return self._set_config(args.key, args.value)

        return CommandResult(success=False, error="Invalid action")

    def _list_config(self) -> CommandResult:
        """List all configuration settings."""
        # TODO: Implement configuration listing
        return CommandResult(success=True, output="Configuration listing not implemented yet")

    def _get_config(self, key: str) -> CommandResult:
        """Get a configuration value."""
        # TODO: Implement configuration retrieval
        return CommandResult(success=True, output=f"Getting configuration for {key} not implemented yet")

    def _set_config(self, key: str, value: str) -> CommandResult:
        """Set a configuration value."""
        # TODO: Implement configuration setting
        return CommandResult(success=True, output=f"Setting configuration {key}={value} not implemented yet")

def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the MCPS CLI."""
    if args is None:
        args = sys.argv[1:]

    if not args:
        # Show help if no arguments provided
        command = HelpCommand()
        result = command.execute(CommandContext(
            args=[],
            options={},
            env=dict(os.environ),
            working_dir=os.getcwd()
        ))
        print(result.output if result.success else result.error)
        return 0 if result.success else 1

    command_name = args[0]
    command_args = args[1:]

    # Map of available commands
    commands = {
        "help": HelpCommand(),
        "version": VersionCommand(),
        "config": ConfigCommand()
    }
    
    try:
        from mcps.cli.commands.agent.main import AgentCommand
        commands["agent"] = AgentCommand()
    except ImportError:
        pass

    if command_name not in commands:
        print(f"Unknown command: {command_name}")
        print("Use 'mcps help' to see available commands")
        return 1

    command = commands[command_name]
    result = command.execute(CommandContext(
        args=command_args,
        options={},
        env=dict(os.environ),
        working_dir=os.getcwd()
    ))
    print(result.output if result.success else result.error)
    return 0 if result.success else 1

if __name__ == "__main__":
    sys.exit(main())  