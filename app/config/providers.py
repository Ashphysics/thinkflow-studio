"""
Provider configuration schemas for language models.
"""

from pydantic import BaseModel, ConfigDict
from typing import Literal

from app.config.constants import PROVIDER_GOOGLE, PROVIDER_ANTHROPIC, PROVIDER_OPENAI


class BaseProviderConfig(BaseModel):
    """
    Base configuration for any model provider.
    """
    model_config = ConfigDict(extra="ignore")
    
    provider: str
    model_name: str
    temperature: float = 0.0
    max_output_tokens: int | None = None
    timeout: int = 30


class GoogleProviderConfig(BaseProviderConfig):
    """
    Google Gemini specific configuration.
    """
    provider: Literal[PROVIDER_GOOGLE] = PROVIDER_GOOGLE
    top_p: float | None = None
    top_k: int | None = None


class ProviderFactory:
    """
    Helper to instantiate the right provider configuration.
    """
    @staticmethod
    def create_google_config(model_name: str, **kwargs) -> GoogleProviderConfig:
        return GoogleProviderConfig(model_name=model_name, **kwargs)
