"""
Coordinator Agent for ThinkFlow Studio.
Acts as the entry point to the deterministic ideation pipeline.
"""

from typing import Any
from loguru import logger

from app.core.base_agent import BaseAgent
from app.core.exceptions import AgentExecutionError
from app.orchestrator.pipeline import AgentPipeline

class CoordinatorAgent(BaseAgent):
    """
    The main entry point.
    Delegates execution to the AgentPipeline which orchestrates the sequence:
    Analyzer -> Critic -> Framework Selector -> Planner.
    """

    @property
    def system_prompt(self) -> str:
        return "Coordinator routing logic is now handled deterministically by the orchestrator pipeline."

    async def _execute(self, prompt: str, context: Any = None) -> Any:
        """
        Initializes and runs the orchestration pipeline.
        """
        session_id = context.get("session_id") if isinstance(context, dict) else None
        
        logger.info(f"[CoordinatorAgent] Dispatching request to orchestration pipeline | Session: {session_id}")
        
        try:
            pipeline = AgentPipeline(session_id=session_id)
            result = await pipeline.run(prompt)
            
            if result.status == "failed":
                logger.error(f"[CoordinatorAgent] Pipeline execution failed: {result.error_message}")
                raise AgentExecutionError(f"Pipeline failed: {result.error_message}")
                
            return result
            
        except Exception as e:
            logger.exception("[CoordinatorAgent] Failed to execute pipeline.")
            raise AgentExecutionError(f"Coordinator dispatch failed: {e}")
