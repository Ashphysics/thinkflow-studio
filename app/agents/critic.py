"""
Critic Agent.
Responsible strictly for evaluating the output of the Idea Analyzer.
Does not plan, does not reject ideas, does not call MCP tools.
"""

import time
import json
from typing import Any
from loguru import logger
from google.genai import types

from app.core.base_agent import BaseAgent
from app.core.exceptions import AgentExecutionError
from app.schemas.critic_analysis import CriticOutput
from app.agents.agent_registry import agent_registry


class CriticAgent(BaseAgent):
    """
    Evaluates a structured IdeaAnalysisOutput and returns a CriticOutput.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are the Critic Agent. "
            "Your ONLY responsibility is to evaluate the provided structured idea analysis. "
            "Do NOT reject the idea. Do NOT generate execution plans. "
            "Identify strengths, weaknesses, hidden assumptions, potential risks, missing information, "
            "opportunities, and critical validation questions. "
            "Always return your critique strictly matching the requested JSON schema."
        )

    async def _execute(self, prompt: str, context: Any = None) -> CriticOutput:
        """
        Executes the critique using Google Gen AI structured outputs.
        """
        if not context or not isinstance(context, dict) or "idea_analysis" not in context:
            raise AgentExecutionError("CriticAgent requires an 'idea_analysis' key in the context payload.")

        idea_analysis = context["idea_analysis"]
        if not idea_analysis:
            raise AgentExecutionError("Provided 'idea_analysis' is empty.")

        session_id = context.get("session_id", "unknown")
        request_id = context.get("request_id", "unknown")
        start_time = time.time()

        logger.info(f"[{self.__class__.__name__}] Starting critique | Session: {session_id} | Request: {request_id}")

        try:
            client = self.llm["client"]
            model_id = self.llm["model_id"]
            
            # Convert context to string to pass to the LLM
            idea_analysis_str = json.dumps(idea_analysis, indent=2) if isinstance(idea_analysis, dict) else str(idea_analysis)

            # Use strict schema generation via Gemini GenAI
            response = client.models.generate_content(
                model=model_id,
                contents=f"Critique the following structured idea analysis:\n\n{idea_analysis_str}\n\nUser prompt context: {prompt}",
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    response_mime_type="application/json",
                    response_schema=CriticOutput,
                    temperature=0.0 # Deterministic structural evaluation
                )
            )

            # Parse and validate the response
            critique_data = response.text
            result = CriticOutput.model_validate_json(critique_data)
            
            execution_time = time.time() - start_time
            logger.info(f"[{self.__class__.__name__}] Critique complete | Status: SUCCESS | Time: {execution_time:.2f}s")
            
            return result

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"[{self.__class__.__name__}] Critique failed | Status: ERROR | Time: {execution_time:.2f}s | Error: {e}")
            raise AgentExecutionError(f"CriticAgent execution failed: {e}")

# Automatically register the agent when the module is imported
agent_registry.register("critic", CriticAgent)
