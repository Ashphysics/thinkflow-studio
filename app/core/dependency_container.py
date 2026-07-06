"""
Lightweight custom Dependency Injection Container.
Provides singleton and factory registration without external framework overhead.
"""

from typing import Callable, Dict, Type, Any
from app.core.exceptions import DependencyError
from app.core.types import T
from loguru import logger

class DependencyContainer:
    """
    A simple Inversion of Control (IoC) container for dependency injection.
    Supports singletons and factories.
    """
    _instance = None
    
    def __new__(cls) -> "DependencyContainer":
        if cls._instance is None:
            cls._instance = super(DependencyContainer, cls).__new__(cls)
            cls._instance._singletons = {}  # type: ignore
            cls._instance._factories = {}  # type: ignore
        return cls._instance

    def __init__(self) -> None:
        # Avoid re-initialization in __new__ singleton
        if not hasattr(self, "_singletons"):
            self._singletons: Dict[Type[Any], Any] = {}
            self._factories: Dict[Type[Any], Callable[[], Any]] = {}

    def register_singleton(self, interface: Type[T], instance: T) -> None:
        """
        Registers an already instantiated object as a singleton.
        """
        if interface in self._singletons:
            logger.warning(f"Overwriting singleton for {interface}")
        self._singletons[interface] = instance
        logger.debug(f"Registered singleton for {interface}")

    def register_factory(self, interface: Type[T], factory: Callable[[], T]) -> None:
        """
        Registers a factory function that creates a new instance each time.
        """
        self._factories[interface] = factory
        logger.debug(f"Registered factory for {interface}")

    def resolve(self, interface: Type[T]) -> T:
        """
        Resolves a dependency by its interface type.
        Prioritizes singletons, then falls back to factories.
        """
        if interface in self._singletons:
            return self._singletons[interface]
            
        if interface in self._factories:
            return self._factories[interface]()
            
        logger.error(f"Failed to resolve dependency: {interface}")
        raise DependencyError(f"No registration found for {interface}")

    def clear(self) -> None:
        """
        Clears all registered dependencies. Useful for testing.
        """
        self._singletons.clear()
        self._factories.clear()

# Global container instance
container = DependencyContainer()
