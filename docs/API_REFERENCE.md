# API Reference

**Version:** 1.0.0  
**Last Updated:** 2026-07-06  

This document outlines the public interfaces for ThinkFlow Studio's core architectural components.

---

## 1. Orchestration

### `AgentPipeline` (app/orchestrator/pipeline.py)
The deterministic DAG execution engine.

- **`execute(prompt: str) -> WorkflowContext`**
  - **Description**: Initiates the full pipeline execution given a user prompt. Handles state transitions and intercepts fatal exceptions.
  - **Returns**: A fully populated `WorkflowContext` containing the outputs of all agents.

---

## 2. Context & Schemas

### `WorkflowContext` (app/schemas/context.py)
The state object passed between agents and serialized to SQLite.

- **Properties**:
  - `session_id` (str): Unique identifier.
  - `user_prompt` (str): Original input.
  - `idea_analysis` (IdeaAnalysisOutput | None)
  - `critic_analysis` (CriticOutput | None)
  - `framework_selection` (FrameworkSelectionOutput | None)
  - `execution_plan` (ExecutionPlanOutput | None)
  - `status` (str): "running", "completed", or "failed".

---

## 3. Core Agent Protocol

### `BaseAgent` (app/core/base_agent.py)
The abstract base class for all specialist agents.

- **`execute(prompt: str, context: Any = None) -> Any`**
  - **Description**: Public interface for invoking an agent. Handles telemetry wrapping and exception handling.
- **`system_prompt` (property)**
  - **Description**: Must be overridden by subclasses to provide strict instructions to the LLM.

---

## 4. MCP Tools

### `BaseTool` (app/mcp/base.py)
The abstract base class for structural frameworks.

- **`execute(**kwargs) -> Dict[str, Any]`**
  - **Description**: Executes the tool logic. For frameworks, it typically returns an empty, typed JSON template (e.g., SWOT, 5 Whys).
- **`get_schema() -> Dict[str, Any]`**
  - **Description**: Returns the JSON schema representing the expected inputs for the tool.

---

## 5. Dependency Injection

### `DependencyContainer` (app/core/di.py)
Provides singleton access to shared services.

- **`register(interface: Type, instance: Any) -> None`**
  - **Description**: Binds a service instance to an interface type.
- **`resolve(interface: Type) -> Any`**
  - **Description**: Retrieves the singleton instance. Used to access the `ModelFactory` and `MemoryService`.

---

## 6. Models & Memory

### `ModelFactory` (app/core/model_factory.py)
Manages the Google GenAI SDK client instantiation.

- **`get_client() -> genai.Client`**
  - **Description**: Returns the initialized Gemini client.
- **`get_model_id() -> str`**
  - **Description**: Returns the configured model identifier (e.g., `gemini-2.5-flash`).

### `MemoryService` (app/memory/sqlite_store.py)
Handles SQLite persistence.

- **`save_context(context: WorkflowContext) -> None`**
- **`load_context(session_id: str) -> WorkflowContext | None`**
- **`extract_long_term_knowledge(context: WorkflowContext) -> None`**
