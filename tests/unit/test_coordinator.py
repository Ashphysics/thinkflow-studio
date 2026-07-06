"""
Unit tests for the Coordinator Agent.
"""

import pytest
from unittest.mock import AsyncMock, patch
from app.config.providers import ProviderFactory
from app.agents.coordinator import CoordinatorAgent
from app.orchestrator.context import WorkflowContext
from unittest.mock import MagicMock
from app.core.dependency_container import container
from app.core.session_manager import SessionManager
from app.core.model_factory import ModelFactory

def setup_mock_container():
    container.clear()
    container.register_singleton(SessionManager, SessionManager())
    container.register_singleton(ModelFactory, MagicMock(spec=ModelFactory))


@pytest.mark.asyncio
@patch("app.orchestrator.pipeline.AgentPipeline")
async def test_coordinator_execution_flow(MockPipeline):
    """Verify that Coordinator correctly delegates to AgentPipeline."""
    
    # Setup mock pipeline behavior
    mock_pipeline_instance = AsyncMock()
    mock_context = WorkflowContext(session_id="s123", request_id="req1", user_prompt="Test", status="completed")
    mock_pipeline_instance.run.return_value = mock_context
    MockPipeline.return_value = mock_pipeline_instance
    
    setup_mock_container()
    config = ProviderFactory.create_google_config("test-model")
    coordinator = CoordinatorAgent(config=config)
    
    # Run the coordinator
    result = await coordinator.run(prompt="Test orchestration", context={"session_id": "s123"})
    
    # Verify State
    assert result.status == "completed"
    assert result.session_id == "s123"

@pytest.mark.asyncio
@patch("app.orchestrator.pipeline.AgentPipeline")
async def test_coordinator_dependency_failure(MockPipeline):
    """Verify that execution halts and errors are propagated if pipeline fails."""
    
    mock_pipeline_instance = AsyncMock()
    mock_context = WorkflowContext(session_id="s123", request_id="req1", user_prompt="Test", status="failed", error_message="Internal pipeline error")
    mock_pipeline_instance.run.return_value = mock_context
    MockPipeline.return_value = mock_pipeline_instance
    
    setup_mock_container()
    config = ProviderFactory.create_google_config("test-model")
    coordinator = CoordinatorAgent(config=config)
    
    from app.core.exceptions import AgentExecutionError
    
    with pytest.raises(AgentExecutionError) as exc_info:
        await coordinator.run(prompt="Test failure", context={"session_id": "s123"})
    
    assert "Internal pipeline error" in str(exc_info.value)

