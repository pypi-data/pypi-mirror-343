"""Main agent CLI command for MCPS."""

import argparse
from typing import List, Dict, Any

from mcps.cli.base import BaseCommand, CommandContext, CommandResult
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


class AgentCommand(BaseCommand):
    """Manage MCPS agents."""

    name = "agent"
    description = "Manage MCPS agents"
    
    @property
    def usage(self) -> str:
        """Get command usage information."""
        return "mcps agent <subcommand> [options]"
    
    def validate_args(self, args: List[str], options: Dict[str, Any]) -> bool:
        """Validate command arguments."""
        return len(args) >= 1
    
    def execute(self, context: CommandContext) -> CommandResult:
        """Execute the agent command."""
        parser = argparse.ArgumentParser(description="Manage MCPS agents")
        parser.add_argument(
            "subcommand",
            help="Subcommand to execute"
        )
        
        try:
            args = parser.parse_args(context.args[:1])
        except SystemExit:
            return CommandResult(success=False, error="Invalid subcommand", output="")
            
        subcommand = args.subcommand
        subcommand_args = context.args[1:]
        
        subcommands = {
            "list": AgentListCommand(),
            "query": AgentQueryCommand(),
            "capabilities": AgentCapabilitiesCommand(),
            "info": AgentInfoCommand(),
            
            "deploy": AgentDeployCommand(),
            "start": AgentStartCommand(),
            "stop": AgentStopCommand(),
            "run": AgentRunCommand(),
            "cleanup": AgentCleanupCommand(),
            "status": AgentStatusCommand(),
            "pull": AgentPullCommand()
        }
        
        if subcommand not in subcommands:
            return CommandResult(
                success=False, 
                error=f"Unknown subcommand: {subcommand}. Available subcommands: {', '.join(subcommands.keys())}",
                output=""
            )
            
        subcommand_context = CommandContext(
            args=subcommand_args,
            options=context.options,
            env=context.env,
            working_dir=context.working_dir
        )
        
        return subcommands[subcommand].execute(subcommand_context)
