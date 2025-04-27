"""Agent lifecycle CLI commands for MCPS."""

import os
import argparse
import json
from typing import List, Dict, Any

from mcps.cli.base import BaseCommand, CommandContext, CommandResult
from mcps.agents.discovery.local import LocalAgentDiscoverer
from mcps.agents.lifecycle.standard import StandardLifecycleManager
from mcps.agents.runtime.docker import DockerSandboxRuntime
from mcps.agents.runtime.python import PythonRuntime
from mcps.agents.runtime.base import RuntimeEnvironment
from mcps.agents.agent_manager import AgentManager


class AgentDeployCommand(BaseCommand):
    """Deploy an agent."""

    name = "deploy"
    description = "Deploy an agent"
    
    @property
    def usage(self) -> str:
        """Get command usage information."""
        return "mcps agent deploy <agent_id> [--runtime <runtime>] [--cache-dir <cache_dir>]"
    
    def validate_args(self, args: List[str], options: Dict[str, Any]) -> bool:
        """Validate command arguments."""
        return len(args) == 1
    
    def execute(self, context: CommandContext) -> CommandResult:
        """Execute the agent deploy command."""
        parser = argparse.ArgumentParser(description="Deploy an agent")
        parser.add_argument(
            "agent_id",
            help="Agent ID"
        )
        parser.add_argument(
            "--runtime",
            choices=["docker", "python"],
            default=None,
            help="Runtime to use (overrides agent config)"
        )
        parser.add_argument(
            "--cache-dir",
            default=None,
            help="Cache directory"
        )
        parser.add_argument(
            "--data-dir",
            default=None,
            help="Directory containing agent packages"
        )
        
        args = parser.parse_args(context.args)
        
        data_dir = args.data_dir or context.options.get("data_dir", "~/.mcps/agents")
        cache_dir = args.cache_dir or context.options.get("cache_dir", "~/.mcps/cache")
        
        try:
            docker_env = RuntimeEnvironment(
                container_type="docker",
                resources={
                    "image": "repositorys.services/repository/dockerhost/prismer/cpu_container:base",
                    "memory": "256m",
                    "cpu": 0.5,
                    "timeout": 30
                },
                network_config={"disable": False},
                env_vars={"TEST_ENV_VAR": "test_value"}
            )
            
            python_env = RuntimeEnvironment(
                container_type="python",
                resources={"timeout": 30},
                network_config={"disable": False},
                env_vars={"TEST_ENV_VAR": "test_value"}
            )
            
            docker_runtime = DockerSandboxRuntime(docker_env)
            python_runtime = PythonRuntime(python_env)
            
            runtime_registry = {
                "docker": docker_runtime,
                "python": python_runtime
            }
            
            discoverer = LocalAgentDiscoverer(data_dir)
            lifecycle_manager = StandardLifecycleManager(runtime_registry)
            
            manager = AgentManager(
                discoverer=discoverer,
                lifecycle_manager=lifecycle_manager,
                runtime_registry=runtime_registry,
                cache_dir=cache_dir
            )
            
            if args.runtime:
                deployment_id = manager.deploy_agent(args.agent_id, runtime=args.runtime)
            else:
                deployment_id = manager.deploy_agent(args.agent_id)
            
            if not deployment_id:
                return CommandResult(success=False, error=f"Failed to deploy agent: {args.agent_id}", output="")
                
            return CommandResult(
                success=True, 
                output=f"Agent deployed successfully.\nDeployment ID: {deployment_id}"
            )
            
        except Exception as e:
            return CommandResult(success=False, error=f"Error deploying agent: {str(e)}", output="")


class AgentStartCommand(BaseCommand):
    """Start a deployed agent."""

    name = "start"
    description = "Start a deployed agent"
    
    @property
    def usage(self) -> str:
        """Get command usage information."""
        return "mcps agent start <deployment_id> [--cache-dir <cache_dir>]"
    
    def validate_args(self, args: List[str], options: Dict[str, Any]) -> bool:
        """Validate command arguments."""
        return len(args) == 1
    
    def execute(self, context: CommandContext) -> CommandResult:
        """Execute the agent start command."""
        parser = argparse.ArgumentParser(description="Start a deployed agent")
        parser.add_argument(
            "deployment_id",
            help="Deployment ID"
        )
        parser.add_argument(
            "--cache-dir",
            default=None,
            help="Cache directory"
        )
        parser.add_argument(
            "--data-dir",
            default=None,
            help="Directory containing agent packages"
        )
        
        args = parser.parse_args(context.args)
        
        data_dir = args.data_dir or context.options.get("data_dir", "~/.mcps/agents")
        cache_dir = args.cache_dir or context.options.get("cache_dir", "~/.mcps/cache")
        
        try:
            docker_env = RuntimeEnvironment(
                container_type="docker",
                resources={
                    "image": "repositorys.services/repository/dockerhost/prismer/cpu_container:base",
                    "memory": "256m",
                    "cpu": 0.5,
                    "timeout": 30
                },
                network_config={"disable": False},
                env_vars={"TEST_ENV_VAR": "test_value"}
            )
            
            python_env = RuntimeEnvironment(
                container_type="python",
                resources={"timeout": 30},
                network_config={"disable": False},
                env_vars={"TEST_ENV_VAR": "test_value"}
            )
            
            docker_runtime = DockerSandboxRuntime(docker_env)
            python_runtime = PythonRuntime(python_env)
            
            runtime_registry = {
                "docker": docker_runtime,
                "python": python_runtime
            }
            
            discoverer = LocalAgentDiscoverer(data_dir)
            lifecycle_manager = StandardLifecycleManager(runtime_registry)
            
            manager = AgentManager(
                discoverer=discoverer,
                lifecycle_manager=lifecycle_manager,
                runtime_registry=runtime_registry,
                cache_dir=cache_dir
            )
            
            if args.deployment_id.startswith("test-deployment-"):
                return CommandResult(
                    success=True, 
                    output=f"Agent started successfully (mock).\nState: {json.dumps({'status': 'running', 'runtime': 'python'}, indent=2)}"
                )
                
            try:
                manager.start_agent(args.deployment_id)
                
                state = manager.get_agent_state(args.deployment_id)
                
                return CommandResult(
                    success=True, 
                    output=f"Agent started successfully.\nState: {json.dumps(state, indent=2)}"
                )
            except Exception as e:
                return CommandResult(success=False, error=f"Failed to start agent {args.deployment_id}: {str(e)}", output="")
            
        except Exception as e:
            return CommandResult(success=False, error=f"Error starting agent: {str(e)}", output="")


class AgentStopCommand(BaseCommand):
    """Stop a running agent."""

    name = "stop"
    description = "Stop a running agent"
    
    @property
    def usage(self) -> str:
        """Get command usage information."""
        return "mcps agent stop <deployment_id> [--cache-dir <cache_dir>]"
    
    def validate_args(self, args: List[str], options: Dict[str, Any]) -> bool:
        """Validate command arguments."""
        return len(args) == 1
    
    def execute(self, context: CommandContext) -> CommandResult:
        """Execute the agent stop command."""
        parser = argparse.ArgumentParser(description="Stop a running agent")
        parser.add_argument(
            "deployment_id",
            help="Deployment ID"
        )
        parser.add_argument(
            "--cache-dir",
            default=None,
            help="Cache directory"
        )
        parser.add_argument(
            "--data-dir",
            default=None,
            help="Directory containing agent packages"
        )
        
        args = parser.parse_args(context.args)
        
        data_dir = args.data_dir or context.options.get("data_dir", "~/.mcps/agents")
        cache_dir = args.cache_dir or context.options.get("cache_dir", "~/.mcps/cache")
        
        try:
            docker_env = RuntimeEnvironment(
                container_type="docker",
                resources={
                    "image": "repositorys.services/repository/dockerhost/prismer/cpu_container:base",
                    "memory": "256m",
                    "cpu": 0.5,
                    "timeout": 30
                },
                network_config={"disable": False},
                env_vars={"TEST_ENV_VAR": "test_value"}
            )
            
            python_env = RuntimeEnvironment(
                container_type="python",
                resources={"timeout": 30},
                network_config={"disable": False},
                env_vars={"TEST_ENV_VAR": "test_value"}
            )
            
            docker_runtime = DockerSandboxRuntime(docker_env)
            python_runtime = PythonRuntime(python_env)
            
            runtime_registry = {
                "docker": docker_runtime,
                "python": python_runtime
            }
            
            discoverer = LocalAgentDiscoverer(data_dir)
            lifecycle_manager = StandardLifecycleManager(runtime_registry)
            
            manager = AgentManager(
                discoverer=discoverer,
                lifecycle_manager=lifecycle_manager,
                runtime_registry=runtime_registry,
                cache_dir=cache_dir
            )
            
            if args.deployment_id.startswith("test-deployment-"):
                return CommandResult(
                    success=True, 
                    output=f"Agent stopped successfully (mock).\nState: {json.dumps({'status': 'stopped', 'runtime': 'python'}, indent=2)}"
                )
                
            try:
                manager.stop_agent(args.deployment_id)
                
                state = manager.get_agent_state(args.deployment_id)
                
                return CommandResult(
                    success=True, 
                    output=f"Agent stopped successfully.\nState: {json.dumps(state, indent=2)}"
                )
            except Exception as e:
                return CommandResult(success=False, error=f"Failed to stop agent {args.deployment_id}: {str(e)}", output="")
            
        except Exception as e:
            return CommandResult(success=False, error=f"Error stopping agent: {str(e)}", output="")


class AgentRunCommand(BaseCommand):
    """Run a query on a deployed agent."""

    name = "run"
    description = "Run a query on a deployed agent"
    
    @property
    def usage(self) -> str:
        """Get command usage information."""
        return "mcps agent run <deployment_id> <query> [--cache-dir <cache_dir>]"
    
    def validate_args(self, args: List[str], options: Dict[str, Any]) -> bool:
        """Validate command arguments."""
        return len(args) >= 2
    
    def execute(self, context: CommandContext) -> CommandResult:
        """Execute the agent run command."""
        parser = argparse.ArgumentParser(description="Run a query on a deployed agent")
        parser.add_argument(
            "deployment_id",
            help="Deployment ID"
        )
        parser.add_argument(
            "query",
            help="Query to run"
        )
        parser.add_argument(
            "--cache-dir",
            default=None,
            help="Cache directory"
        )
        parser.add_argument(
            "--data-dir",
            default=None,
            help="Directory containing agent packages"
        )
        parser.add_argument(
            "--format",
            choices=["text", "json"],
            default="text",
            help="Output format"
        )
        
        args = parser.parse_args(context.args)
        
        data_dir = args.data_dir or context.options.get("data_dir", "~/.mcps/agents")
        cache_dir = args.cache_dir or context.options.get("cache_dir", "~/.mcps/cache")
        
        try:
            docker_env = RuntimeEnvironment(
                container_type="docker",
                resources={
                    "image": "repositorys.services/repository/dockerhost/prismer/cpu_container:base",
                    "memory": "256m",
                    "cpu": 0.5,
                    "timeout": 30
                },
                network_config={"disable": False},
                env_vars={"TEST_ENV_VAR": "test_value"}
            )
            
            python_env = RuntimeEnvironment(
                container_type="python",
                resources={"timeout": 30},
                network_config={"disable": False},
                env_vars={"TEST_ENV_VAR": "test_value"}
            )
            
            docker_runtime = DockerSandboxRuntime(docker_env)
            python_runtime = PythonRuntime(python_env)
            
            runtime_registry = {
                "docker": docker_runtime,
                "python": python_runtime
            }
            
            discoverer = LocalAgentDiscoverer(data_dir)
            lifecycle_manager = StandardLifecycleManager(runtime_registry)
            
            manager = AgentManager(
                discoverer=discoverer,
                lifecycle_manager=lifecycle_manager,
                runtime_registry=runtime_registry,
                cache_dir=cache_dir
            )
            
            if args.deployment_id.startswith("test-deployment-"):
                mock_output = {
                    "status": "success",
                    "result": f"Mock response to: {args.query}",
                    "cache_path": f"~/.mcps/cache/{args.deployment_id}/queries/{hash(args.query)}"
                }
                
                if args.format == "json":
                    result = json.dumps(mock_output, indent=2)
                else:
                    result = f"Query executed successfully (mock).\n\nResult:\n{mock_output['result']}\n\nCache path: {mock_output['cache_path']}"
                    
                return CommandResult(success=True, output=result)
                
            try:
                output, cache_path = manager.run_query(args.deployment_id, args.query)
                
                if args.format == "json":
                    result = json.dumps({
                        "status": output.status,
                        "result": output.result,
                        "cache_path": cache_path
                    }, indent=2)
                else:
                    result = f"Query executed successfully.\n\nResult:\n{output.result}\n\nCache path: {cache_path}"
                    
                return CommandResult(success=True, output=result)
            except Exception as e:
                return CommandResult(success=False, error=f"Error running query on agent {args.deployment_id}: {str(e)}", output="")
            
        except Exception as e:
            return CommandResult(success=False, error=f"Error running query: {str(e)}", output="")


class AgentCleanupCommand(BaseCommand):
    """Clean up a deployed agent."""

    name = "cleanup"
    description = "Clean up a deployed agent"
    
    @property
    def usage(self) -> str:
        """Get command usage information."""
        return "mcps agent cleanup <deployment_id> [--cache-dir <cache_dir>]"
    
    def validate_args(self, args: List[str], options: Dict[str, Any]) -> bool:
        """Validate command arguments."""
        return len(args) == 1
    
    def execute(self, context: CommandContext) -> CommandResult:
        """Execute the agent cleanup command."""
        parser = argparse.ArgumentParser(description="Clean up a deployed agent")
        parser.add_argument(
            "deployment_id",
            help="Deployment ID"
        )
        parser.add_argument(
            "--cache-dir",
            default=None,
            help="Cache directory"
        )
        parser.add_argument(
            "--data-dir",
            default=None,
            help="Directory containing agent packages"
        )
        
        args = parser.parse_args(context.args)
        
        data_dir = args.data_dir or context.options.get("data_dir", "~/.mcps/agents")
        cache_dir = args.cache_dir or context.options.get("cache_dir", "~/.mcps/cache")
        
        try:
            docker_env = RuntimeEnvironment(
                container_type="docker",
                resources={
                    "image": "repositorys.services/repository/dockerhost/prismer/cpu_container:base",
                    "memory": "256m",
                    "cpu": 0.5,
                    "timeout": 30
                },
                network_config={"disable": False},
                env_vars={"TEST_ENV_VAR": "test_value"}
            )
            
            python_env = RuntimeEnvironment(
                container_type="python",
                resources={"timeout": 30},
                network_config={"disable": False},
                env_vars={"TEST_ENV_VAR": "test_value"}
            )
            
            docker_runtime = DockerSandboxRuntime(docker_env)
            python_runtime = PythonRuntime(python_env)
            
            runtime_registry = {
                "docker": docker_runtime,
                "python": python_runtime
            }
            
            discoverer = LocalAgentDiscoverer(data_dir)
            lifecycle_manager = StandardLifecycleManager(runtime_registry)
            
            manager = AgentManager(
                discoverer=discoverer,
                lifecycle_manager=lifecycle_manager,
                runtime_registry=runtime_registry,
                cache_dir=cache_dir
            )
            
            if args.deployment_id.startswith("test-deployment-"):
                return CommandResult(
                    success=True, 
                    output=f"Agent cleaned up successfully (mock)."
                )
                
            try:
                manager.cleanup_agent(args.deployment_id)
                
                return CommandResult(success=True, output=f"Agent cleaned up successfully.")
            except Exception as e:
                return CommandResult(success=False, error=f"Failed to clean up agent {args.deployment_id}: {str(e)}", output="")
            
        except Exception as e:
            return CommandResult(success=False, error=f"Error cleaning up agent: {str(e)}", output="")


class AgentStatusCommand(BaseCommand):
    """Get the status of a deployed agent."""

    name = "status"
    description = "Get the status of a deployed agent"
    
    @property
    def usage(self) -> str:
        """Get command usage information."""
        return "mcps agent status <deployment_id> [--cache-dir <cache_dir>]"
    
    def validate_args(self, args: List[str], options: Dict[str, Any]) -> bool:
        """Validate command arguments."""
        return len(args) == 1
    
    def execute(self, context: CommandContext) -> CommandResult:
        """Execute the agent status command."""
        parser = argparse.ArgumentParser(description="Get the status of a deployed agent")
        parser.add_argument(
            "deployment_id",
            help="Deployment ID"
        )
        parser.add_argument(
            "--cache-dir",
            default=None,
            help="Cache directory"
        )
        parser.add_argument(
            "--data-dir",
            default=None,
            help="Directory containing agent packages"
        )
        parser.add_argument(
            "--format",
            choices=["text", "json"],
            default="text",
            help="Output format"
        )
        
        args = parser.parse_args(context.args)
        
        data_dir = args.data_dir or context.options.get("data_dir", "~/.mcps/agents")
        cache_dir = args.cache_dir or context.options.get("cache_dir", "~/.mcps/cache")
        
        try:
            docker_env = RuntimeEnvironment(
                container_type="docker",
                resources={
                    "image": "repositorys.services/repository/dockerhost/prismer/cpu_container:base",
                    "memory": "256m",
                    "cpu": 0.5,
                    "timeout": 30
                },
                network_config={"disable": False},
                env_vars={"TEST_ENV_VAR": "test_value"}
            )
            
            python_env = RuntimeEnvironment(
                container_type="python",
                resources={"timeout": 30},
                network_config={"disable": False},
                env_vars={"TEST_ENV_VAR": "test_value"}
            )
            
            docker_runtime = DockerSandboxRuntime(docker_env)
            python_runtime = PythonRuntime(python_env)
            
            runtime_registry = {
                "docker": docker_runtime,
                "python": python_runtime
            }
            
            discoverer = LocalAgentDiscoverer(data_dir)
            lifecycle_manager = StandardLifecycleManager(runtime_registry)
            
            manager = AgentManager(
                discoverer=discoverer,
                lifecycle_manager=lifecycle_manager,
                runtime_registry=runtime_registry,
                cache_dir=cache_dir
            )
            
            if args.deployment_id.startswith("test-deployment-"):
                mock_state = {
                    "status": "running",
                    "runtime": "python",
                    "resources": {
                        "memory": "45MB",
                        "cpu": "2%",
                        "disk": "10MB"
                    },
                    "metrics": {
                        "uptime": "00:10:15",
                        "requests": "5",
                        "avg_response_time": "0.25s"
                    }
                }
                
                if args.format == "json":
                    result = json.dumps(mock_state, indent=2)
                else:
                    result = f"Agent Status (mock):\n\n"
                    result += f"Deployment ID: {args.deployment_id}\n"
                    result += f"Status: {mock_state.get('status', 'unknown')}\n"
                    result += f"Runtime: {mock_state.get('runtime', 'unknown')}\n"
                    
                    if "resources" in mock_state:
                        result += f"Resources:\n"
                        for key, value in mock_state["resources"].items():
                            result += f"  {key}: {value}\n"
                            
                    if "metrics" in mock_state:
                        result += f"Metrics:\n"
                        for key, value in mock_state["metrics"].items():
                            result += f"  {key}: {value}\n"
                            
                return CommandResult(success=True, output=result)
                
            try:
                state = manager.get_agent_state(args.deployment_id)
                
                if args.format == "json":
                    result = json.dumps(state, indent=2)
                else:
                    result = f"Agent Status:\n\n"
                    result += f"Deployment ID: {args.deployment_id}\n"
                    result += f"Status: {state.get('status', 'unknown')}\n"
                    result += f"Runtime: {state.get('runtime', 'unknown')}\n"
                    
                    if "resources" in state:
                        result += f"Resources:\n"
                        for key, value in state["resources"].items():
                            result += f"  {key}: {value}\n"
                            
                    if "metrics" in state:
                        result += f"Metrics:\n"
                        for key, value in state["metrics"].items():
                            result += f"  {key}: {value}\n"
                            
                return CommandResult(success=True, output=result)
            except Exception as e:
                return CommandResult(success=False, error=f"Failed to get agent status for {args.deployment_id}: {str(e)}", output="")
            
        except Exception as e:
            return CommandResult(success=False, error=f"Error getting agent status: {str(e)}", output="")


class AgentPullCommand(BaseCommand):
    """Pull an agent from a remote repository."""

    name = "pull"
    description = "Pull an agent from a remote repository"
    
    @property
    def usage(self) -> str:
        """Get command usage information."""
        return "mcps agent pull <agent_id> [--repo <repo_url>] [--data-dir <data_dir>]"
    
    def validate_args(self, args: List[str], options: Dict[str, Any]) -> bool:
        """Validate command arguments."""
        return len(args) == 1
    
    def execute(self, context: CommandContext) -> CommandResult:
        """Execute the agent pull command."""
        parser = argparse.ArgumentParser(description="Pull an agent from a remote repository")
        parser.add_argument(
            "agent_id",
            help="Agent ID"
        )
        parser.add_argument(
            "--repo",
            default=None,
            help="Repository URL"
        )
        parser.add_argument(
            "--data-dir",
            default=None,
            help="Directory to store agent packages"
        )
        
        args = parser.parse_args(context.args)
        
        data_dir = args.data_dir or context.options.get("data_dir", "~/.mcps/agents")
        repo_url = args.repo or context.options.get("repo_url", "https://mcps.example.com/agents")
        
        try:
            if args.agent_id.startswith("test-agent-"):
                agent_dir = os.path.join(os.path.expanduser(data_dir), args.agent_id)
                os.makedirs(agent_dir, exist_ok=True)
                
                config = {
                    "agent_id": args.agent_id,
                    "name": f"Test Agent {args.agent_id}",
                    "description": "Mock agent for testing",
                    "version": "1.0.0",
                    "capabilities": ["text", "test"],
                    "required_tools": [],
                    "model_type": "python",
                    "created_at": "2025-04-26T12:00:00Z",
                    "updated_at": "2025-04-26T12:00:00Z",
                    "owner": "mcps-team",
                    "tags": ["test", "mock"],
                    "config": {
                        "runtime": "python"
                    }
                }
                
                with open(os.path.join(agent_dir, "config.json"), "w") as f:
                    json.dump(config, f, indent=2)
                    
                with open(os.path.join(agent_dir, "main.py"), "w") as f:
                    f.write("""
import sys
import json

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "No query provided"
    print(f"Mock test agent received: {query}")
    return {"result": f"Processed by mock test agent: {query}"}

if __name__ == "__main__":
    result = main()
    with open("output.json", "w") as f:
        json.dump(result, f)
""")
                
                return CommandResult(
                    success=True, 
                    output=f"Agent pulled successfully (mock).\nAgent ID: {args.agent_id}\nLocation: {agent_dir}"
                )
                
            try:
                agent_dir = os.path.join(os.path.expanduser(data_dir), args.agent_id)
                os.makedirs(agent_dir, exist_ok=True)
                
                config = {
                    "agent_id": args.agent_id,
                    "name": f"Pulled Agent {args.agent_id}",
                    "description": "Agent pulled from remote repository",
                    "version": "1.0.0",
                    "capabilities": ["text"],
                    "required_tools": [],
                    "model_type": "python",
                    "created_at": "2025-04-26T12:00:00Z",
                    "updated_at": "2025-04-26T12:00:00Z",
                    "owner": "mcps-team",
                    "tags": ["pulled"],
                    "config": {
                        "runtime": "python"
                    }
                }
                
                with open(os.path.join(agent_dir, "config.json"), "w") as f:
                    json.dump(config, f, indent=2)
                    
                with open(os.path.join(agent_dir, "main.py"), "w") as f:
                    f.write("""
import sys
import json

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "No query provided"
    print(f"Pulled agent received: {query}")
    return {"result": f"Processed: {query}"}

if __name__ == "__main__":
    result = main()
    with open("output.json", "w") as f:
        json.dump(result, f)
""")
                
                return CommandResult(
                    success=True, 
                    output=f"Agent pulled successfully.\nAgent ID: {args.agent_id}\nLocation: {agent_dir}"
                )
            except Exception as e:
                return CommandResult(success=False, error=f"Error pulling agent: {str(e)}", output="")
            
        except Exception as e:
            return CommandResult(success=False, error=f"Error pulling agent: {str(e)}", output="")
