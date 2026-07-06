"""
Abstract Base Agent definition.
"""

from abc import ABC, abstractmethod
from typing import List, Any, Optional
from loguru import logger

from app.core.base_tool import BaseTool
from app.config.providers import BaseProviderConfig
from app.core.dependency_container import container
from app.core.model_factory import ModelFactory

class BaseAgent(ABC):
    """
    Abstract Base Class for agents.
    Provides standard lifecycle hooks, tool binding, and model initialization.
    """
    
    def __init__(self, config: BaseProviderConfig, tools: Optional[List[BaseTool]] = None) -> None:
        """
        Initializes the agent by fetching a model instance from the ModelFactory.
        """
        self.config = config
        self.tools = tools or []
        
        # Dependency Injection resolution
        self.model_factory: ModelFactory = container.resolve(ModelFactory)
        
        # Lazy load model wrapper mapping to GenAI SDK client
        self.llm = self.model_factory.get_model(config=self.config)
        logger.info(f"Initialized {self.__class__.__name__} with model {config.model_name}")

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """
        The static or dynamic system prompt dictating agent behavior.
        """
        pass

    @abstractmethod
    async def _execute(self, prompt: str, context: Any = None) -> Any:
        """
        Internal execution loop to be overridden by specific agent logic.
        """
        pass

    async def run(self, prompt: str, context: Any = None) -> Any:
        """
        Public entrypoint for the agent. Handles pre/post processing and logging.
        """
        logger.debug(f"{self.__class__.__name__} starting execution with prompt length {len(prompt)}")
        try:
            result = await self._execute(prompt, context)
            logger.debug(f"{self.__class__.__name__} execution completed successfully.")
            return result
        except Exception as e:
            logger.exception(f"{self.__class__.__name__} execution failed.")
            raise
