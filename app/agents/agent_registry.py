"""
Simple registry for agent discovery.
"""

from typing import Dict, Type
from loguru import logger
from app.core.base_agent import BaseAgent

class AgentRegistry:
    """
    A lightweight registry mapping string identifiers to concrete agent classes.
    Prevents circular imports and decouples the Coordinator from specific implementations.
    """
    def __init__(self) -> None:
        self._registry: Dict[str, Type[BaseAgent]] = {}

    def register(self, name: str, agent_class: Type[BaseAgent]) -> None:
        """Registers a new agent class under a string identifier."""
        if name in self._registry:
            logger.warning(f"Overwriting agent registration for '{name}'.")
        self._registry[name] = agent_class
        logger.debug(f"Registered agent: {name}")

    def unregister(self, name: str) -> None:
        """Unregisters an agent by name."""
        if name in self._registry:
            del self._registry[name]
            logger.debug(f"Unregistered agent: {name}")

    def get_agent(self, name: str) -> Type[BaseAgent]:
        """Retrieves an agent class by its string identifier."""
        if name not in self._registry:
            logger.error(f"Agent '{name}' not found in registry.")
            raise KeyError(f"Agent '{name}' is not registered.")
        return self._registry[name]

    def list_agents(self) -> list[str]:
        """Returns a list of all registered agent identifiers."""
        return list(self._registry.keys())

# Global singleton instance of the registry
agent_registry = AgentRegistry()
