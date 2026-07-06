"""
Agent Tools Package for ThinkFlow Studio.

Contains execution tools directly invokable by agents via Gemini function calling.
Includes validation checkers, math calculators, and scratchpad modules.

TODOs:
    - [ ] Implement sandboxed code executors for Python validation steps.
    - [ ] Hook tools dynamically to Google Gen AI SDK FunctionDeclaration structures.
    """

from collections.abc import Callable
from typing import Any


class AgentTool:
    """
    Represents an execution tool wrapper with schema declarations.
    """
    def __init__(self, name: str, description: str, func: Callable[..., Any]) -> None:
        self.name: str = name
        self.description: str = description
        self.func: Callable[..., Any] = func

    def get_declaration(self) -> dict[str, Any]:
        """
        Generates Gemini-compliant FunctionDeclaration schemas.
        """
        # TODO: Autogenerate JSON schema from function type hints
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {}
        }


class ToolRegistry:
    """
    Registry collection holding references to all tools loaded for run sessions.
    """
    def __init__(self) -> None:
        self._tools: dict[str, AgentTool] = {}

    def register(self, tool: AgentTool) -> None:
        """
        Register a new tool.
        """
        self._tools[tool.name] = tool

    def get_all_declarations(self) -> list[dict[str, Any]]:
        """
        Fetch lists of JSON declarations.
        """
        return [tool.get_declaration() for tool in self._tools.values()]
