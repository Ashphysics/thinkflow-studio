"""
Tests for evaluation metrics.
"""
from app.evaluation.evaluator import PipelineEvaluator
from app.orchestrator.context import WorkflowContext

def test_evaluation_scorer():
    context = WorkflowContext(
        session_id="eval1",
        request_id="req1",
        user_prompt="test",
        status="completed",
        start_time=100.0,
        end_time=115.0 # 15s duration (no penalty)
    )
    # Give it one schema element to test partial score
    from app.schemas.idea_analysis import IdeaAnalysisOutput
    context.idea_analysis = IdeaAnalysisOutput(
        idea_title="", one_sentence_summary="", category="", domain="",
        primary_goal="", target_users=[], assumptions=[], constraints=[],
        missing_information=[], required_clarifications=[], confidence_score=1.0
    )
    
    score = PipelineEvaluator.evaluate(context)
    
    # Max is 40. We only provided idea_analysis (10 points). 
    assert score["schema_validation_score"] == 10
    assert score["execution_score"] == 10
    assert score["latency"] == 15.0

def test_evaluation_latency_penalty():
    context = WorkflowContext(
        session_id="eval2",
        request_id="req2",
        user_prompt="test",
        status="failed",
        start_time=100.0,
        end_time=145.0 # 45s duration (10 pt penalty)
    )
    
    score = PipelineEvaluator.evaluate(context)
    
    assert score["schema_validation_score"] == 0
    # Score 0 - 10 penalty but bounded to 0
    assert score["execution_score"] == 0
    assert score["latency"] == 45.0
