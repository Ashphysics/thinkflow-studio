# ThinkFlow Studio 🧠

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![Gemini](https://img.shields.io/badge/powered_by-Google_Gemini-orange.svg)

> A deterministic, multi-agent structured thinking environment designed to transform raw ideas into production-ready execution plans.

![Cover Image](assets/screenshots/cover.png)

## Overview

### Problem Statement
Large Language Models (LLMs) are incredibly powerful at brainstorming, but often fail when asked to produce strict, reliable, multi-step execution plans. When given a complex idea, single-prompt approaches suffer from hallucination, schema drift, and loss of context. 

### The Solution
**ThinkFlow Studio** solves this by decoupling the cognitive load. Instead of one model doing everything, ThinkFlow uses a **Deterministic Directed Acyclic Graph (DAG) Pipeline**. Specialized agents—such as the Idea Analyzer, Critic, and Planner—pass strictly typed Pydantic models to each other. Furthermore, cognitive frameworks (like SWOT or 5 Whys) are removed from system prompts entirely and offloaded to a local **Model Context Protocol (MCP)** server.

## Features
- 🤖 **Multi-Agent Orchestration**: Specialized agents performing distinct roles.
- 🔗 **MCP Integration**: Fetches structural frameworks via local FastMCP stdio.
- 💾 **Local Persistence**: Zero-dependency SQLite store for Session and Long Term Memory.
- 🛡️ **Zero-Trust Security**: Heuristic prompt injection scanning and API key redaction.
- 📊 **Telemetry**: Event-driven execution tracking and latency monitoring.
- 🧪 **CI Evaluation Harness**: Built-in benchmark suite to score schema adherence.
- 🐳 **Docker Ready**: One-click deployment.

---

## Architecture Diagram

![Architecture](assets/screenshots/architecture.png)

### Agent Responsibilities
1. **Coordinator**: Intercepts the prompt and initiates the DAG pipeline.
2. **Idea Analyzer**: Transforms unstructured natural language into structured target demographics and core goals.
3. **Critic**: Stress-tests the idea, identifying risks, assumptions, and missing information.
4. **Framework Selector**: Interfaces with the MCP Server to retrieve the optimal cognitive framework template (e.g., SWOT).
5. **Planner**: Compiles the outputs from the Analyzer, Critic, and Framework into an actionable Execution Roadmap.

### MCP Integration
ThinkFlow uses the Model Context Protocol (MCP) to decouple structural frameworks from agent logic. The FastMCP server runs as a local subprocess and communicates via standard I/O, ensuring agents receive perfectly formatted JSON templates without hallucinating fields.

### Memory
- **Session Memory**: Complete Pydantic state blobs are saved to SQLite, allowing instant UI restoration.
- **Long-Term Memory (LTM)**: Passive extraction of high-value metadata (e.g., target domains) for future agent personalization.

### Security
- **Input Validation**: Hard-capped token limits.
- **Injection Scanning**: RegEx heuristic scanning blocks `system` overrides.
- **Secure Logging**: Intercepts and masks leaked API tokens.

### Observability & Evaluation
- **Tracer**: Subscribes to the Event Dispatcher to track exact agent latencies.
- **Pipeline Evaluator**: Scores output based on strict Pydantic schema validation.

---

## Folder Structure

```
thinkflow-studio/
├── app/
│   ├── agents/          # Specialist agent definitions
│   ├── core/            # Dependency injection and BaseAgent
│   ├── evaluation/      # CI benchmark scoring harness
│   ├── mcp/             # FastMCP server
│   ├── memory/          # SQLite stores and LTM
│   ├── orchestrator/    # DAG Pipeline
│   ├── schemas/         # Pydantic I/O models
│   ├── security/        # Input scanners
│   ├── telemetry/       # Secure Logging & Metrics
│   └── ui/              # Streamlit presentation layer
├── assets/              # Demo assets
├── docs/                # Architecture diagrams
├── tests/               # Pytest suite
└── Dockerfile           # Multi-stage container
```

---

## Installation & Usage

### Docker Setup (Recommended)
Ensure you have Docker and Docker Compose installed.

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/thinkflow-studio.git
   cd thinkflow-studio
   ```

2. Configure Environment:
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

3. Build and Run:
   ```bash
   make run
   # Or manually: docker-compose up --build
   ```

4. Access the UI at `http://localhost:8501`.

### Running Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   streamlit run app/ui/app.py
   ```

---

## Demo & Screenshots

![Demo Run](assets/screenshots/demo.gif)

*The ThinkFlow Execution Roadmap Tab*
![UI Screenshot](assets/screenshots/ui_main.png)

---

## Future Work
- **Vector Search LTM**: Replacing the SQLite exact-match Long-Term Memory with an embedded PgVector store.
- **Human-in-the-Loop (HITL)**: Pausing the pipeline at the Critic phase to ask the user to resolve assumptions before Planning.
- **Dynamic MCP Scaling**: Connecting to remote enterprise MCP servers for live business data retrieval.

## Contributing
Please see `CONTRIBUTING.md` for our code style and PR process. Ensure you run `make audit` before submitting!

## License
MIT License. See `LICENSE` for details.

## Acknowledgements
Built for the **Google AI Agents Kaggle Competition**. Powered by the Google Gen AI SDK.
