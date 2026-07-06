"""
Planner Agent.
Responsible strictly for translating analyzed contexts into a structured execution roadmap.
Does not critique, does not fetch MCP tools.
"""

import time
import json
from typing import Any
from loguru import logger
from google.genai import types

from app.core.base_agent import BaseAgent
from app.core.exceptions import AgentExecutionError
from app.schemas.execution_plan import ExecutionPlanOutput, LLMExecutionPlanOutput
from app.agents.agent_registry import agent_registry


class PlannerAgent(BaseAgent):
    """
    Synthesizes IdeaAnalysis, CriticAnalysis, and FrameworkSelection 
    to output a final structured execution plan.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are the Planner Agent. "
            "Your ONLY responsibility is to create an actionable, structured execution plan. "
            "Do NOT critique the idea yourself; rely strictly on the provided Critic Analysis. "
            "Do NOT choose new frameworks; rely strictly on the provided Framework Selection. "
            "Your task is to populate the 'ExecutionPlanOutput' schema. "
            "You MUST also fill in the 'filled_framework' field by populating the empty JSON template "
            "provided in the Framework Selection context using the project details."
        )

    async def _execute(self, prompt: str, context: Any = None) -> ExecutionPlanOutput:
        """
        Executes the planning phase using Google Gen AI.
        """
        if not context or not isinstance(context, dict):
            raise AgentExecutionError("PlannerAgent requires a context dictionary.")
            
        idea_analysis = context.get("idea_analysis")
        critic_analysis = context.get("critic_analysis")
        framework_selection = context.get("framework_selection")
        
        if not idea_analysis or not critic_analysis or not framework_selection:
            raise AgentExecutionError(
                "PlannerAgent requires 'idea_analysis', 'critic_analysis', and "
                "'framework_selection' in the context payload."
            )

        session_id = context.get("session_id", "unknown")
        request_id = context.get("request_id", "unknown")
        start_time = time.time()

        framework_used = "unknown"
        if isinstance(framework_selection, dict):
            framework_used = framework_selection.get("selected_framework", "unknown")

        logger.info(
            f"[{self.__class__.__name__}] Starting planning phase | "
            f"Session: {session_id} | "
            f"Framework Used: {framework_used}"
        )

        try:
            client = self.llm["client"]
            model_id = self.llm["model_id"]
            
            combined_context = {
                "idea_analysis": idea_analysis,
                "critic_analysis": critic_analysis,
                "framework_selection": framework_selection,
                "user_prompt": prompt
            }
            context_str = json.dumps(combined_context, indent=2)

            # Generate structured roadmap
            response = client.models.generate_content(
                model=model_id,
                contents=f"Generate the execution plan based on this verified context:\n\n{context_str}",
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    response_mime_type="application/json",
                    response_schema=LLMExecutionPlanOutput,
                    temperature=0.1
                )
            )

            plan_data = response.text
            llm_result = LLMExecutionPlanOutput.model_validate_json(plan_data)
            
            # Parse the stringified JSON framework
            filled_dict = {}
            if llm_result.filled_framework_json:
                try:
                    filled_dict = json.loads(llm_result.filled_framework_json)
                except Exception as e:
                    logger.warning(f"[{self.__class__.__name__}] Failed to parse filled_framework_json: {e}")
                    filled_dict = {"raw": llm_result.filled_framework_json}

            result = ExecutionPlanOutput(
                project_title=llm_result.project_title,
                project_summary=llm_result.project_summary,
                recommended_strategy=llm_result.recommended_strategy,
                execution_phases=llm_result.execution_phases,
                milestones=llm_result.milestones,
                tasks=llm_result.tasks,
                priority_order=llm_result.priority_order,
                estimated_duration=llm_result.estimated_duration,
                estimated_difficulty=llm_result.estimated_difficulty,
                required_resources=llm_result.required_resources,
                potential_risks=llm_result.potential_risks,
                success_metrics=llm_result.success_metrics,
                next_best_action=llm_result.next_best_action,
                confidence_score=llm_result.confidence_score,
                filled_framework=filled_dict
            )
            
            execution_time = time.time() - start_time
            logger.info(
                f"[{self.__class__.__name__}] Planning complete | "
                f"Session: {session_id} | "
                f"Planner Version: 1.0.0 | "
                f"Framework Used: {framework_used} | "
                f"Status: SUCCESS | "
                f"Time: {execution_time:.2f}s"
            )
            
            return result

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"[{self.__class__.__name__}] Planning failed | "
                f"Session: {session_id} | "
                f"Status: ERROR | "
                f"Time: {execution_time:.2f}s | "
                f"Error: {e}"
            )
            raise AgentExecutionError(f"PlannerAgent execution failed: {e}")

# Automatically register the agent when the module is imported
agent_registry.register("planner", PlannerAgent)
