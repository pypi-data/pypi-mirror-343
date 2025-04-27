"""Message caching utilities for MCPS."""

import os
import json
import logging
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

from mcps.config.cache import CacheManager

logger = logging.getLogger(__name__)

class MessageCache:
    """Cache for storing and retrieving messages."""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize message cache.
        
        Args:
            cache_dir: Optional custom cache directory. Defaults to ~/.mcps
        """
        self.cache_manager = CacheManager(cache_dir)
        
    def save_message(self, message_id: str, message_data: Dict[str, Any]) -> str:
        """Save a message to cache.
        
        Args:
            message_id: Message identifier
            message_data: Message data to save
            
        Returns:
            Path to the saved message file
        """
        if "timestamp" not in message_data:
            message_data["timestamp"] = datetime.utcnow().isoformat() + "Z"
            
        if "id" not in message_data:
            message_data["id"] = message_id
            
        self.cache_manager.save_message(message_id, message_data)
        
        message_path = self.cache_manager.cache_dir / "messages" / f"{message_id}.json"
        logger.info(f"Saved message {message_id} to {message_path}")
        
        return str(message_path)
        
    def load_message(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Load a message from cache.
        
        Args:
            message_id: Message identifier
            
        Returns:
            Message data or None if not found
        """
        message_data = self.cache_manager.load_message(message_id)
        
        if message_data:
            logger.info(f"Loaded message {message_id}")
        else:
            logger.warning(f"Message {message_id} not found in cache")
            
        return message_data
        
    def list_messages(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """List cached messages.
        
        Args:
            limit: Maximum number of messages to return
            offset: Number of messages to skip
            
        Returns:
            List of message data
        """
        messages_dir = self.cache_manager.cache_dir / "messages"
        
        if not messages_dir.exists():
            return []
            
        message_files = sorted(
            [f for f in messages_dir.iterdir() if f.is_file() and f.suffix == ".json"],
            key=lambda f: f.stat().st_mtime,
            reverse=True
        )
        
        messages = []
        
        for i, message_file in enumerate(message_files):
            if i < offset:
                continue
                
            if len(messages) >= limit:
                break
                
            try:
                with open(message_file, "r") as f:
                    message_data = json.load(f)
                    messages.append(message_data)
            except Exception as e:
                logger.error(f"Error loading message from {message_file}: {e}")
                
        return messages
        
    def search_messages(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Search cached messages.
        
        Args:
            query: Search query
            limit: Maximum number of messages to return
            
        Returns:
            List of matching message data
        """
        messages_dir = self.cache_manager.cache_dir / "messages"
        
        if not messages_dir.exists():
            return []
            
        message_files = [f for f in messages_dir.iterdir() if f.is_file() and f.suffix == ".json"]
        
        matches = []
        
        for message_file in message_files:
            try:
                with open(message_file, "r") as f:
                    message_data = json.load(f)
                    
                content = message_data.get("content", "")
                if isinstance(content, str) and query.lower() in content.lower():
                    matches.append(message_data)
                    
                    if len(matches) >= limit:
                        break
            except Exception as e:
                logger.error(f"Error searching message in {message_file}: {e}")
                
        return matches
        
    def delete_message(self, message_id: str) -> bool:
        """Delete a message from cache.
        
        Args:
            message_id: Message identifier
            
        Returns:
            True if message was deleted, False otherwise
        """
        message_path = self.cache_manager.cache_dir / "messages" / f"{message_id}.json"
        
        if not message_path.exists():
            logger.warning(f"Message {message_id} not found in cache")
            return False
            
        try:
            message_path.unlink()
            logger.info(f"Deleted message {message_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting message {message_id}: {e}")
            return False
            
    def clear_messages(self, older_than_days: Optional[int] = None) -> int:
        """Clear cached messages.
        
        Args:
            older_than_days: Only clear messages older than this many days
            
        Returns:
            Number of messages cleared
        """
        messages_dir = self.cache_manager.cache_dir / "messages"
        
        if not messages_dir.exists():
            return 0
            
        message_files = [f for f in messages_dir.iterdir() if f.is_file() and f.suffix == ".json"]
        
        cleared_count = 0
        
        for message_file in message_files:
            try:
                if older_than_days is not None:
                    mtime = message_file.stat().st_mtime
                    age_days = (time.time() - mtime) / (60 * 60 * 24)
                    
                    if age_days < older_than_days:
                        continue
                        
                message_file.unlink()
                cleared_count += 1
            except Exception as e:
                logger.error(f"Error clearing message {message_file}: {e}")
                
        logger.info(f"Cleared {cleared_count} messages")
        return cleared_count
