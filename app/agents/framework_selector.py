"""
Framework Selector Agent.
Responsible strictly for selecting the best MCP thinking framework and retrieving its template.
Does not plan, does not critique, does not summarize.
"""

import time
import json
import sys
from typing import Any, Dict
from loguru import logger
from google.genai import types

from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession

from app.core.base_agent import BaseAgent
from app.core.exceptions import AgentExecutionError
from app.schemas.framework_selection import FrameworkSelectionOutput
from app.agents.agent_registry import agent_registry


class FrameworkSelectorAgent(BaseAgent):
    """
    Analyzes IdeaAnalysis and Critic outputs to select a framework, 
    then retrieves the template from the local MCP server.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are the Framework Selector Agent. "
            "Your ONLY responsibility is to select the most appropriate structured thinking framework "
            "based on the provided Idea Analysis and Critic outputs. "
            "Do NOT generate plans. Do NOT critique the idea. "
            "Choose exactly one of the following exact MCP tool names: "
            "['swot_analysis', 'five_whys', 'first_principles', 'decision_matrix', 'pros_cons', 'smart_goals', 'eisenhower_matrix']. "
            "Provide the 'selected_framework' as the exact tool name string and your reasoning in 'selection_reason'."
        )

    async def _fetch_mcp_template(self, tool_name: str, idea_title: str) -> Dict[str, Any]:
        """
        Connects to the local FastMCP server via STDIO to retrieve the framework template.
        """
        logger.debug(f"[{self.__class__.__name__}] Fetching template from MCP tool: {tool_name}")
        server_params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "app.mcp.server"]
        )
        
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    # Provide minimal generic payload based on typical tool requirements
                    # Tools like swot_analysis expect 'topic'
                    # Tools like five_whys expect 'problem_statement'
                    # Tools like first_principles expect 'complex_problem'
                    tool_args = {
                        "topic": idea_title,
                        "problem_statement": idea_title,
                        "complex_problem": idea_title,
                        "decision_topic": idea_title,
                        "raw_goal": idea_title,
                        "options": ["Option A", "Option B"],
                        "criteria": ["Criteria 1", "Criteria 2"],
                        "tasks": ["Task 1", "Task 2"]
                    }
                    
                    result = await session.call_tool(tool_name, arguments=tool_args)
                    
                    if result.isError:
                        raise AgentExecutionError(f"MCP Tool {tool_name} returned an error: {result.content}")
                    
                    # Ensure content is extracted cleanly; typically JSON string inside text block
                    if not result.content:
                        raise AgentExecutionError(f"MCP Tool {tool_name} returned empty content.")
                        
                    content_str = result.content[0].text
                    
                    try:
                        # Depending on the MCP SDK output format, it might be a JSON string or dict string repr
                        import ast
                        template_dict = ast.literal_eval(content_str) if content_str.startswith("{") else json.loads(content_str)
                        return template_dict
                    except Exception as e:
                        # Fallback parsing
                        return {"raw_template": content_str}
        except Exception as e:
            logger.error(f"[{self.__class__.__name__}] MCP connection or execution failed: {e}")
            raise AgentExecutionError(f"Failed to fetch MCP template: {e}")

    async def _execute(self, prompt: str, context: Any = None) -> FrameworkSelectionOutput:
        """
        Executes the selection using Google Gen AI, then fetches the template.
        """
        if not context or not isinstance(context, dict):
            raise AgentExecutionError("FrameworkSelectorAgent requires a context dictionary.")
            
        idea_analysis = context.get("idea_analysis")
        critic_analysis = context.get("critic_analysis")
        
        if not idea_analysis or not critic_analysis:
            raise AgentExecutionError("FrameworkSelectorAgent requires both 'idea_analysis' and 'critic_analysis' in context.")

        session_id = context.get("session_id", "unknown")
        request_id = context.get("request_id", "unknown")
        start_time = time.time()

        logger.info(f"[{self.__class__.__name__}] Starting framework selection | Session: {session_id} | Request: {request_id}")

        try:
            client = self.llm["client"]
            model_id = self.llm["model_id"]
            
            combined_context = {
                "idea_analysis": idea_analysis,
                "critic_analysis": critic_analysis,
                "user_prompt": prompt
            }
            context_str = json.dumps(combined_context, indent=2)

            # Step 1: LLM Selection
            response = client.models.generate_content(
                model=model_id,
                contents=f"Select the best framework based on this context:\n\n{context_str}",
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    response_mime_type="application/json",
                    response_schema=FrameworkSelectionOutput,
                    temperature=0.0
                )
            )

            selection_data = response.text
            result = FrameworkSelectionOutput.model_validate_json(selection_data)
            
            logger.info(f"[{self.__class__.__name__}] Selected framework: {result.selected_framework}")
            
            # Step 2: Fetch MCP Template
            # We extract title safely; assuming idea_analysis is a dict
            idea_title = idea_analysis.get("idea_title", "Unknown Topic") if isinstance(idea_analysis, dict) else "Unknown Topic"
            
            template = await self._fetch_mcp_template(result.selected_framework, idea_title)
            result.framework_template = template
            
            execution_time = time.time() - start_time
            logger.info(f"[{self.__class__.__name__}] Selection complete | Status: SUCCESS | Time: {execution_time:.2f}s")
            
            return result

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"[{self.__class__.__name__}] Selection failed | Status: ERROR | Time: {execution_time:.2f}s | Error: {e}")
            raise AgentExecutionError(f"FrameworkSelector execution failed: {e}")

# Automatically register the agent when the module is imported
agent_registry.register("framework_selector", FrameworkSelectorAgent)
