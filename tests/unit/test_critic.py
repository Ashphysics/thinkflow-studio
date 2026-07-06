"""
Unit tests for the Critic Agent.
"""

import pytest
import json
from unittest.mock import MagicMock
from pydantic import ValidationError

from app.core.dependency_container import container
from app.core.model_factory import ModelFactory
from app.config.providers import GoogleProviderConfig
from app.agents.critic import CriticAgent
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
async def test_critic_success():
    """Verify the critic returns a correctly typed CriticOutput object."""
    
    mock_output = {
        "strengths": ["Clear target audience"],
        "weaknesses": ["No revenue model defined"],
        "risks": ["High competition"],
        "assumptions": ["Teachers will pay for this"],
        "missing_information": ["Pricing"],
        "validation_questions": ["What is the willingness to pay?"],
        "opportunities": ["Expand to university professors"],
        "overall_readiness_score": 0.6,
        "confidence_score": 0.9
    }
    
    setup_mock_container(json.dumps(mock_output))
    
    config = GoogleProviderConfig(model_name="test-model")
    critic = CriticAgent(config=config)
    
    context = {"idea_analysis": {"idea_title": "AI for Teachers"}}
    result = await critic.run(prompt="Evaluate this", context=context)
    
    assert result.overall_readiness_score == 0.6
    assert result.confidence_score == 0.9
    assert len(result.weaknesses) == 1

@pytest.mark.asyncio
async def test_critic_missing_context():
    """Verify critic rejects requests missing the required context payload."""
    setup_mock_container()
    config = GoogleProviderConfig(model_name="test-model")
    critic = CriticAgent(config=config)
    
    with pytest.raises(AgentExecutionError, match="requires an 'idea_analysis' key"):
        await critic.run(prompt="Evaluate this", context={"wrong_key": "data"})

@pytest.mark.asyncio
async def test_critic_api_failure():
    """Verify critic wraps API exceptions correctly."""
    setup_mock_container(should_fail=True)
    config = GoogleProviderConfig(model_name="test-model")
    critic = CriticAgent(config=config)
    
    with pytest.raises(AgentExecutionError, match="CriticAgent execution failed"):
        await critic.run(prompt="Evaluate this", context={"idea_analysis": {"title": "Test"}})
