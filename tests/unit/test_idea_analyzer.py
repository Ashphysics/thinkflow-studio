"""
Unit tests for the Idea Analyzer Agent.
"""

import pytest
import json
from unittest.mock import MagicMock, AsyncMock, patch
from pydantic import ValidationError

from app.core.dependency_container import container
from app.core.model_factory import ModelFactory
from app.config.providers import GoogleProviderConfig
from app.agents.idea_analyzer import IdeaAnalyzerAgent
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

@pytest.mark.asyncio
async def test_idea_analyzer_success():
    """Verify the analyzer returns a correctly typed IdeaAnalysisOutput object."""
    
    mock_output = {
        "idea_title": "AI for Teachers",
        "one_sentence_summary": "A startup building AI tools for educators.",
        "category": "SaaS",
        "domain": "Education",
        "primary_goal": "Help teachers grade faster",
        "target_users": ["High School Teachers"],
        "assumptions": ["Teachers have internet"],
        "constraints": ["Budget"],
        "missing_information": ["Pricing model"],
        "required_clarifications": ["What subjects?"],
        "confidence_score": 0.85
    }
    
    setup_mock_container(json.dumps(mock_output))
    
    config = GoogleProviderConfig(model_name="test-model")
    analyzer = IdeaAnalyzerAgent(config=config)
    
    result = await analyzer.run("I want to build an AI startup for teachers.")
    
    assert result.idea_title == "AI for Teachers"
    assert result.confidence_score == 0.85
    assert len(result.target_users) == 1

@pytest.mark.asyncio
async def test_idea_analyzer_empty_input():
    """Verify analyzer rejects empty input immediately."""
    setup_mock_container()
    config = GoogleProviderConfig(model_name="test-model")
    analyzer = IdeaAnalyzerAgent(config=config)
    
    with pytest.raises(AgentExecutionError, match="cannot be empty"):
        await analyzer.run("   ")

@pytest.mark.asyncio
async def test_idea_analyzer_api_failure():
    """Verify analyzer wraps API exceptions correctly."""
    setup_mock_container(should_fail=True)
    config = GoogleProviderConfig(model_name="test-model")
    analyzer = IdeaAnalyzerAgent(config=config)
    
    with pytest.raises(AgentExecutionError, match="IdeaAnalyzer execution failed"):
        await analyzer.run("Valid prompt but API fails.")
