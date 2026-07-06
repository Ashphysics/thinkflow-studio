"""
Application settings configuration module for ThinkFlow Studio.

Utilizes pydantic-settings to validate environment variables parsed from local .env files.
Provides a cached singleton method to access settings globally.

TODOs:
    - [ ] Add integration with Google Cloud Secret Manager for production environment.
    - [ ] Create specialized settings sections for custom MCP server integrations.
"""

from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Settings configuration class.

    Reads variables from system environments or from local `.env` files.
    """
    # Configuration metadata
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Google Gemini API Settings
    # SecretStr protects the key from accidental console prints or logs
    gemini_api_key: SecretStr | None = Field(
        default=None,
        validation_alias="GOOGLE_API_KEY"
    )

    # App Environment Settings
    app_env: str = Field(default="development", validation_alias="APP_ENV")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")

    # Database Configuration
    database_url: str = Field(
        default="sqlite:///./thinkflow.db",
        validation_alias="DATABASE_URL"
    )

    # UI Streamlit Portal Configuration
    streamlit_server_port: int = Field(
        default=8501,
        validation_alias="STREAMLIT_SERVER_PORT"
    )
    streamlit_server_address: str = Field(
        default="0.0.0.0",
        validation_alias="STREAMLIT_SERVER_ADDRESS"
    )

    # Model Context Protocol URL
    mcp_server_url: str = Field(
        default="http://localhost:8000/sse",
        validation_alias="MCP_SERVER_URL"
    )

    # Default Google Gemini Models
    default_coordinator_model: str = Field(
        default="gemini-2.5-pro",
        validation_alias="DEFAULT_COORDINATOR_MODEL"
    )
    default_analyzer_model: str = Field(
        default="gemini-2.5-flash",
        validation_alias="DEFAULT_ANALYZER_MODEL"
    )
    default_critic_model: str = Field(
        default="gemini-2.5-pro",
        validation_alias="DEFAULT_CRITIC_MODEL"
    )


@lru_cache
def get_settings() -> Settings:
    """
    Retrieve cached Settings singleton instance.

    Returns:
        Settings: Validated configuration settings.
    """
    return Settings()
