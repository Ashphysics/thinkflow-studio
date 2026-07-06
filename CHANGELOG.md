# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - Initial Release
### Added
- **Multi-Agent Orchestration Pipeline**: Integrated Coordinator, Idea Analyzer, Critic, Framework Selector, and Planner agents into a deterministic DAG.
- **FastMCP Server**: Local standard I/O based Model Context Protocol server exposing 7 structured cognitive frameworks (SWOT, 5 Whys, etc.).
- **Streamlit UI**: Decoupled presentation layer with real-time progress tracking, architecture visualization, and developer telemetry mode.
- **SQLite Memory Persistence**: Session state preservation and Long-Term Memory (LTM) extraction without external database dependencies.
- **Security & Observability**: Local prompt injection scanning, API key log redaction, and event-driven latency telemetry.
- **Docker Deployment**: Multi-stage Dockerfile and `docker-compose.yml` for instant zero-config deployments.
