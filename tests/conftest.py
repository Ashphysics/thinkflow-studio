"""
Global Pytest Configurations and Shared Fixtures for ThinkFlow Studio.

TODOs:
    - [ ] Add mock adapters for Vertex AI / Google Gen AI API calls.
    - [ ] Create seed fixture databases to test transaction insertions.
"""


import pytest

from app.config.settings import Settings, get_settings


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """
    Retrieves global settings config overriden for test execution profiles.
    """
    settings = get_settings()
    # Force settings overrides to avoid hitting production databases/services
    settings.app_env = "test"
    settings.database_url = "sqlite:///:memory:"
    return settings
