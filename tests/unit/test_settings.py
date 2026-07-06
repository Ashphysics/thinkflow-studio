"""
Unit tests for settings configurations module in ThinkFlow Studio.
"""

from app.config.settings import Settings, get_settings


def test_settings_initialization() -> None:
    """
    Verifies settings can load default values successfully.
    """
    settings = get_settings()
    assert isinstance(settings, Settings)
    assert settings.streamlit_server_port == 8501
    assert settings.default_coordinator_model == "gemini-2.5-pro"
