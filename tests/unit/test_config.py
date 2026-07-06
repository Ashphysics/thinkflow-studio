"""
Unit tests for the application config modules.
"""

import pytest
from app.config.constants import PROVIDER_GOOGLE, DEFAULT_TIMEOUT_SECONDS
from app.config.providers import ProviderFactory, GoogleProviderConfig

def test_constants():
    """Verify constants are correctly imported and typed."""
    assert PROVIDER_GOOGLE == "google"
    assert isinstance(DEFAULT_TIMEOUT_SECONDS, int)

def test_google_provider_config():
    """Verify Google Provider Config instantiation."""
    config = ProviderFactory.create_google_config(
        model_name="gemini-2.5-pro",
        temperature=0.7
    )
    
    assert isinstance(config, GoogleProviderConfig)
    assert config.provider == "google"
    assert config.model_name == "gemini-2.5-pro"
    assert config.temperature == 0.7
