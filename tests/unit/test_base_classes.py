"""
Unit tests for abstract base classes ensuring they enforce contracts.
"""

import pytest
from pydantic import BaseModel
from typing import Any
from app.core.base_tool import BaseTool

class DummySchema(BaseModel):
    query: str

class MockTool(BaseTool):
    @property
    def name(self) -> str:
        return "mock_tool"
        
    @property
    def description(self) -> str:
        return "A mock tool for testing."
        
    @property
    def input_schema(self):
        return DummySchema
        
    async def invoke(self, **kwargs: Any) -> Any:
        return f"Executed with {kwargs.get('query')}"

@pytest.mark.asyncio
async def test_mock_tool_execution():
    """Verify standard tool invocation handles Pydantic schemas properly."""
    tool = MockTool()
    assert tool.name == "mock_tool"
    
    # Using the __call__ override
    result = await tool(query="hello world")
    assert result == "Executed with hello world"
