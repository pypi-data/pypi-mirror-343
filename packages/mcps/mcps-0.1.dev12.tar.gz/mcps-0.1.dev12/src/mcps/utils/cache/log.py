"""Log caching utilities for MCPS."""

import os
import logging
import time
from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path

from mcps.config.cache import CacheManager

logger = logging.getLogger(__name__)

class LogCache:
    """Cache for storing and retrieving logs."""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize log cache.
        
        Args:
            cache_dir: Optional custom cache directory. Defaults to ~/.mcps
        """
        self.cache_manager = CacheManager(cache_dir)
        
    def save_log(self, log_id: str, log_data: str) -> str:
        """Save a log entry to cache.
        
        Args:
            log_id: Log identifier
            log_data: Log data to save
            
        Returns:
            Path to the saved log file
        """
        self.cache_manager.save_log(log_id, log_data)
        
        log_path = self.cache_manager.cache_dir / "logs" / f"{log_id}.log"
        logger.debug(f"Saved log entry to {log_path}")
        
        return str(log_path)
        
    def get_log_path(self, log_id: str) -> str:
        """Get path for a log file.
        
        Args:
            log_id: Log identifier
            
        Returns:
            Path to the log file
        """
        log_path = self.cache_manager.get_log_path(log_id)
        return str(log_path)
        
    def read_log(self, log_id: str) -> Optional[str]:
        """Read a log from cache.
        
        Args:
            log_id: Log identifier
            
        Returns:
            Log data or None if not found
        """
        log_path = self.cache_manager.get_log_path(log_id)
        
        if not log_path.exists():
            logger.warning(f"Log {log_id} not found in cache")
            return None
            
        try:
            with open(log_path, "r") as f:
                log_data = f.read().rstrip()
            
            logger.info(f"Read log {log_id}")
            return log_data
        except Exception as e:
            logger.error(f"Error reading log {log_id}: {e}")
            return None
            
    def read_log_lines(self, log_id: str, max_lines: int = 100, tail: bool = True) -> List[str]:
        """Read lines from a log.
        
        Args:
            log_id: Log identifier
            max_lines: Maximum number of lines to read
            tail: If True, read from the end of the log
            
        Returns:
            List of log lines
        """
        log_path = self.cache_manager.get_log_path(log_id)
        
        if not log_path.exists():
            logger.warning(f"Log {log_id} not found in cache")
            return []
            
        try:
            with open(log_path, "r") as f:
                lines = f.readlines()
                
            if tail:
                lines = lines[-max_lines:]
            else:
                lines = lines[:max_lines]
                
            return [line.rstrip() for line in lines]
        except Exception as e:
            logger.error(f"Error reading log lines for {log_id}: {e}")
            return []
            
    def list_logs(self) -> List[str]:
        """List available logs.
        
        Returns:
            List of log IDs
        """
        logs_dir = self.cache_manager.cache_dir / "logs"
        
        if not logs_dir.exists():
            return []
            
        log_files = [f for f in logs_dir.iterdir() if f.is_file() and f.suffix == ".log"]
        
        return [f.stem for f in log_files]
        
    def search_logs(self, query: str, max_results: int = 100) -> Dict[str, List[str]]:
        """Search logs for a query.
        
        Args:
            query: Search query
            max_results: Maximum number of results per log
            
        Returns:
            Dictionary mapping log IDs to matching lines
        """
        logs_dir = self.cache_manager.cache_dir / "logs"
        
        if not logs_dir.exists():
            return {}
            
        log_files = [f for f in logs_dir.iterdir() if f.is_file() and f.suffix == ".log"]
        
        results = {}
        
        for log_file in log_files:
            try:
                matching_lines = []
                
                with open(log_file, "r") as f:
                    for line in f:
                        if query.lower() in line.lower():
                            matching_lines.append(line.rstrip())
                            
                            if len(matching_lines) >= max_results:
                                break
                                
                if matching_lines:
                    results[log_file.stem] = matching_lines
            except Exception as e:
                logger.error(f"Error searching log {log_file}: {e}")
                
        return results
        
    def delete_log(self, log_id: str) -> bool:
        """Delete a log from cache.
        
        Args:
            log_id: Log identifier
            
        Returns:
            True if log was deleted, False otherwise
        """
        log_path = self.cache_manager.get_log_path(log_id)
        
        if not log_path.exists():
            logger.warning(f"Log {log_id} not found in cache")
            return False
            
        try:
            log_path.unlink()
            logger.info(f"Deleted log {log_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting log {log_id}: {e}")
            return False
            
    def clear_logs(self, older_than_days: Optional[int] = None) -> int:
        """Clear cached logs.
        
        Args:
            older_than_days: Only clear logs older than this many days
            
        Returns:
            Number of logs cleared
        """
        logs_dir = self.cache_manager.cache_dir / "logs"
        
        if not logs_dir.exists():
            return 0
            
        log_files = [f for f in logs_dir.iterdir() if f.is_file() and f.suffix == ".log"]
        
        cleared_count = 0
        
        for log_file in log_files:
            try:
                if older_than_days is not None:
                    mtime = log_file.stat().st_mtime
                    age_days = (time.time() - mtime) / (60 * 60 * 24)
                    
                    if age_days < older_than_days:
                        continue
                        
                log_file.unlink()
                cleared_count += 1
            except Exception as e:
                logger.error(f"Error clearing log {log_file}: {e}")
                
        logger.info(f"Cleared {cleared_count} logs")
        return cleared_count
        
    def rotate_log(self, log_id: str, max_size_kb: int = 1024, max_backups: int = 5) -> bool:
        """Rotate a log file if it exceeds the maximum size.
        
        Args:
            log_id: Log identifier
            max_size_kb: Maximum log size in KB
            max_backups: Maximum number of backup files to keep
            
        Returns:
            True if log was rotated, False otherwise
        """
        log_path = self.cache_manager.get_log_path(log_id)
        
        if not log_path.exists():
            logger.warning(f"Log {log_id} not found in cache")
            return False
            
        try:
            size_kb = log_path.stat().st_size / 1024
            
            if size_kb <= max_size_kb:
                return False
                
            for i in range(max_backups - 1, 0, -1):
                backup_path = log_path.with_suffix(f".log.{i}")
                prev_backup_path = log_path.with_suffix(f".log.{i-1}")
                
                if prev_backup_path.exists():
                    if backup_path.exists():
                        backup_path.unlink()
                    prev_backup_path.rename(backup_path)
                    
            backup_path = log_path.with_suffix(".log.1")
            if backup_path.exists():
                backup_path.unlink()
            log_path.rename(backup_path)
            
            log_path.touch()
            
            logger.info(f"Rotated log {log_id}")
            return True
        except Exception as e:
            logger.error(f"Error rotating log {log_id}: {e}")
            return False
