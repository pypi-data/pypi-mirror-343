"""Tests for message and log caching utilities."""

import os
import json
import shutil
import tempfile
from pathlib import Path
from unittest import mock

import pytest

from mcps.utils import MessageCache, LogCache


@pytest.fixture
def temp_cache_dir():
    """Create a temporary directory for cache testing."""
    temp_dir = tempfile.mkdtemp(prefix="mcps_cache_test_")
    yield temp_dir
    shutil.rmtree(temp_dir)


class TestMessageCache:
    """Test the message cache functionality."""
    
    def test_save_load_message(self, temp_cache_dir):
        """Test saving and loading a message."""
        cache = MessageCache(cache_dir=temp_cache_dir)
        
        message_id = "test_message"
        message_data = {
            "content": "Hello, world!",
            "sender": "test_agent",
            "recipient": "test_service"
        }
        
        path = cache.save_message(message_id, message_data)
        assert os.path.exists(path)
        
        loaded_data = cache.load_message(message_id)
        assert loaded_data is not None
        assert loaded_data["content"] == "Hello, world!"
        assert loaded_data["sender"] == "test_agent"
        assert loaded_data["recipient"] == "test_service"
        assert "timestamp" in loaded_data
        assert "id" in loaded_data
        
    def test_list_messages(self, temp_cache_dir):
        """Test listing messages."""
        cache = MessageCache(cache_dir=temp_cache_dir)
        
        for i in range(5):
            message_id = f"test_message_{i}"
            message_data = {
                "content": f"Message {i}",
                "sender": "test_agent",
                "recipient": "test_service"
            }
            cache.save_message(message_id, message_data)
            
        messages = cache.list_messages()
        assert len(messages) == 5
        
        messages = cache.list_messages(limit=3)
        assert len(messages) == 3
        
        messages = cache.list_messages(offset=2)
        assert len(messages) == 3
        
    def test_search_messages(self, temp_cache_dir):
        """Test searching messages."""
        cache = MessageCache(cache_dir=temp_cache_dir)
        
        cache.save_message("message_1", {"content": "Hello, world!"})
        cache.save_message("message_2", {"content": "Hello, Python!"})
        cache.save_message("message_3", {"content": "Goodbye, world!"})
        
        results = cache.search_messages("Hello")
        assert len(results) == 2
        
        results = cache.search_messages("world")
        assert len(results) == 2
        
        results = cache.search_messages("Python")
        assert len(results) == 1
        
        results = cache.search_messages("nonexistent")
        assert len(results) == 0
        
    def test_delete_message(self, temp_cache_dir):
        """Test deleting a message."""
        cache = MessageCache(cache_dir=temp_cache_dir)
        
        message_id = "test_message"
        cache.save_message(message_id, {"content": "Test message"})
        
        assert cache.load_message(message_id) is not None
        
        result = cache.delete_message(message_id)
        assert result is True
        
        assert cache.load_message(message_id) is None
        
        result = cache.delete_message("nonexistent")
        assert result is False
        
    def test_clear_messages(self, temp_cache_dir):
        """Test clearing messages."""
        cache = MessageCache(cache_dir=temp_cache_dir)
        
        for i in range(5):
            cache.save_message(f"message_{i}", {"content": f"Message {i}"})
            
        count = cache.clear_messages()
        assert count == 5
        
        messages = cache.list_messages()
        assert len(messages) == 0


class TestLogCache:
    """Test the log cache functionality."""
    
    def test_save_read_log(self, temp_cache_dir):
        """Test saving and reading a log."""
        cache = LogCache(cache_dir=temp_cache_dir)
        
        log_id = "test_log"
        log_data = "2025-04-26 12:34:56 INFO Test log message"
        
        path = cache.save_log(log_id, log_data)
        assert os.path.exists(path)
        
        loaded_data = cache.read_log(log_id)
        assert loaded_data is not None
        assert loaded_data == log_data
        
    def test_read_log_lines(self, temp_cache_dir):
        """Test reading log lines."""
        cache = LogCache(cache_dir=temp_cache_dir)
        
        log_id = "test_log"
        log_lines = [
            "2025-04-26 12:34:56 INFO Line 1",
            "2025-04-26 12:34:57 INFO Line 2",
            "2025-04-26 12:34:58 INFO Line 3",
            "2025-04-26 12:34:59 INFO Line 4",
            "2025-04-26 12:35:00 INFO Line 5"
        ]
        
        for line in log_lines:
            cache.save_log(log_id, line)
            
        lines = cache.read_log_lines(log_id)
        assert len(lines) == 5
        
        lines = cache.read_log_lines(log_id, max_lines=3)
        assert len(lines) == 3
        assert lines[0] == log_lines[2]
        assert lines[2] == log_lines[4]
        
        lines = cache.read_log_lines(log_id, max_lines=3, tail=False)
        assert len(lines) == 3
        assert lines[0] == log_lines[0]
        assert lines[2] == log_lines[2]
        
    def test_list_logs(self, temp_cache_dir):
        """Test listing logs."""
        cache = LogCache(cache_dir=temp_cache_dir)
        
        for i in range(3):
            cache.save_log(f"log_{i}", f"Log {i}")
            
        logs = cache.list_logs()
        assert len(logs) == 3
        assert "log_0" in logs
        assert "log_1" in logs
        assert "log_2" in logs
        
    def test_search_logs(self, temp_cache_dir):
        """Test searching logs."""
        cache = LogCache(cache_dir=temp_cache_dir)
        
        cache.save_log("log_1", "2025-04-26 12:34:56 INFO Hello, world!")
        cache.save_log("log_2", "2025-04-26 12:34:57 INFO Hello, Python!")
        cache.save_log("log_3", "2025-04-26 12:34:58 INFO Goodbye, world!")
        
        results = cache.search_logs("Hello")
        assert len(results) == 2
        assert "log_1" in results
        assert "log_2" in results
        
        results = cache.search_logs("world")
        assert len(results) == 2
        assert "log_1" in results
        assert "log_3" in results
        
        results = cache.search_logs("Python")
        assert len(results) == 1
        assert "log_2" in results
        
        results = cache.search_logs("nonexistent")
        assert len(results) == 0
        
    def test_delete_log(self, temp_cache_dir):
        """Test deleting a log."""
        cache = LogCache(cache_dir=temp_cache_dir)
        
        log_id = "test_log"
        cache.save_log(log_id, "Test log")
        
        assert cache.read_log(log_id) is not None
        
        result = cache.delete_log(log_id)
        assert result is True
        
        assert cache.read_log(log_id) is None
        
        result = cache.delete_log("nonexistent")
        assert result is False
        
    def test_clear_logs(self, temp_cache_dir):
        """Test clearing logs."""
        cache = LogCache(cache_dir=temp_cache_dir)
        
        for i in range(3):
            cache.save_log(f"log_{i}", f"Log {i}")
            
        count = cache.clear_logs()
        assert count == 3
        
        logs = cache.list_logs()
        assert len(logs) == 0
        
    def test_rotate_log(self, temp_cache_dir):
        """Test log rotation."""
        cache = LogCache(cache_dir=temp_cache_dir)
        
        log_id = "test_log"
        
        large_log_data = "X" * 2048  # 2KB
        cache.save_log(log_id, large_log_data)
        
        result = cache.rotate_log(log_id, max_size_kb=1)
        assert result is True
        
        log_path = Path(cache.get_log_path(log_id))
        assert log_path.exists()
        assert log_path.stat().st_size == 0
        
        backup_path = log_path.with_suffix(".log.1")
        assert backup_path.exists()
        
        cache.save_log(log_id, "Small log")
        result = cache.rotate_log(log_id, max_size_kb=1)
        assert result is False
