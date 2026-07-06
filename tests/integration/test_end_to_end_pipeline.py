"""
End-to-end integration test for the orchestration pipeline.
"""

import pytest
from unittest.mock import AsyncMock, patch

from app.orchestrator.pipeline import AgentPipeline
from app.schemas.idea_analysis import IdeaAnalysisOutput
from app.schemas.critic_analysis import CriticOutput
from app.schemas.framework_selection import FrameworkSelectionOutput
from app.schemas.execution_plan import ExecutionPlanOutput

# We patch the actual agent run methods to return mocked Pydantic objects 
# rather than hitting the LLM or MCP server.

@pytest.mark.asyncio
@patch("app.agents.idea_analyzer.IdeaAnalyzerAgent.run")
@patch("app.agents.critic.CriticAgent.run")
@patch("app.agents.framework_selector.FrameworkSelectorAgent.run")
@patch("app.agents.planner.PlannerAgent.run")
async def test_end_to_end_pipeline_success(
    mock_planner_run,
    mock_selector_run,
    mock_critic_run,
    mock_analyzer_run
):
    from app.core.dependency_container import container
    from app.core.session_manager import SessionManager
    from app.core.model_factory import ModelFactory
    from unittest.mock import MagicMock
    
    container.clear()
    container.register_singleton(SessionManager, SessionManager())
    container.register_singleton(ModelFactory, MagicMock(spec=ModelFactory))
    # Mock return values for each agent in the chain
    mock_analyzer_run.return_value = IdeaAnalysisOutput(
        idea_title="Test", one_sentence_summary="Test", category="Test", 
        domain="Test", primary_goal="Test", target_users=[], assumptions=[], 
        constraints=[], missing_information=[], required_clarifications=[], confidence_score=1.0
    )
    
    mock_critic_run.return_value = CriticOutput(
        strengths=[], weaknesses=[], risks=[], assumptions=[], 
        missing_information=[], validation_questions=[], opportunities=[], 
        overall_readiness_score=1.0, confidence_score=1.0
    )
    
    mock_selector_run.return_value = FrameworkSelectionOutput(
        selected_framework="swot_analysis", selection_reason="test", 
        framework_template={"strengths": []}, confidence_score=1.0
    )
    
    mock_planner_run.return_value = ExecutionPlanOutput(
        project_title="Test", project_summary="Test", recommended_strategy="Test", 
        execution_phases=[], milestones=[], tasks=[], priority_order=[], 
        estimated_duration="Test", estimated_difficulty="Test", required_resources=[], 
        potential_risks=[], success_metrics=[], next_best_action="Test", 
        confidence_score=1.0, filled_framework={}
    )

    # Initialize the pipeline
    pipeline = AgentPipeline()
    result = await pipeline.run("Test prompt")
    
    # Assert pipeline completes successfully and state is fully populated
    assert result.status == "completed"
    assert result.idea_analysis is not None
    assert result.critic_analysis is not None
    assert result.framework_selection is not None
    assert result.execution_plan is not None
    assert result.execution_plan.project_title == "Test"
    
    # Assert the execution logs recorded all 4 agents
    assert len(result.execution_logs) == 4
    assert result.execution_logs[-1]["agent"] == "planner"
    assert result.execution_logs[-1]["status"] == "success"
