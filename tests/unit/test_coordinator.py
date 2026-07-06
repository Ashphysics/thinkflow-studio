"""
Unit tests for the Coordinator Agent.
"""

import pytest
import json
from unittest.mock import MagicMock, AsyncMock, patch

from app.core.dependency_container import DependencyContainer, container
from app.core.session_manager import SessionManager
from app.core.model_factory import ModelFactory
from app.config.providers import GoogleProviderConfig
from app.agents.coordinator import CoordinatorAgent
from app.schemas.coordinator import ExecutionPlan, AgentTask

# Mock structures
class MockGenAIResponse:
    def __init__(self, text: str):
        self.text = text

class MockGenAIModels:
    def __init__(self, mock_response_text: str):
        self._mock_text = mock_response_text

    def generate_content(self, **kwargs):
        return MockGenAIResponse(self._mock_text)

class MockGenAIClient:
    def __init__(self, mock_response_text: str):
        self.models = MockGenAIModels(mock_response_text)

def setup_mock_container(mock_plan_json: str):
    """Sets up the DI container with mocked singletons for testing."""
    container.clear()
    
    # Mock Session Manager
    session_manager = SessionManager()
    container.register_singleton(SessionManager, session_manager)
    
    # Mock Model Factory
    mock_model_factory = MagicMock(spec=ModelFactory)
    mock_model_factory.get_model.return_value = {
        "client": MockGenAIClient(mock_plan_json),
        "model_id": "test-model"
    }
    container.register_singleton(ModelFactory, mock_model_factory)

@pytest.mark.asyncio
async def test_coordinator_execution_flow():
    """Verify that Coordinator correctly requests a plan and iterates through tasks."""
    
    mock_plan = {
        "plan_id": "plan-123",
        "estimated_steps": 2,
        "tasks": [
            {
                "task_id": "task-1",
                "target_agent": "mock_agent_1",
                "instruction": "Do step 1",
                "input_payload": {},
                "dependencies": []
            },
            {
                "task_id": "task-2",
                "target_agent": "mock_agent_2",
                "instruction": "Do step 2",
                "input_payload": {},
                "dependencies": ["task-1"]
            }
        ]
    }
    
    setup_mock_container(json.dumps(mock_plan))
    
    config = GoogleProviderConfig(model_name="test-model")
    coordinator = CoordinatorAgent(config=config)
    
    # Run the coordinator
    result_state = await coordinator.run(prompt="Test orchestration")
    
    # Verify State
    assert result_state.status == "completed"
    assert result_state.session_id is not None
    assert len(result_state.completed_tasks) == 2
    assert "task-1" in result_state.completed_tasks
    assert "task-2" in result_state.completed_tasks
    assert "mock_agent_1" in result_state.results["task-1"]["agent"]
    
@pytest.mark.asyncio
async def test_coordinator_dependency_failure():
    """Verify that execution halts if dependencies are not met (e.g. invalid plan)."""
    
    mock_plan_bad_deps = {
        "plan_id": "plan-456",
        "estimated_steps": 1,
        "tasks": [
            {
                "task_id": "task-1",
                "target_agent": "mock_agent",
                "instruction": "Fail me",
                "input_payload": {},
                "dependencies": ["non-existent-task"]
            }
        ]
    }
    
    setup_mock_container(json.dumps(mock_plan_bad_deps))
    
    config = GoogleProviderConfig(model_name="test-model")
    coordinator = CoordinatorAgent(config=config)
    
    result_state = await coordinator.run(prompt="Test bad dependencies")
    
    assert result_state.status == "failed"
    assert "task-1" in result_state.failed_tasks
