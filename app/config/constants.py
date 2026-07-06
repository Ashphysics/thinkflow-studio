"""
System-wide constants and enumerations.
"""

from typing import Final

# Timeout definitions
DEFAULT_TIMEOUT_SECONDS: Final[int] = 30
EXTENDED_TIMEOUT_SECONDS: Final[int] = 120

# Model Provider String Identifiers
PROVIDER_GOOGLE: Final[str] = "google"
PROVIDER_ANTHROPIC: Final[str] = "anthropic"
PROVIDER_OPENAI: Final[str] = "openai"

# API Limits
MAX_RETRIES: Final[int] = 3
BACKOFF_FACTOR: Final[float] = 1.5

# Standard System Messages
DEFAULT_AGENT_SYSTEM_PROMPT: Final[str] = (
    "You are an expert AI agent in ThinkFlow Studio. "
    "Follow instructions carefully and use provided tools when necessary."
)
