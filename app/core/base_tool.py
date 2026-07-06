"""
Abstract Base Tool definition aligning with Google ADK parameters.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Type
from pydantic import BaseModel
from loguru import logger

class BaseTool(ABC):
    """
    Abstract Base Class for all executable tools in ThinkFlow Studio.
    Forces strict typing and schema definitions for Google GenAI compatibility.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """
        The name of the tool as passed to the LLM.
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Detailed description of what the tool does, used by the agent to decide when to call it.
        """
        pass

    @property
    @abstractmethod
    def input_schema(self) -> Type[BaseModel]:
        """
        Pydantic model representing the expected arguments for the tool.
        """
        pass

    @abstractmethod
    async def invoke(self, **kwargs: Any) -> Any:
        """
        The actual business logic of the tool.
        Must accept kwargs mapping to the `input_schema` fields.
        """
        pass

    async def __call__(self, **kwargs: Any) -> Any:
        """
        Allows the tool instance to be called directly.
        Adds validation wrapping around `invoke()`.
        """
        try:
            # Validate kwargs using the input schema
            validated_input = self.input_schema(**kwargs)
            logger.debug(f"Invoking tool '{self.name}' with args: {validated_input.model_dump()}")
            
            return await self.invoke(**validated_input.model_dump())
        except Exception as e:
            logger.exception(f"Error executing tool '{self.name}'")
            raise e
