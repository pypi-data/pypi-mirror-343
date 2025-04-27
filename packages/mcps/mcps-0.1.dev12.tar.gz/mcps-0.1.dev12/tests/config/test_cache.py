"""Tests for the cache manager."""

import os
import json
import shutil
import tempfile
from pathlib import Path
from unittest import mock

import pytest

from mcps.config.cache import CacheManager


@pytest.fixture
def temp_cache_dir():
    """Create a temporary directory for cache testing."""
    temp_dir = tempfile.mkdtemp(prefix="mcps_cache_test_")
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_cache_manager_init(temp_cache_dir):
    """Test cache manager initialization."""
    cache_manager = CacheManager(cache_dir=temp_cache_dir)
    
    assert os.path.exists(temp_cache_dir)
    assert os.path.exists(os.path.join(temp_cache_dir, "config"))
    assert os.path.exists(os.path.join(temp_cache_dir, "temp"))
    assert os.path.exists(os.path.join(temp_cache_dir, "agents"))
    assert os.path.exists(os.path.join(temp_cache_dir, "services"))
    assert os.path.exists(os.path.join(temp_cache_dir, "logs"))
    assert os.path.exists(os.path.join(temp_cache_dir, "messages"))


def test_config_save_load(temp_cache_dir):
    """Test saving and loading configuration."""
    cache_manager = CacheManager(cache_dir=temp_cache_dir)
    
    config_data = {
        "name": "test_config",
        "value": 42,
        "nested": {
            "key": "value"
        }
    }
    
    cache_manager.save_config("test_config", config_data)
    
    config_path = os.path.join(temp_cache_dir, "config", "test_config.json")
    assert os.path.exists(config_path)
    
    with open(config_path, "r") as f:
        saved_data = json.load(f)
    assert saved_data == config_data
    
    loaded_data = cache_manager.load_config("test_config")
    assert loaded_data == config_data
    
    empty_data = cache_manager.load_config("non_existent")
    assert empty_data == {}


def test_agent_cache_dir(temp_cache_dir):
    """Test agent cache directory."""
    cache_manager = CacheManager(cache_dir=temp_cache_dir)
    
    agent_dir = cache_manager.get_agent_cache_dir("test_agent")
    
    assert os.path.exists(os.path.join(temp_cache_dir, "agents", "test_agent"))
    assert agent_dir == Path(os.path.join(temp_cache_dir, "agents", "test_agent"))


def test_service_cache_dir(temp_cache_dir):
    """Test service cache directory."""
    cache_manager = CacheManager(cache_dir=temp_cache_dir)
    
    service_dir = cache_manager.get_service_cache_dir("test_service")
    
    assert os.path.exists(os.path.join(temp_cache_dir, "services", "test_service"))
    assert service_dir == Path(os.path.join(temp_cache_dir, "services", "test_service"))


def test_temp_dir(temp_cache_dir):
    """Test temporary directory."""
    cache_manager = CacheManager(cache_dir=temp_cache_dir)
    
    temp_dir = cache_manager.get_temp_dir()
    
    assert os.path.exists(os.path.join(temp_cache_dir, "temp"))
    assert temp_dir == Path(os.path.join(temp_cache_dir, "temp"))


def test_message_save_load(temp_cache_dir):
    """Test saving and loading messages."""
    cache_manager = CacheManager(cache_dir=temp_cache_dir)
    
    message_data = {
        "id": "test_message",
        "content": "Hello, world!",
        "timestamp": "2025-04-26T12:34:56Z"
    }
    
    cache_manager.save_message("test_message", message_data)
    
    message_path = os.path.join(temp_cache_dir, "messages", "test_message.json")
    assert os.path.exists(message_path)
    
    with open(message_path, "r") as f:
        saved_data = json.load(f)
    assert saved_data == message_data
    
    loaded_data = cache_manager.load_message("test_message")
    assert loaded_data == message_data
    
    assert cache_manager.load_message("non_existent") is None


def test_log_save(temp_cache_dir):
    """Test saving logs."""
    cache_manager = CacheManager(cache_dir=temp_cache_dir)
    
    log_data = "2025-04-26 12:34:56 INFO Test log message"
    
    cache_manager.save_log("test_log", log_data)
    
    log_path = os.path.join(temp_cache_dir, "logs", "test_log.log")
    assert os.path.exists(log_path)
    
    with open(log_path, "r") as f:
        saved_data = f.read().strip()
    assert saved_data == log_data
    
    additional_log_data = "2025-04-26 12:35:00 INFO Another log message"
    cache_manager.save_log("test_log", additional_log_data)
    
    with open(log_path, "r") as f:
        saved_data = f.read().strip().split("\n")
    assert saved_data == [log_data, additional_log_data]


def test_cleanup_temp(temp_cache_dir):
    """Test cleaning up temporary directory."""
    cache_manager = CacheManager(cache_dir=temp_cache_dir)
    
    temp_dir = cache_manager.get_temp_dir()
    test_file = temp_dir / "test_file.txt"
    test_dir = temp_dir / "test_dir"
    
    with open(test_file, "w") as f:
        f.write("Test file")
    
    test_dir.mkdir()
    with open(test_dir / "nested_file.txt", "w") as f:
        f.write("Nested file")
    
    assert test_file.exists()
    assert test_dir.exists()
    assert (test_dir / "nested_file.txt").exists()
    
    cache_manager.cleanup_temp()
    
    assert not test_file.exists()
    assert not test_dir.exists()
    assert not (test_dir / "nested_file.txt").exists()


def test_get_cache_stats(temp_cache_dir):
    """Test getting cache statistics."""
    cache_manager = CacheManager(cache_dir=temp_cache_dir)
    
    cache_manager.save_config("test_config", {"key": "value"})
    cache_manager.save_message("test_message", {"content": "Hello"})
    cache_manager.save_log("test_log", "Log message")
    
    stats = cache_manager.get_cache_stats()
    
    assert stats["cache_dir"] == temp_cache_dir
    assert stats["total_size"] > 0
    assert stats["config_count"] == 1
    assert stats["message_count"] == 1
    assert stats["log_count"] == 1
    assert stats["agent_count"] == 0
    assert stats["service_count"] == 0


@mock.patch("os.path.expanduser")
def test_default_cache_dir(mock_expanduser, temp_cache_dir):
    """Test default cache directory."""
    mock_expanduser.return_value = temp_cache_dir
    
    cache_manager = CacheManager()
    
    assert os.path.exists(temp_cache_dir)
    assert os.path.exists(os.path.join(temp_cache_dir, "config"))
    assert os.path.exists(os.path.join(temp_cache_dir, "temp"))
    assert os.path.exists(os.path.join(temp_cache_dir, "agents"))
    assert os.path.exists(os.path.join(temp_cache_dir, "services"))
    assert os.path.exists(os.path.join(temp_cache_dir, "logs"))
    assert os.path.exists(os.path.join(temp_cache_dir, "messages"))
