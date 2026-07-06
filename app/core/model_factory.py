"""
Model Factory for ThinkFlow Studio.
Handles singleton initialization and lazy loading of Google Gen AI models.
"""

from typing import Dict
from google import genai
from loguru import logger

from app.config.settings import get_settings
from app.config.providers import BaseProviderConfig, GoogleProviderConfig
from app.core.exceptions import ModelInitializationError

class ModelFactory:
    """
    Factory for managing GenAI SDK model clients.
    Implements caching to ensure models are singletons and lazy-loaded.
    """
    
    def __init__(self) -> None:
        self._clients: Dict[str, genai.Client] = {}
        self._models: Dict[str, Any] = {} # Abstract return types based on ADK/GenAI
        self._settings = get_settings()

    def _get_client(self) -> genai.Client:
        """
        Retrieves or initializes the Google GenAI SDK Client.
        """
        client_key = "default"
        if client_key not in self._clients:
            api_key = self._settings.gemini_api_key.get_secret_value() if self._settings.gemini_api_key else None
            if not api_key:
                raise ModelInitializationError("GOOGLE_API_KEY is not set.")
            try:
                # Initialize GenAI Client
                self._clients[client_key] = genai.Client(api_key=api_key)
                logger.debug("Initialized Google GenAI SDK Client.")
            except Exception as e:
                logger.exception("Failed to initialize GenAI Client")
                raise ModelInitializationError(f"Client init failed: {e}")
        return self._clients[client_key]

    def get_model(self, config: BaseProviderConfig) -> Any:
        """
        Returns a configured GenAI model based on the provider config.
        Implements lazy loading and caching.
        """
        cache_key = f"{config.provider}_{config.model_name}"
        
        if cache_key in self._models:
            return self._models[cache_key]
            
        logger.info(f"Lazy loading model: {cache_key}")
        
        if isinstance(config, GoogleProviderConfig):
            try:
                client = self._get_client()
                # Store client/model reference or initialize ADK specific model wrapper here
                # For basic GenAI usage, we just return a dictionary containing client and config
                # that agents can use to call `client.models.generate_content`
                model_wrapper = {
                    "client": client,
                    "model_id": config.model_name,
                    "config": genai.types.GenerateContentConfig(
                        temperature=config.temperature,
                        max_output_tokens=config.max_output_tokens,
                        top_p=config.top_p,
                        top_k=config.top_k
                    )
                }
                self._models[cache_key] = model_wrapper
                return model_wrapper
            except Exception as e:
                logger.exception(f"Failed to load model {config.model_name}")
                raise ModelInitializationError(f"Model load failed: {e}")
        else:
            raise ModelInitializationError(f"Unsupported provider config: {config.provider}")

from typing import Any
