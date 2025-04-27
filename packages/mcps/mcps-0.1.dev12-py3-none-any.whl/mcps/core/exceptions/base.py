from typing import Optional, Any, Dict

class MCPSException(Exception):
    """Base exception class for MCPS framework"""
    def __init__(self, message: str, code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.code = code
        self.details = details or {}

class TransportException(MCPSException):
    """Base class for transport-related exceptions"""
    pass

class AuthenticationException(MCPSException):
    """Base class for authentication-related exceptions"""
    pass

class ServiceException(MCPSException):
    """Base class for service-related exceptions"""
    pass

class AgentException(MCPSException):
    """Base class for agent-related exceptions"""
    pass

class ToolException(MCPSException):
    """Base class for tool-related exceptions"""
    pass

class ConfigurationException(MCPSException):
    """Base class for configuration-related exceptions"""
    pass

class ValidationException(MCPSException):
    """Base class for validation-related exceptions"""
    pass

class ResourceException(MCPSException):
    """Base class for resource-related exceptions"""
    pass

class StateException(MCPSException):
    """Base class for state management exceptions"""
    pass 