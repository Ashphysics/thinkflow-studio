# ThinkFlow Studio 🧠

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![Gemini](https://img.shields.io/badge/powered_by-Google_Gemini-orange.svg)
![Documentation](https://img.shields.io/badge/docs-v1.0.0-green)

> A deterministic, multi-agent structured thinking environment designed to transform raw ideas into production-ready execution plans.

[Watch the Demo Video here] <!-- Placeholder for YouTube link -->

![Cover Image](assets/screenshots/cover.png) <!-- Placeholder for cover image -->

---

## 📖 Project Overview

### The Problem Statement
Large Language Models (LLMs) are incredibly powerful at brainstorming, but often fail when asked to produce strict, reliable, multi-step execution plans. When given a complex idea, single-prompt approaches suffer from hallucination, schema drift, and loss of context. Furthermore, modern Agentic API endpoints strictly prohibit flexible/arbitrary JSON schemas (`additionalProperties: true`), making it difficult to inject dynamic thinking frameworks into standard LLM outputs.

### The Solution
**ThinkFlow Studio** solves this by decoupling the cognitive load. Instead of one model doing everything, ThinkFlow uses a **Deterministic Directed Acyclic Graph (DAG) Pipeline**. 
Specialized agents—such as the Idea Analyzer, Critic, and Planner—pass strictly typed Pydantic models to each other. Furthermore, cognitive frameworks (like SWOT or 5 Whys) are removed from system prompts entirely and offloaded to a local **Model Context Protocol (MCP)** server, bypassing strict schema limitations via a specialized dual-schema parsing architecture.

---

## ✨ Features
- 🤖 **Multi-Agent Orchestration**: Specialized agents performing distinct roles (Analyzer, Critic, Framework Selector, Planner).
- 🔗 **MCP Integration**: Fetches structural frameworks dynamically via a local FastMCP `stdio` client.
- 💾 **Local Persistence**: Zero-dependency SQLite store for Session and Long Term Memory.
- 🛡️ **Zero-Trust Security**: Heuristic prompt injection scanning and API key redaction.
- 📊 **Telemetry**: Event-driven execution tracking and latency monitoring via `loguru`.
- 🧪 **CI Evaluation Harness**: Built-in benchmark suite to score schema adherence.
- 🐳 **Docker Ready**: Isolated, reproducible deployment.

---

## 🏗️ Multi-Agent Architecture

![Architecture Diagram](assets/screenshots/architecture.png) <!-- Placeholder for architecture diagram -->

1. **Coordinator**: Intercepts the prompt, validates security, and initiates the DAG pipeline.
2. **Idea Analyzer**: Transforms unstructured natural language into structured target demographics and core goals.
3. **Critic**: Stress-tests the idea, identifying risks, assumptions, and missing information.
4. **Framework Selector**: Interfaces with the MCP Server to retrieve the optimal cognitive framework template (e.g., SWOT, 5 Whys).
5. **Planner**: Compiles the outputs from the Analyzer, Critic, and Framework into an actionable Execution Roadmap.

---

## 💻 Technology Stack

- **Core**: Python 3.12+
- **LLM SDK**: Google GenAI SDK (Gemini Developer API) - `gemini-2.5-flash`
- **Agent Output Structuring**: Pydantic v2
- **UI Framework**: Streamlit
- **Inter-Process Communication**: FastMCP (Model Context Protocol) via `stdio`
- **Data Persistence**: SQLite (Standard Library)
- **Logging**: Loguru

---

## 📁 Folder Structure

```text
thinkflow-studio/
├── app/
│   ├── agents/          # Specialist agent definitions (analyzer, critic, etc.)
│   ├── config/          # Pydantic Settings management
│   ├── core/            # Dependency injection, factories, and BaseAgent
│   ├── evaluation/      # CI benchmark scoring harness
│   ├── mcp/             # FastMCP server and tool registry
│   ├── memory/          # SQLite stores and context managers
│   ├── orchestrator/    # DAG Pipeline orchestration
│   ├── schemas/         # Pydantic I/O models
│   ├── security/        # Input scanners
│   ├── telemetry/       # Secure Logging & Metrics
│   └── ui/              # Streamlit presentation layer (app.py)
├── assets/              # Demo assets (images, videos)
├── docs/                # Comprehensive architecture and developer documentation
├── tests/               # Pytest suite (unit and integration)
└── Dockerfile           # Multi-stage container definition
```

---

## 🚀 Installation & Running

### Environment Variables
ThinkFlow Studio requires a Google Gemini API Key. 

1. Create a `.env` file in the root directory (you can copy the provided example):
```bash
cp .env.example .env
```
2. Add your API key to `.env`:
```env
GOOGLE_API_KEY="your-gemini-api-key-here"
LOG_LEVEL="INFO"
ENVIRONMENT="development"
```

### Running Locally
Requires Python 3.12+.

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit UI:
```bash
python -m streamlit run app/ui/app.py
```
*Note: Make sure to run this from the project root directory.*

### Running with Docker (Recommended)
Ensure you have Docker installed.

1. Build the Docker image:
```bash
docker build -t thinkflow-studio .
```

2. Run the container:
```bash
docker run -p 8501:8501 --env-file .env thinkflow-studio
```
3. Access the UI at `http://localhost:8501`.

---

## 🖥️ Streamlit UI
The user interface is built entirely in Streamlit (`app/ui/app.py`). It features:
- A responsive chat interface for submitting ideas.
- Interactive tabs displaying live agent progress.
- Clean JSON and Markdown rendering for the final Execution Roadmap and Framework output.

![Streamlit UI Screenshot](assets/screenshots/ui_main.png) <!-- Placeholder for UI screenshot -->

---

## 🔌 MCP Server
ThinkFlow uses the **Model Context Protocol (MCP)** to decouple structural frameworks from agent logic. The FastMCP server (`app/mcp/server.py`) runs as a local subprocess and communicates via standard I/O (`stdio_client`). This completely offloads prompt instructions for 7 distinct cognitive frameworks (SWOT, 5 Whys, First Principles, etc.), ensuring agents receive perfectly formatted JSON templates without hallucinating fields.

---

## 🧠 Memory System
- **Session Memory**: Complete Pydantic state blobs are saved to SQLite (`app/memory/sqlite_store.py`), allowing instant UI restoration across server reloads.
- **Long-Term Memory (LTM)**: Passive extraction of high-value metadata (e.g., target domains) for future agent personalization.

---

## 🔐 Security & Telemetry
- **Input Validation**: Hard-capped token limits.
- **Injection Scanning**: RegEx heuristic scanning blocks system-level overrides.
- **Secure Logging**: Intercepts and masks leaked API tokens before they hit `sys.stderr`.
- **Telemetry**: Subscribes to the Event Dispatcher to track exact agent execution times and success rates using `loguru`.

---

## 🛣️ Future Roadmap
- **Vector Search LTM**: Replacing the SQLite exact-match Long-Term Memory with an embedded PgVector store.
- **Human-in-the-Loop (HITL)**: Pausing the pipeline at the Critic phase to ask the user to resolve assumptions before proceeding to the Planner.
- **Dynamic MCP Scaling**: Connecting to remote enterprise MCP servers for live business data retrieval.

---

## 📄 License
This project is licensed under the MIT License. See `LICENSE` for details.

## 🙏 Acknowledgements
Built for the **Google AI Agents Kaggle Competition**. Powered by the highly capable Google GenAI SDK.
