"""
Configuration Package Initialization for ThinkFlow Studio.

This package consolidates application settings, logging setups, and environment
variables. It exports the global settings object and log configuration functions.

TODOs:
    - [ ] Integrate secrets manager for enterprise credential retrieval.
    - [ ] Dynamic settings reload without restarting the main service.
"""

from app.config.constants import DEFAULT_MAX_LOOPS, DEFAULT_TIMEOUT
from app.config.logging_config import configure_logging
from app.config.settings import Settings, get_settings

# Instantiate global settings singleton
settings: Settings = get_settings()

__all__: list[str] = [
    "DEFAULT_MAX_LOOPS",
    "DEFAULT_TIMEOUT",
    "configure_logging",
    "settings",
]
