"""
Core exception hierarchy for ThinkFlow Studio.
"""

class ThinkFlowError(Exception):
    """Base class for all ThinkFlow exceptions."""
    pass

class ConfigurationError(ThinkFlowError):
    """Raised when there is an issue with application configuration."""
    pass

class DependencyError(ThinkFlowError):
    """Raised when a dependency cannot be resolved or is incorrectly registered."""
    pass

class ModelInitializationError(ThinkFlowError):
    """Raised when an AI model fails to initialize."""
    pass

class AgentExecutionError(ThinkFlowError):
    """Raised when an agent encounters an error during execution."""
    pass

class SessionError(ThinkFlowError):
    """Raised when a session management operation fails."""
    pass
