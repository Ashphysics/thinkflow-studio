"""
Configuration Package Initialization for ThinkFlow Studio.

This package consolidates application settings, logging setups, and environment
variables. It exports the global settings object and log configuration functions.

TODOs:
    - [ ] Integrate secrets manager for enterprise credential retrieval.
    - [ ] Dynamic settings reload without restarting the main service.
"""

from app.config.logging_config import setup_logging
from app.config.settings import Settings, get_settings

# Instantiate global settings singleton
settings: Settings = get_settings()

__all__: list[str] = [
    "setup_logging",
    "settings",
]
