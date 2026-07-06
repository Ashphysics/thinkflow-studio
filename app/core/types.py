"""
Type definitions and protocols for the core infrastructure.
"""

from typing import Any, Callable, Dict, TypeVar, Coroutine

# Type Variables for generics
T = TypeVar("T")

# General Types
JsonDict = Dict[str, Any]

# Async Function Types
AsyncCallback = Callable[..., Coroutine[Any, Any, Any]]
