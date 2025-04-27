from typing import Dict, Any, List, Optional, Type
import importlib.util
import os
import sys
from datetime import datetime
from ..base import BasePlugin, PluginManager, PluginMetadata, BaseCommand

class DefaultPluginManager(PluginManager):
    """Default implementation of plugin management"""
    
    def __init__(self, plugin_dir: Optional[str] = None):
        """Initialize plugin manager
        
        Args:
            plugin_dir: Optional directory to load plugins from
        """
        self._plugins: Dict[str, BasePlugin] = {}
        self._plugin_dir = plugin_dir or os.path.join(os.path.expanduser("~"), ".mcps", "plugins")
        
        # Create plugin directory if it doesn't exist
        os.makedirs(self._plugin_dir, exist_ok=True)
        
        # Add plugin directory to Python path
        if self._plugin_dir not in sys.path:
            sys.path.append(self._plugin_dir)
    
    def load_plugin(self, plugin_path: str) -> BasePlugin:
        """Load a plugin
        
        Args:
            plugin_path: Path to plugin package
            
        Returns:
            Loaded plugin instance
        """
        # Check if plugin is already loaded
        plugin_id = os.path.basename(plugin_path)
        if plugin_id in self._plugins:
            return self._plugins[plugin_id]
        
        # Load plugin module
        spec = importlib.util.spec_from_file_location(
            plugin_id,
            os.path.join(plugin_path, "__init__.py")
        )
        if not spec or not spec.loader:
            raise ImportError(f"Could not load plugin from {plugin_path}")
            
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find plugin class
        plugin_class = None
        for item in dir(module):
            obj = getattr(module, item)
            if isinstance(obj, type) and issubclass(obj, BasePlugin) and obj != BasePlugin:
                plugin_class = obj
                break
                
        if not plugin_class:
            raise ImportError(f"No plugin class found in {plugin_path}")
        
        # Instantiate plugin
        plugin = plugin_class()
        
        # Initialize plugin
        plugin.initialize()
        
        # Store plugin
        self._plugins[plugin_id] = plugin
        
        return plugin
    
    def unload_plugin(self, plugin_id: str) -> None:
        """Unload a plugin
        
        Args:
            plugin_id: Plugin identifier
        """
        if plugin_id in self._plugins:
            plugin = self._plugins[plugin_id]
            plugin.cleanup()
            del self._plugins[plugin_id]
    
    def get_plugin(self, plugin_id: str) -> Optional[BasePlugin]:
        """Get plugin by ID
        
        Args:
            plugin_id: Plugin identifier
            
        Returns:
            Plugin instance if found
        """
        return self._plugins.get(plugin_id)
    
    def list_plugins(self) -> List[PluginMetadata]:
        """List loaded plugins
        
        Returns:
            List of plugin metadata
        """
        return [plugin.metadata for plugin in self._plugins.values()]
    
    def discover_plugins(self) -> List[str]:
        """Discover available plugins
        
        Returns:
            List of plugin paths
        """
        plugin_paths = []
        
        # Scan plugin directory
        for item in os.listdir(self._plugin_dir):
            item_path = os.path.join(self._plugin_dir, item)
            if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, "__init__.py")):
                plugin_paths.append(item_path)
        
        return plugin_paths
    
    def load_all_plugins(self) -> None:
        """Load all discovered plugins"""
        for plugin_path in self.discover_plugins():
            try:
                self.load_plugin(plugin_path)
            except Exception as e:
                print(f"Error loading plugin {plugin_path}: {e}")
    
    def get_commands(self) -> List[BaseCommand]:
        """Get all commands from loaded plugins
        
        Returns:
            List of commands
        """
        commands = []
        for plugin in self._plugins.values():
            commands.extend(plugin.get_commands())
        return commands 