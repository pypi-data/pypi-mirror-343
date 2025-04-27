"""Nacos configuration module for MCPS.

This module provides Nacos integration for dynamic configuration management.
"""

import json
import os
import yaml
from typing import Any, Dict, Optional, Callable

from mcps.config.base import BaseConfig
from mcps.core.exceptions.base import ConfigurationException

try:
    import nacos
    import requests.exceptions
    NACOS_AVAILABLE = True
except ImportError:
    NACOS_AVAILABLE = False


class NacosConfig(BaseConfig):
    """Configuration management using Nacos.
    
    This class extends BaseConfig to provide Nacos integration for dynamic configuration.
    """
    
    def __init__(
        self,
        server_addr: str,
        namespace: str,
        data_id: str,
        group: str = "DEFAULT_GROUP",
        username: Optional[str] = None,
        password: Optional[str] = None,
        config_path: Optional[str] = None,
    ):
        """Initialize the Nacos configuration.
        
        Args:
            server_addr: Nacos server address (e.g., "127.0.0.1:8848")
            namespace: Nacos namespace
            data_id: Nacos data ID for configuration
            group: Nacos group name (default: "DEFAULT_GROUP")
            username: Optional username for Nacos authentication
            password: Optional password for Nacos authentication
            config_path: Optional path to a local configuration file (fallback)
        """
        super().__init__(config_path)
        
        if not NACOS_AVAILABLE:
            self.logger.warning("Nacos SDK is not available. Install with: pip install nacos-sdk-python")
            self.client = None
            return
            
        self.server_addr = server_addr
        self.namespace = namespace
        self.data_id = data_id
        self.group = group
        self.username = username
        self.password = password
        
        try:
            self.client = nacos.NacosClient(
                server_addresses=server_addr,
                namespace=namespace,
                username=username,
                password=password
            )
            
            self.load_dynamic_config()
        except Exception as e:
            self.logger.warning(f"Failed to load config from Nacos: {e}")
            self.logger.info("Using local configuration as fallback")
            self.client = None
    
    def load_dynamic_config(self) -> None:
        """Load configuration from Nacos.
        
        This method loads configuration from Nacos and updates the local config.
        If the Nacos configuration is not available, it will log a warning.
        """
        if not self.client:
            self.logger.warning("Nacos client is not available")
            return
            
        try:
            config_str = self.client.get_config(
                data_id=self.data_id,
                group=self.group
            )
            
            if config_str:
                if config_str.strip().startswith('{'):
                    config_dict = json.loads(config_str)
                else:
                    config_dict = yaml.safe_load(config_str)
                
                self.update(config_dict)
            else:
                self.logger.warning(f"No configuration found in Nacos (data_id: {self.data_id}, group: {self.group})")
        
        except yaml.YAMLError as e:
            self.logger.error(f"Invalid YAML configuration from Nacos: {e}")
            self.logger.error(f"Raw config content: {config_str}")
            raise ConfigurationException(f"Invalid YAML configuration from Nacos: {e}")
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON configuration from Nacos: {e}")
            self.logger.error(f"Raw config content: {config_str}")
            raise ConfigurationException(f"Invalid JSON configuration from Nacos: {e}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to connect to Nacos server: {e}")
            raise ConfigurationException(f"Failed to connect to Nacos server: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error loading config from Nacos: {e}")
            raise ConfigurationException(f"Unexpected error loading config from Nacos: {e}")
    
    def publish_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """Publish configuration to Nacos.
        
        Args:
            config: Optional configuration dictionary to publish.
                   If None, the current configuration will be published.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.client:
            self.logger.warning("Nacos client is not available")
            return False
            
        try:
            config_dict = config if config is not None else self._config
            
            config_str = json.dumps(config_dict)
            
            result = self.client.publish_config(
                data_id=self.data_id,
                group=self.group,
                content=config_str
            )
            
            if result:
                self.logger.info(f"Configuration published to Nacos (data_id: {self.data_id}, group: {self.group})")
            else:
                self.logger.warning(f"Failed to publish configuration to Nacos")
            
            return bool(result)
        
        except Exception as e:
            self.logger.error(f"Error publishing config to Nacos: {e}")
            return False
    
    def add_listener(self, callback: Callable[[str], None]) -> None:
        """Add a listener for configuration changes in Nacos.
        
        Args:
            callback: Callback function that will be called when configuration changes
        """
        if not self.client:
            self.logger.warning("Nacos client is not available")
            return
            
        try:
            self.client.add_config_watcher(
                data_id=self.data_id,
                group=self.group,
                cb=callback
            )
            self.logger.info(f"Listener added for Nacos configuration changes")
        except Exception as e:
            self.logger.error(f"Failed to add Nacos configuration listener: {e}")
    
    def remove_listener(self) -> None:
        """Remove the listener for configuration changes in Nacos.
        """
        if not self.client:
            self.logger.warning("Nacos client is not available")
            return
            
        try:
            self.client.remove_config_watcher(
                data_id=self.data_id,
                group=self.group
            )
            self.logger.info(f"Listener removed for Nacos configuration changes")
        except Exception as e:
            self.logger.error(f"Failed to remove Nacos configuration listener: {e}")
    
    def get_server_status(self) -> bool:
        """Check if the Nacos server is available.
        
        Returns:
            bool: True if the server is available, False otherwise
        """
        if not self.client:
            return False
            
        try:
            return self.client.is_valid()
        except Exception:
            return False
