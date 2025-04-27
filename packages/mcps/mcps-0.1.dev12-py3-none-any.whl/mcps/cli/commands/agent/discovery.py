"""Agent discovery CLI commands for MCPS."""

import argparse
import json
from typing import List, Dict, Any

from mcps.cli.base import BaseCommand, CommandContext, CommandResult
from mcps.agents.discovery.local import LocalAgentDiscoverer


class AgentListCommand(BaseCommand):
    """List available agents."""

    name = "list"
    description = "List available agents"
    
    @property
    def usage(self) -> str:
        """Get command usage information."""
        return "mcps agent list [--filter <filter>] [--capabilities <capabilities>] [--format <format>]"
    
    def validate_args(self, args: List[str], options: Dict[str, Any]) -> bool:
        """Validate command arguments."""
        return True
    
    def execute(self, context: CommandContext) -> CommandResult:
        """Execute the agent list command."""
        parser = argparse.ArgumentParser(description="List available agents")
        parser.add_argument(
            "--filter", 
            help="Filter agents by name or description"
        )
        parser.add_argument(
            "--capabilities",
            help="Filter agents by capabilities (comma-separated)"
        )
        parser.add_argument(
            "--format",
            choices=["text", "json"],
            default="text",
            help="Output format"
        )
        parser.add_argument(
            "--data-dir",
            default=None,
            help="Directory containing agent packages"
        )
        
        args = parser.parse_args(context.args)
        
        data_dir = args.data_dir or context.options.get("data_dir", "~/.mcps/agents")
        discoverer = LocalAgentDiscoverer(data_dir)
        
        agents = discoverer.list_agents()
        
        if args.filter:
            agents = [
                agent for agent in agents 
                if args.filter.lower() in agent.name.lower() or 
                args.filter.lower() in agent.description.lower()
            ]
            
        if args.capabilities:
            capabilities = [cap.strip() for cap in args.capabilities.split(",")]
            agents = [
                agent for agent in agents
                if all(cap in agent.capabilities for cap in capabilities)
            ]
            
        if args.format == "json":
            result = json.dumps([agent.to_dict() for agent in agents], indent=2)
        else:
            if not agents:
                result = "No agents found."
            else:
                result = "Available agents:\n\n"
                for agent in agents:
                    result += f"ID: {agent.agent_id}\n"
                    result += f"Name: {agent.name}\n"
                    result += f"Description: {agent.description}\n"
                    result += f"Version: {agent.version}\n"
                    result += f"Capabilities: {', '.join(agent.capabilities)}\n"
                    result += f"Runtime: {agent.config.get('runtime', 'unknown')}\n"
                    result += "\n"
                    
        return CommandResult(success=True, output=result)


class AgentQueryCommand(BaseCommand):
    """Query for agents using natural language."""

    name = "query"
    description = "Query for agents using natural language"
    
    @property
    def usage(self) -> str:
        """Get command usage information."""
        return "mcps agent query <query> [--top-k <number>] [--format <format>]"
    
    def validate_args(self, args: List[str], options: Dict[str, Any]) -> bool:
        """Validate command arguments."""
        return len(args) >= 1
    
    def execute(self, context: CommandContext) -> CommandResult:
        """Execute the agent query command."""
        parser = argparse.ArgumentParser(description="Query for agents using natural language")
        parser.add_argument(
            "query",
            help="Natural language query"
        )
        parser.add_argument(
            "--top-k",
            type=int,
            default=3,
            help="Number of top matches to return"
        )
        parser.add_argument(
            "--format",
            choices=["text", "json"],
            default="text",
            help="Output format"
        )
        parser.add_argument(
            "--data-dir",
            default=None,
            help="Directory containing agent packages"
        )
        
        args = parser.parse_args(context.args)
        
        data_dir = args.data_dir or context.options.get("data_dir", "~/.mcps/agents")
        discoverer = LocalAgentDiscoverer(data_dir)
        
        matches = discoverer.find_by_query(args.query, top_k=args.top_k)
        
        if args.format == "json":
            result = json.dumps([
                {
                    "agent": match.agent.to_dict(),
                    "score": match.score
                } for match in matches
            ], indent=2)
        else:
            if not matches:
                result = "No matching agents found."
            else:
                result = f"Top {len(matches)} matches for query: '{args.query}'\n\n"
                for i, match in enumerate(matches):
                    agent = match.agent
                    result += f"Match {i+1} (score: {match.confidence:.4f}):\n"
                    result += f"ID: {agent.agent_id}\n"
                    result += f"Name: {agent.name}\n"
                    result += f"Description: {agent.description}\n"
                    result += f"Version: {agent.version}\n"
                    result += f"Capabilities: {', '.join(agent.capabilities)}\n"
                    result += f"Runtime: {agent.config.get('runtime', 'unknown')}\n"
                    result += "\n"
                    
        return CommandResult(success=True, output=result)


class AgentCapabilitiesCommand(BaseCommand):
    """Find agents by capabilities."""

    name = "capabilities"
    description = "Find agents by capabilities"
    
    @property
    def usage(self) -> str:
        """Get command usage information."""
        return "mcps agent capabilities <capability1,capability2,...> [--format <format>]"
    
    def validate_args(self, args: List[str], options: Dict[str, Any]) -> bool:
        """Validate command arguments."""
        return len(args) >= 1
    
    def execute(self, context: CommandContext) -> CommandResult:
        """Execute the agent capabilities command."""
        parser = argparse.ArgumentParser(description="Find agents by capabilities")
        parser.add_argument(
            "capabilities",
            help="Comma-separated list of capabilities"
        )
        parser.add_argument(
            "--format",
            choices=["text", "json"],
            default="text",
            help="Output format"
        )
        parser.add_argument(
            "--data-dir",
            default=None,
            help="Directory containing agent packages"
        )
        
        args = parser.parse_args(context.args)
        
        data_dir = args.data_dir or context.options.get("data_dir", "~/.mcps/agents")
        discoverer = LocalAgentDiscoverer(data_dir)
        
        capabilities = [cap.strip() for cap in args.capabilities.split(",")]
        
        matches = discoverer.find_by_capabilities(capabilities)
        
        if args.format == "json":
            result = json.dumps([
                {
                    "agent": match.agent.to_dict(),
                    "score": match.score
                } for match in matches
            ], indent=2)
        else:
            if not matches:
                result = f"No agents found with capabilities: {', '.join(capabilities)}"
            else:
                result = f"Agents with capabilities: {', '.join(capabilities)}\n\n"
                for i, match in enumerate(matches):
                    agent = match.agent
                    result += f"Match {i+1} (score: {match.confidence:.4f}):\n"
                    result += f"ID: {agent.agent_id}\n"
                    result += f"Name: {agent.name}\n"
                    result += f"Description: {agent.description}\n"
                    result += f"Version: {agent.version}\n"
                    result += f"Capabilities: {', '.join(agent.capabilities)}\n"
                    result += f"Runtime: {agent.config.get('runtime', 'unknown')}\n"
                    result += "\n"
                    
        return CommandResult(success=True, output=result)


class AgentInfoCommand(BaseCommand):
    """Get detailed information about an agent."""

    name = "info"
    description = "Get detailed information about an agent"
    
    @property
    def usage(self) -> str:
        """Get command usage information."""
        return "mcps agent info <agent_id> [--format <format>]"
    
    def validate_args(self, args: List[str], options: Dict[str, Any]) -> bool:
        """Validate command arguments."""
        return len(args) == 1
    
    def execute(self, context: CommandContext) -> CommandResult:
        """Execute the agent info command."""
        parser = argparse.ArgumentParser(description="Get detailed information about an agent")
        parser.add_argument(
            "agent_id",
            help="Agent ID"
        )
        parser.add_argument(
            "--format",
            choices=["text", "json"],
            default="text",
            help="Output format"
        )
        parser.add_argument(
            "--data-dir",
            default=None,
            help="Directory containing agent packages"
        )
        
        args = parser.parse_args(context.args)
        
        data_dir = args.data_dir or context.options.get("data_dir", "~/.mcps/agents")
        discoverer = LocalAgentDiscoverer(data_dir)
        
        try:
            agent = discoverer.get_agent(args.agent_id)
        except Exception as e:
            return CommandResult(success=False, error=f"Error getting agent: {str(e)}", output="")
            
        if not agent:
            return CommandResult(success=False, error=f"Agent not found: {args.agent_id}", output="")
            
        if args.format == "json":
            result = json.dumps(agent.to_dict(), indent=2)
        else:
            result = f"Agent Information:\n\n"
            result += f"ID: {agent.agent_id}\n"
            result += f"Name: {agent.name}\n"
            result += f"Description: {agent.description}\n"
            result += f"Version: {agent.version}\n"
            result += f"Capabilities: {', '.join(agent.capabilities)}\n"
            result += f"Required Tools: {', '.join(agent.required_tools)}\n"
            result += f"Model Type: {agent.model_type}\n"
            result += f"Created At: {agent.created_at}\n"
            result += f"Updated At: {agent.updated_at}\n"
            result += f"Owner: {agent.owner}\n"
            result += f"Tags: {', '.join(agent.tags)}\n"
            result += f"Runtime: {agent.config.get('runtime', 'unknown')}\n"
            
            if "protocol" in agent.config:
                result += f"Protocol: {agent.config['protocol']}\n"
                
            if "port" in agent.config:
                result += f"Port: {agent.config['port']}\n"
                
        return CommandResult(success=True, output=result)
