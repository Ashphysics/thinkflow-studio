# GitHub Release & Configuration

## Repository Description
ThinkFlow Studio: A deterministic, multi-agent structured thinking environment powered by Google Gen AI and MCP.

## Repository Topics
`ai-agents` `google-genai` `mcp` `model-context-protocol` `streamlit` `pydantic` `multi-agent` `dag` `sqlite`

---

## Release Notes: Version 1.0.0

🎉 **Initial Release for the Google AI Agents Kaggle Competition!**

We are thrilled to release ThinkFlow Studio v1.0.0. This release transforms unstructured ideation into rigorous, deterministic execution plans.

### Highlights
- 🧠 **Deterministic DAG Pipeline**: A strict execution flow (Coordinator -> Analyzer -> Critic -> Selector -> Planner) using strict Pydantic schemas to prevent context dilution.
- 🔌 **FastMCP Integration**: Cognitive frameworks (SWOT, 5 Whys) are decoupled from prompts and served via local stdio, guaranteeing zero schema hallucination.
- 🐳 **Docker-Ready**: Instantly deploy the Streamlit frontend, SQLite memory persistence, and MCP subprocess in a single container.
- 🛡️ **Zero-Trust Security**: Built-in local prompt injection scanning and API key redaction in logs.
- 📊 **Developer Telemetry**: Event-driven latency tracking and success metrics viewable directly in the UI.

### Getting Started
Simply clone the repo, copy `.env.example` to `.env`, add your `GOOGLE_API_KEY`, and run `make run`!
