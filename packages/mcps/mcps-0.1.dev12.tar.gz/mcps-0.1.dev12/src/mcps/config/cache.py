"""Global cache configuration and management for MCPS."""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class CacheManager:
    """Global cache manager for MCPS."""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize cache manager.
        
        Args:
            cache_dir: Optional custom cache directory. Defaults to ~/.mcps
        """
        self.cache_dir = Path(cache_dir or os.path.expanduser("~/.mcps"))
        self._ensure_cache_structure()
        
    def _ensure_cache_structure(self) -> None:
        """Ensure cache directory structure exists."""
        directories = [
            self.cache_dir,
            self.cache_dir / "config",
            self.cache_dir / "temp",
            self.cache_dir / "agents",
            self.cache_dir / "services",
            self.cache_dir / "logs",
            self.cache_dir / "messages"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
        logger.info(f"Cache directory structure ensured at {self.cache_dir}")
        
    def get_config_path(self, config_name: str) -> Path:
        """Get path for a configuration file.
        
        Args:
            config_name: Name of the configuration
            
        Returns:
            Path to the configuration file
        """
        return self.cache_dir / "config" / f"{config_name}.json"
        
    def save_config(self, config_name: str, config_data: Dict[str, Any]) -> None:
        """Save configuration data.
        
        Args:
            config_name: Name of the configuration
            config_data: Configuration data to save
        """
        config_path = self.get_config_path(config_name)
        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=2)
        logger.info(f"Saved configuration to {config_path}")
        
    def load_config(self, config_name: str) -> Dict[str, Any]:
        """Load configuration data.
        
        Args:
            config_name: Name of the configuration
            
        Returns:
            Configuration data
        """
        config_path = self.get_config_path(config_name)
        if not config_path.exists():
            return {}
            
        with open(config_path, "r") as f:
            return json.load(f)
            
    def get_agent_cache_dir(self, agent_id: str) -> Path:
        """Get cache directory for an agent.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Path to agent cache directory
        """
        agent_dir = self.cache_dir / "agents" / agent_id
        agent_dir.mkdir(parents=True, exist_ok=True)
        return agent_dir
        
    def get_service_cache_dir(self, service_id: str) -> Path:
        """Get cache directory for a service.
        
        Args:
            service_id: Service identifier
            
        Returns:
            Path to service cache directory
        """
        service_dir = self.cache_dir / "services" / service_id
        service_dir.mkdir(parents=True, exist_ok=True)
        return service_dir
        
    def get_temp_dir(self) -> Path:
        """Get temporary directory.
        
        Returns:
            Path to temporary directory
        """
        return self.cache_dir / "temp"
        
    def save_message(self, message_id: str, message_data: Dict[str, Any]) -> None:
        """Save a message to cache.
        
        Args:
            message_id: Message identifier
            message_data: Message data to save
        """
        message_path = self.cache_dir / "messages" / f"{message_id}.json"
        with open(message_path, "w") as f:
            json.dump(message_data, f, indent=2)
        logger.info(f"Saved message to {message_path}")
        
    def load_message(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Load a message from cache.
        
        Args:
            message_id: Message identifier
            
        Returns:
            Message data or None if not found
        """
        message_path = self.cache_dir / "messages" / f"{message_id}.json"
        if not message_path.exists():
            return None
            
        with open(message_path, "r") as f:
            return json.load(f)
            
    def save_log(self, log_id: str, log_data: str) -> None:
        """Save a log to cache.
        
        Args:
            log_id: Log identifier
            log_data: Log data to save
        """
        log_path = self.cache_dir / "logs" / f"{log_id}.log"
        file_exists = log_path.exists() and log_path.stat().st_size > 0
        
        with open(log_path, "a") as f:
            if file_exists:
                f.write("\n" + log_data)
            else:
                f.write(log_data)
        logger.debug(f"Saved log to {log_path}")
        
    def get_log_path(self, log_id: str) -> Path:
        """Get path for a log file.
        
        Args:
            log_id: Log identifier
            
        Returns:
            Path to the log file
        """
        return self.cache_dir / "logs" / f"{log_id}.log"
        
    def cleanup_temp(self) -> None:
        """Clean up temporary directory."""
        temp_dir = self.get_temp_dir()
        for item in temp_dir.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                import shutil
                shutil.rmtree(item)
        logger.info(f"Cleaned up temporary directory: {temp_dir}")
        
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        stats = {
            "cache_dir": str(self.cache_dir),
            "total_size": 0,
            "config_count": 0,
            "agent_count": 0,
            "service_count": 0,
            "message_count": 0,
            "log_count": 0
        }
        
        for root, dirs, files in os.walk(self.cache_dir):
            for file in files:
                file_path = Path(root) / file
                stats["total_size"] += file_path.stat().st_size
                
                if file_path.parent == self.cache_dir / "config":
                    stats["config_count"] += 1
                elif file_path.parent == self.cache_dir / "messages":
                    stats["message_count"] += 1
                elif file_path.parent == self.cache_dir / "logs":
                    stats["log_count"] += 1
                    
        stats["agent_count"] = len(list((self.cache_dir / "agents").iterdir()))
        stats["service_count"] = len(list((self.cache_dir / "services").iterdir()))
        
        return stats
