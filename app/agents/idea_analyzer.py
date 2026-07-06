"""
Idea Analyzer Agent.
Responsible strictly for parsing unstructured user intent into structured JSON.
Does not plan, does not criticize, does not call MCP tools.
"""

import time
from typing import Any, Dict
from loguru import logger
from google.genai import types

from app.core.base_agent import BaseAgent
from app.core.exceptions import AgentExecutionError
from app.schemas.idea_analysis import IdeaAnalysisOutput
from app.agents.agent_registry import agent_registry


class IdeaAnalyzerAgent(BaseAgent):
    """
    Analyzes raw user ideas into a strongly typed structural object.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are the Idea Analyzer Agent. "
            "Your ONLY responsibility is to understand and categorize the user's raw idea. "
            "Do NOT criticize the idea. Do NOT generate execution plans. Do NOT invent features. "
            "Extract the domain, target users, assumptions, and constraints. "
            "If information is missing, note it in `missing_information` and `required_clarifications`. "
            "Always return your analysis strictly matching the requested JSON schema."
        )

    async def _execute(self, prompt: str, context: Any = None) -> IdeaAnalysisOutput:
        """
        Executes the analysis using Google Gen AI structured outputs.
        """
        if not prompt or not prompt.strip():
            raise AgentExecutionError("Input prompt cannot be empty.")

        session_id = context.get("session_id", "unknown") if isinstance(context, dict) else "unknown"
        request_id = context.get("request_id", "unknown") if isinstance(context, dict) else "unknown"
        start_time = time.time()

        logger.info(f"[{self.__class__.__name__}] Starting analysis | Session: {session_id} | Request: {request_id}")

        try:
            client = self.llm["client"]
            model_id = self.llm["model_id"]
            
            # Use strict schema generation via Gemini GenAI
            response = client.models.generate_content(
                model=model_id,
                contents=f"Analyze the following user idea:\n\n{prompt}",
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    response_mime_type="application/json",
                    response_schema=IdeaAnalysisOutput,
                    temperature=0.0 # Deterministic structural extraction
                )
            )

            # Parse and validate the response
            analysis_data = response.text
            result = IdeaAnalysisOutput.model_validate_json(analysis_data)
            
            execution_time = time.time() - start_time
            logger.info(f"[{self.__class__.__name__}] Analysis complete | Status: SUCCESS | Time: {execution_time:.2f}s")
            
            return result

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"[{self.__class__.__name__}] Analysis failed | Status: ERROR | Time: {execution_time:.2f}s | Error: {e}")
            raise AgentExecutionError(f"IdeaAnalyzer execution failed: {e}")

# Automatically register the agent when the module is imported
agent_registry.register("analyzer", IdeaAnalyzerAgent)
