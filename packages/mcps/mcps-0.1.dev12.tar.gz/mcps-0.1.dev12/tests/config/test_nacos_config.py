"""Tests for Nacos configuration."""

import pytest
import json
import yaml
from unittest.mock import MagicMock, patch
from mcps.config.nacos_config import NacosConfig
from mcps.core.exceptions.base import ConfigurationException


@pytest.fixture
def mock_nacos_client():
    """Create a mock Nacos client."""
    client = MagicMock()
    return client

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

def test_nacos_config_init_with_mock(mock_nacos_client, config_data):
    """Test Nacos config initialization with a mock client."""
    mock_nacos_client.get_config.return_value = json.dumps(config_data)
    
    with patch('mcps.config.nacos_config.nacos.NacosClient', return_value=mock_nacos_client):
        config = NacosConfig(
            server_addr="localhost:8848",
            namespace="test",
            data_id="test_config",
            group="test_group",
            username="test_user",
            password="test_password"
        )
    
    assert config.server_addr == "localhost:8848"
    assert config.namespace == "test"
    assert config.data_id == "test_config"
    assert config.group == "test_group"
    assert config.username == "test_user"
    assert config.password == "test_password"
    
    assert config._config == config_data
    mock_nacos_client.get_config.assert_called_once_with(
        data_id="test_config",
        group="test_group"
    )

def test_nacos_config_load_dynamic_config_json(mock_nacos_client, config_data):
    """Test loading JSON configuration from Nacos."""
    mock_nacos_client.get_config.return_value = json.dumps(config_data)
    
    with patch('mcps.config.nacos_config.nacos.NacosClient', return_value=mock_nacos_client):
        config = NacosConfig(
            server_addr="localhost:8848",
            namespace="test",
            data_id="test_config"
        )
    
    assert config._config == config_data

def test_nacos_config_load_dynamic_config_yaml(mock_nacos_client, config_data):
    """Test loading YAML configuration from Nacos."""
    mock_nacos_client.get_config.return_value = yaml.dump(config_data)
    
    with patch('mcps.config.nacos_config.nacos.NacosClient', return_value=mock_nacos_client):
        config = NacosConfig(
            server_addr="localhost:8848",
            namespace="test",
            data_id="test_config"
        )
    
    assert config._config == config_data

def test_nacos_config_load_dynamic_config_empty(mock_nacos_client):
    """Test loading empty configuration from Nacos."""
    mock_nacos_client.get_config.return_value = None
    
    with patch('mcps.config.nacos_config.nacos.NacosClient', return_value=mock_nacos_client):
        config = NacosConfig(
            server_addr="localhost:8848",
            namespace="test",
            data_id="test_config"
        )
    
    assert config._config == {}

def test_nacos_config_publish_config(mock_nacos_client, config_data):
    """Test publishing configuration to Nacos."""
    mock_nacos_client.publish_config.return_value = True
    mock_nacos_client.get_config.return_value = json.dumps(config_data)
    
    with patch('mcps.config.nacos_config.nacos.NacosClient', return_value=mock_nacos_client):
        config = NacosConfig(
            server_addr="localhost:8848",
            namespace="test",
            data_id="test_config"
        )
    
    result = config.publish_config(config_data)
    
    assert result is True
    mock_nacos_client.publish_config.assert_called_once_with(
        data_id="test_config",
        group="DEFAULT_GROUP",
        content=json.dumps(config_data)
    )

def test_nacos_config_add_listener(mock_nacos_client):
    """Test adding a listener for configuration changes."""
    mock_nacos_client.get_config.return_value = "{}"
    
    with patch('mcps.config.nacos_config.nacos.NacosClient', return_value=mock_nacos_client):
        config = NacosConfig(
            server_addr="localhost:8848",
            namespace="test",
            data_id="test_config"
        )
    
    callback = lambda x: None
    config.add_listener(callback)
    
    mock_nacos_client.add_config_watcher.assert_called_once_with(
        data_id="test_config",
        group="DEFAULT_GROUP",
        cb=callback
    )

def test_nacos_config_remove_listener(mock_nacos_client):
    """Test removing a listener for configuration changes."""
    mock_nacos_client.get_config.return_value = "{}"
    
    with patch('mcps.config.nacos_config.nacos.NacosClient', return_value=mock_nacos_client):
        config = NacosConfig(
            server_addr="localhost:8848",
            namespace="test",
            data_id="test_config"
        )
    
    config.remove_listener()
    
    mock_nacos_client.remove_config_watcher.assert_called_once_with(
        data_id="test_config",
        group="DEFAULT_GROUP"
    )

def test_nacos_config_get_server_status(mock_nacos_client):
    """Test checking if the Nacos server is available."""
    mock_nacos_client.is_valid.return_value = True
    mock_nacos_client.get_config.return_value = "{}"
    
    with patch('mcps.config.nacos_config.nacos.NacosClient', return_value=mock_nacos_client):
        config = NacosConfig(
            server_addr="localhost:8848",
            namespace="test",
            data_id="test_config"
        )
    
    result = config.get_server_status()
    
    assert result is True
    mock_nacos_client.is_valid.assert_called_once()
