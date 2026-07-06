"""
Unit tests for the orchestrator components.
"""

import pytest
from unittest.mock import AsyncMock, patch

from app.orchestrator.context import WorkflowContext
from app.orchestrator.events import dispatcher, WorkflowEvent
from app.orchestrator.pipeline import AgentPipeline
from app.core.exceptions import AgentExecutionError

@pytest.fixture
def clean_dispatcher():
    # Clear subscribers for testing
    dispatcher._subscribers = []
    return dispatcher

def test_workflow_context_to_dict():
    context = WorkflowContext(
        session_id="s1",
        request_id="r1",
        user_prompt="test"
    )
    d = context.to_dict()
    assert d["session_id"] == "s1"
    assert d["idea_analysis"] is None

@patch("app.orchestrator.pipeline.agent_registry")
@pytest.mark.asyncio
async def test_pipeline_failure_halts_execution(mock_registry, clean_dispatcher):
    # Setup mock agent that fails
    mock_agent_instance = AsyncMock()
    mock_agent_instance.run.side_effect = AgentExecutionError("Analyzer failed")
    
    mock_agent_class = AsyncMock(return_value=mock_agent_instance)
    mock_registry.get_agent.return_value = mock_agent_class
    
    pipeline = AgentPipeline(session_id="s1")
    
    events_caught = []
    def on_event(e: WorkflowEvent):
        events_caught.append(e.event_type)
        
    clean_dispatcher.subscribe(on_event)
    
    result = await pipeline.run("Make an app")
    
    # Should halt immediately
    assert result.status == "failed"
    assert "Analyzer failed" in result.error_message
    assert result.idea_analysis is None
    assert result.execution_plan is None
    
    # Check events
    assert "pipeline_started" in events_caught
    assert "agent_failed" in events_caught
    assert "pipeline_completed" not in events_caught
