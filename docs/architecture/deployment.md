# Deployment Architecture

**Version:** 1.0.0  
**Last Updated:** 2026-07-06  

The application is containerized using Docker, bundling the Streamlit UI and the FastMCP subprocess into a single easily deployable artifact.

```mermaid
graph LR
    User[User Browser] -->|Port 8501| Docker[Docker Container]
    
    subgraph Docker Container
        UI[Streamlit App]
        MCP[MCP Subprocess]
        DB[(SQLite File Volume)]
        
        UI -- "Spawns via stdio client" --> MCP
        UI -- "Reads/Writes via SQLAlchemy" --> DB
    end
    
    UI -- "HTTPS API Calls via google-genai" --> Gemini[Google Gemini GenAI]
```
