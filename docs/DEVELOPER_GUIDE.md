# Developer Guide

**Version:** 1.0.0  
**Last Updated:** 2026-07-06  

Welcome to the ThinkFlow Studio developer documentation. This guide explains how to extend the platform by adding new agents, creating MCP tools, and debugging the system.

## 1. Adding a New Agent

ThinkFlow's pipeline is a strict Directed Acyclic Graph (DAG). To add a new reasoning step:

1. **Create the Schema**
   Define the Pydantic I/O models in `app/schemas/`. Use strict validation rules.

2. **Create the Agent**
   Subclass `BaseAgent` in `app/agents/my_new_agent.py`:
   ```python
   from app.core.base_agent import BaseAgent
   from app.schemas.my_schema import MyAgentOutput
   from app.agents.agent_registry import agent_registry

   class MyNewAgent(BaseAgent):
       @property
       def system_prompt(self) -> str:
           return "You are a specialized agent..."
       
       async def _execute(self, prompt: str, context: Any = None) -> MyAgentOutput:
           # LLM logic here
           pass
   
   # Register it
   agent_registry.register("my_new_agent", MyNewAgent)
   ```

3. **Update the Pipeline**
   Add your agent to the orchestration sequence in `app/orchestrator/pipeline.py` and update the `WorkflowContext` to hold its state.

## 2. Creating an MCP Tool

MCP Tools provide strictly typed structural frameworks to the LLM.

1. **Define the Tool**
   Create a new class in `app/mcp/tools.py` extending `BaseTool`.
2. **Implement `get_schema()`**
   Provide the JSON schema that the LLM must follow to invoke the tool.
3. **Implement `execute()`**
   Return the empty JSON template.
4. **Register with FastMCP**
   Add it to the server instance in `app/mcp/server.py`.

## 3. Telemetry and Debugging

The system uses event-driven logging. To view agent metrics:
- Ensure `.env` has `LOG_LEVEL="DEBUG"`.
- In the Streamlit UI, open the **Execution Roadmap** tab and expand **Developer Mode**.
- The `ExecutionTracer` automatically calculates latency by subscribing to events via the `EventDispatcher`.

**Note:** Never print API keys. The `SecureLogger` automatically redacts strings matching the Gemini key format, but raw `print()` statements bypass this security measure. Always use `loguru.logger`.
