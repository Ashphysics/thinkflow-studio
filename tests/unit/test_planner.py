"""
Unit tests for the Planner Agent.
"""

import pytest
import json
from unittest.mock import MagicMock
from app.core.dependency_container import container
from app.core.model_factory import ModelFactory
from app.config.providers import GoogleProviderConfig
from app.agents.planner import PlannerAgent
from app.core.exceptions import AgentExecutionError

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
        "idea_analysis": {"title": "App"},
        "critic_analysis": {"risks": ["Risk1"]},
        "framework_selection": {"selected_framework": "swot", "framework_template": {"strengths": []}}
    }

@pytest.mark.asyncio
async def test_planner_missing_context():
    setup_mock_container()
    agent = PlannerAgent(config=GoogleProviderConfig(model_name="test-model"))
    
    with pytest.raises(AgentExecutionError, match="requires 'idea_analysis', 'critic_analysis', and 'framework_selection'"):
        await agent.run("Plan this", context={"idea_analysis": {}})

@pytest.mark.asyncio
async def test_planner_success(valid_context):
    mock_output = {
        "project_title": "App",
        "project_summary": "An App",
        "recommended_strategy": "Iterative",
        "execution_phases": [{"phase_name": "Phase 1", "description": "Design"}],
        "milestones": ["M1"],
        "tasks": ["T1"],
        "priority_order": ["P1"],
        "estimated_duration": "3 months",
        "estimated_difficulty": "Moderate",
        "required_resources": ["Dev"],
        "potential_risks": ["Risk1"],
        "success_metrics": ["100 users"],
        "next_best_action": "Draw wireframes",
        "confidence_score": 0.9,
        "filled_framework": {"strengths": ["Strong design"]}
    }
    setup_mock_container(json.dumps(mock_output))
    
    agent = PlannerAgent(config=GoogleProviderConfig(model_name="test-model"))
    result = await agent.run("Plan this", context=valid_context)
    
    assert result.project_title == "App"
    assert len(result.execution_phases) == 1
    assert result.execution_phases[0].phase_name == "Phase 1"
    assert "strengths" in result.filled_framework

@pytest.mark.asyncio
async def test_planner_api_failure(valid_context):
    setup_mock_container(should_fail=True)
    agent = PlannerAgent(config=GoogleProviderConfig(model_name="test-model"))
    
    with pytest.raises(AgentExecutionError, match="PlannerAgent execution failed"):
        await agent.run("Plan this", context=valid_context)
