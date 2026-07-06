# Pipeline Architecture

**Version:** 1.0.0  
**Last Updated:** 2026-07-06  

The pipeline replaces loosely coupled agent queries with a strict, state-managed execution sequence. It ensures that the context from each agent is deterministically passed to the next agent in the sequence.

```mermaid
sequenceDiagram
    participant UI as Streamlit UI
    participant Pipe as AgentPipeline
    participant A as Idea Analyzer
    participant Cr as Critic
    participant FS as Framework Selector
    participant MCP as FastMCP Server
    participant P as Planner

    UI->>Pipe: Initiates Orchestration (Prompt)
    
    Pipe->>A: User Prompt
    A-->>Pipe: `IdeaAnalysisOutput`
    
    Pipe->>Cr: `IdeaAnalysisOutput`
    Cr-->>Pipe: `CriticOutput`
    
    Pipe->>FS: Analyzer & Critic Outputs
    FS->>MCP: Fetch Framework Template
    MCP-->>FS: JSON Template
    FS-->>Pipe: `FrameworkSelectionOutput`
    
    Pipe->>P: All previous Outputs
    P-->>Pipe: `ExecutionPlanOutput`
    
    Pipe-->>UI: WorkflowContext (Saved to Memory)
```
