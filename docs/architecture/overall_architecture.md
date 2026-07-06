# Overall Architecture

ThinkFlow Studio is built on a decoupled, multi-agent architecture designed for highly deterministic output generation. It eschews generic LLM routing in favor of a strict Directed Acyclic Graph (DAG) and local Model Context Protocol (MCP) tool fetching.

```mermaid
graph TD
    UI[Streamlit UI] --> Pipeline[Agent Pipeline]
    
    subgraph Orchestration
        Pipeline --> IdeaAnalyzer
        IdeaAnalyzer --> Critic
        Critic --> FrameworkSelector
        FrameworkSelector --> Planner
    end

    subgraph External
        FrameworkSelector -- "Fetches Template" --> MCP[FastMCP Server]
        Pipeline -- "Calls" --> LLM[Google Gemini API]
    end

    subgraph Persistence
        Pipeline -- "Saves State" --> SQLite[(SQLite Store)]
        SQLite -- "Loads Session" --> UI
    end
```
