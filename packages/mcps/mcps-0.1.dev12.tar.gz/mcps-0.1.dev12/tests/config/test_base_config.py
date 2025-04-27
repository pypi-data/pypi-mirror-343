"""Tests for base configuration."""

import os
import tempfile
import pytest
import json
import yaml
from mcps.config.base import BaseConfig


@pytest.fixture
def config_data():
    """Create test configuration data."""
    return {
        "test_key": "test_value",
        "nested": {
            "key": "value"
        },
        "list": [1, 2, 3]
    }

@pytest.fixture
def json_config_file(config_data):
    """Create a temporary JSON configuration file."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode='w') as f:
        json.dump(config_data, f)
        return f.name

@pytest.fixture
def yaml_config_file(config_data):
    """Create a temporary YAML configuration file."""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode='w') as f:
        yaml.dump(config_data, f)
        return f.name

def test_base_config_init_empty():
    """Test base config initialization without a file."""
    config = BaseConfig()
    assert config._config == {}

def test_base_config_load_json(json_config_file, config_data):
    """Test loading configuration from a JSON file."""
    config = BaseConfig(json_config_file)
    assert config._config == config_data
    
    os.unlink(json_config_file)

def test_base_config_load_yaml(yaml_config_file, config_data):
    """Test loading configuration from a YAML file."""
    config = BaseConfig(yaml_config_file)
    assert config._config == config_data
    
    os.unlink(yaml_config_file)

def test_base_config_get():
    """Test getting configuration values."""
    config = BaseConfig()
    config._config = {"key1": "value1", "key2": {"nested": "value2"}}
    
    assert config.get("key1") == "value1"
    assert config.get("key2") == {"nested": "value2"}
    assert config.get("non_existent") is None
    assert config.get("non_existent", "default") == "default"

def test_base_config_set():
    """Test setting configuration values."""
    config = BaseConfig()
    
    config.set("key1", "value1")
    assert config._config["key1"] == "value1"
    
    config.set("key2", {"nested": "value2"})
    assert config._config["key2"] == {"nested": "value2"}

def test_base_config_update():
    """Test updating configuration."""
    config = BaseConfig()
    config._config = {"key1": "value1"}
    
    config.update({"key2": "value2", "key3": "value3"})
    assert config._config == {"key1": "value1", "key2": "value2", "key3": "value3"}
    
    config.update({"key1": "new_value1"})
    assert config._config["key1"] == "new_value1"

def test_base_config_save_json():
    """Test saving configuration to a JSON file."""
    config = BaseConfig()
    config._config = {"key1": "value1", "key2": {"nested": "value2"}}
    
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        config_path = f.name
    
    result = config.save(config_path)
    assert result is True
    
    with open(config_path, 'r') as f:
        loaded_config = json.load(f)
    
    assert loaded_config == config._config
    
    os.unlink(config_path)

def test_base_config_save_yaml():
    """Test saving configuration to a YAML file."""
    config = BaseConfig()
    config._config = {"key1": "value1", "key2": {"nested": "value2"}}
    
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
        config_path = f.name
    
    result = config.save(config_path)
    assert result is True
    
    with open(config_path, 'r') as f:
        loaded_config = yaml.safe_load(f)
    
    assert loaded_config == config._config
    
    os.unlink(config_path)

def test_base_config_dict_methods():
    """Test dictionary-like methods."""
    config = BaseConfig()
    config._config = {"key1": "value1"}
    
    assert config["key1"] == "value1"
    
    config["key2"] = "value2"
    assert config._config["key2"] == "value2"
    
    assert "key1" in config
    assert "non_existent" not in config
