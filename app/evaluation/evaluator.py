"""
Evaluator for measuring pipeline schema adherence and execution score.
"""
from app.orchestrator.context import WorkflowContext

class PipelineEvaluator:
    @classmethod
    def evaluate(cls, context: WorkflowContext) -> dict:
        """
        Calculates execution score and schema validation metrics for a completed context.
        """
        score = 0
        total_possible = 40
        
        # Schema validation score
        schema_points = 0
        if context.idea_analysis: schema_points += 10
        if context.critic_analysis: schema_points += 10
        if context.framework_selection: schema_points += 10
        if context.execution_plan: schema_points += 10
        
        score += schema_points
        
        # Latency penalty (assume > 30s is bad)
        latency = (context.end_time or 0) - (context.start_time or 0)
        latency_penalty = 0
        if latency > 30:
            latency_penalty = 10
            
        final_score = max(0, score - latency_penalty)
        
        return {
            "execution_score": final_score,
            "max_score": total_possible,
            "schema_validation_score": schema_points,
            "latency": latency,
            "pipeline_completion": context.status == "completed"
        }
