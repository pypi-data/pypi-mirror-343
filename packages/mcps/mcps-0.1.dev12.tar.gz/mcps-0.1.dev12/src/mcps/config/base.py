"""Base configuration module for MCPS.

This module provides a base configuration class that can be extended
by different configuration backends.
"""

import os
import logging
import json
import yaml
from typing import Dict, Any, Optional


class BaseConfig:
    """Base configuration class.
    
    This class provides basic configuration functionality including
    loading from a file, accessing configuration values, and updating
    the configuration.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize base configuration.
        
        Args:
            config_path: Optional path to a configuration file
        """
        self._config = {}
        self.logger = logging.getLogger(self.__class__.__name__)
        
        if config_path and os.path.exists(config_path):
            self.load_file(config_path)
    
    def load_file(self, config_path: str) -> None:
        """Load configuration from a file.
        
        Args:
            config_path: Path to configuration file
        """
        try:
            ext = os.path.splitext(config_path)[1].lower()
            with open(config_path, 'r') as f:
                if ext == '.json':
                    self._config = json.load(f)
                elif ext in ('.yaml', '.yml'):
                    self._config = yaml.safe_load(f)
                else:
                    self.logger.warning(f"Unsupported file extension: {ext}")
            self.logger.info(f"Loaded configuration from {config_path}")
        except Exception as e:
            self.logger.error(f"Failed to load configuration from {config_path}: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key is not found
            
        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value
    
    def update(self, config: Dict[str, Any]) -> None:
        """Update configuration with a dictionary.
        
        Args:
            config: Dictionary with configuration values
        """
        self._config.update(config)
    
    def save(self, config_path: str) -> bool:
        """Save configuration to a file.
        
        Args:
            config_path: Path to save the configuration to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            ext = os.path.splitext(config_path)[1].lower()
            with open(config_path, 'w') as f:
                if ext == '.json':
                    json.dump(self._config, f, indent=2)
                elif ext in ('.yaml', '.yml'):
                    yaml.dump(self._config, f)
                else:
                    self.logger.warning(f"Unsupported file extension: {ext}")
                    return False
            self.logger.info(f"Saved configuration to {config_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save configuration to {config_path}: {e}")
            return False
    
    def __getitem__(self, key: str) -> Any:
        """Get a configuration value using dictionary syntax.
        
        Args:
            key: Configuration key
            
        Returns:
            Configuration value
            
        Raises:
            KeyError: If key is not found
        """
        return self._config[key]
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Set a configuration value using dictionary syntax.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value
    
    def __contains__(self, key: str) -> bool:
        """Check if a key exists in the configuration.
        
        Args:
            key: Configuration key
            
        Returns:
            True if key exists, False otherwise
        """
        return key in self._config
