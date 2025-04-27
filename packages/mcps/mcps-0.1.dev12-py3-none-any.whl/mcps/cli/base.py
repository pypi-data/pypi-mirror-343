from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class CommandContext:
    """Command execution context"""
    args: List[str]
    options: Dict[str, Any]
    env: Dict[str, str]
    working_dir: str

@dataclass
class CommandResult:
    """Command execution result"""
    success: bool
    output: Any
    error: Optional[str] = None
    exit_code: int = 0
    metadata: Optional[Dict[str, Any]] = None

class BaseCommand(ABC):
    """Base class for CLI commands"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Command name"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Command description"""
        pass
    
    @property
    @abstractmethod
    def usage(self) -> str:
        """Command usage information"""
        pass
    
    @abstractmethod
    def execute(self, context: CommandContext) -> CommandResult:
        """Execute the command
        
        Args:
            context: Command execution context
            
        Returns:
            Command execution result
        """
        pass
    
    @abstractmethod
    def validate_args(self, args: List[str], options: Dict[str, Any]) -> bool:
        """Validate command arguments
        
        Args:
            args: Command arguments
            options: Command options
            
        Returns:
            True if arguments are valid
        """
        pass

@dataclass
class PluginMetadata:
    """Plugin metadata information"""
    plugin_id: str
    name: str
    version: str
    description: str
    author: str
    commands: List[str]
    dependencies: List[str]
    created_at: datetime
    updated_at: datetime

class BasePlugin(ABC):
    """Base class for CLI plugins"""
    
    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """Plugin metadata"""
        pass
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the plugin"""
        pass
    
    @abstractmethod
    def get_commands(self) -> List[BaseCommand]:
        """Get plugin commands
        
        Returns:
            List of plugin commands
        """
        pass
    
    @abstractmethod
    def validate_dependencies(self) -> bool:
        """Validate plugin dependencies
        
        Returns:
            True if dependencies are satisfied
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up plugin resources"""
        pass

class PluginManager(ABC):
    """Base class for plugin management"""
    
    @abstractmethod
    def load_plugin(self, plugin_path: str) -> BasePlugin:
        """Load a plugin
        
        Args:
            plugin_path: Path to plugin package
            
        Returns:
            Loaded plugin instance
        """
        pass
    
    @abstractmethod
    def unload_plugin(self, plugin_id: str) -> None:
        """Unload a plugin
        
        Args:
            plugin_id: Plugin identifier
        """
        pass
    
    @abstractmethod
    def get_plugin(self, plugin_id: str) -> Optional[BasePlugin]:
        """Get plugin by ID
        
        Args:
            plugin_id: Plugin identifier
            
        Returns:
            Plugin instance if found
        """
        pass
    
    @abstractmethod
    def list_plugins(self) -> List[PluginMetadata]:
        """List loaded plugins
        
        Returns:
            List of plugin metadata
        """
        pass 