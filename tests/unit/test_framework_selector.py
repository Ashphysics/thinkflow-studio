"""
Unit tests for the Framework Selector Agent.
"""

import pytest
import json
from unittest.mock import MagicMock, AsyncMock, patch

from app.core.dependency_container import container
from app.core.model_factory import ModelFactory
from app.config.providers import GoogleProviderConfig
from app.agents.framework_selector import FrameworkSelectorAgent
from app.core.exceptions import AgentExecutionError

# Mock GenAI Structures
class MockGenAIResponse:
    def __init__(self, text: str):
        self.text = text

class MockGenAIModels:
    def __init__(self, mock_response_text: str = "", should_fail: bool = False):
        self._mock_text = mock_response_text
        self._should_fail = should_fail

    def generate_content(self, **kwargs):
        if self._should_fail:
            raise Exception("Mocked API Timeout")
        return MockGenAIResponse(self._mock_text)

class MockGenAIClient:
    def __init__(self, mock_response_text: str = "", should_fail: bool = False):
        self.models = MockGenAIModels(mock_response_text, should_fail)

def setup_mock_container(mock_response_json: str = "", should_fail: bool = False):
    """Sets up the DI container with mocked ModelFactory."""
    container.clear()
    
    mock_model_factory = MagicMock(spec=ModelFactory)
    mock_model_factory.get_model.return_value = {
        "client": MockGenAIClient(mock_response_json, should_fail),
        "model_id": "test-model"
    }
    container.register_singleton(ModelFactory, mock_model_factory)

@pytest.fixture
def valid_context():
    return {
        "idea_analysis": {"idea_title": "AI App"},
        "critic_analysis": {"weaknesses": ["None"]}
    }

@pytest.mark.asyncio
async def test_framework_selector_missing_context():
    setup_mock_container()
    agent = FrameworkSelectorAgent(config=GoogleProviderConfig(model_name="test-model"))
    
    with pytest.raises(AgentExecutionError, match="requires both 'idea_analysis' and 'critic_analysis'"):
        await agent.run("Select framework", context={"idea_analysis": {}})

@patch("app.agents.framework_selector.stdio_client")
@patch("app.agents.framework_selector.ClientSession")
@pytest.mark.asyncio
async def test_framework_selector_success(mock_session_cls, mock_stdio_client, valid_context):
    mock_output = {
        "selected_framework": "swot_analysis",
        "selection_reason": "Good for strategic planning",
        "framework_template": {},
        "confidence_score": 0.95
    }
    setup_mock_container(json.dumps(mock_output))
    
    # Mocking MCP Async Context Managers
    mock_stdio_cm = AsyncMock()
    mock_stdio_client.return_value = mock_stdio_cm
    mock_stdio_cm.__aenter__.return_value = (AsyncMock(), AsyncMock())
    
    mock_session_cm = AsyncMock()
    mock_session_cls.return_value = mock_session_cm
    mock_session_instance = AsyncMock()
    mock_session_cm.__aenter__.return_value = mock_session_instance
    
    mock_tool_result = MagicMock()
    mock_tool_result.isError = False
    mock_content = MagicMock()
    mock_content.text = '{"strengths": []}'
    mock_tool_result.content = [mock_content]
    
    mock_session_instance.call_tool = AsyncMock(return_value=mock_tool_result)

    agent = FrameworkSelectorAgent(config=GoogleProviderConfig(model_name="test-model"))
    result = await agent.run(prompt="Select", context=valid_context)
    
    assert result.selected_framework == "swot_analysis"
    assert result.framework_template == {"strengths": []}
    mock_session_instance.call_tool.assert_called_once()
