# Folder Structure

**Version:** 1.0.0  
**Last Updated:** 2026-07-06  

```text
thinkflow-studio/
├── app/
│   ├── agents/          # Specialist agents (Planner, Critic, etc.)
│   ├── config/          # Settings and providers
│   ├── core/            # BaseAgent, BaseTool, Dependency Injection
│   ├── evaluation/      # CI benchmark scoring harness
│   ├── mcp/             # FastMCP server and tool logic
│   ├── memory/          # SQLite stores and LTM extraction
│   ├── orchestrator/    # Deterministic DAG Pipeline and Events
│   ├── schemas/         # Pydantic I/O models
│   ├── security/        # Input scanners
│   ├── telemetry/       # Tracers, Secure Logging, Metrics
│   └── ui/              # Streamlit presentation layer
├── assets/              # Demo videos and screenshots
├── docs/                # Architecture diagrams
├── tests/               # Unit and Integration test suites
├── Dockerfile           # Multi-stage container build
├── docker-compose.yml   # Local deployment manifest
├── Makefile             # CLI automation
└── pyproject.toml       # Modern Python packaging
```
