# Troubleshooting Guide

**Version:** 1.0.0  
**Last Updated:** 2026-07-06  

This document provides solutions to common issues encountered when running or developing ThinkFlow Studio.

## 1. Missing GOOGLE_API_KEY
- **Error**: `AgentExecutionError: Model load failed: GEMINI_API_KEY is not set.`
- **Cause**: The application cannot find the Google Gemini API key.
- **Fix**: Create a `.env` file in the root directory by copying `.env.example`. Ensure the variable is named `GOOGLE_API_KEY` (not `GEMINI_API_KEY`) and that it contains a valid token.

## 2. Streamlit Startup Issues (Zombie Processes)
- **Error**: Streamlit fails to start, or the port `8501` is already in use.
- **Cause**: A previous Streamlit process crashed or was not killed properly.
- **Fix**: Terminate the zombie process.
  - *Windows*: `Stop-Process -Id (Get-NetTCPConnection -LocalPort 8501).OwningProcess -Force`
  - *Linux/Mac*: `kill -9 $(lsof -t -i:8501)`

## 3. Dependency Injection Errors (ModelFactory)
- **Error**: `No registration found for <class 'app.core.model_factory.ModelFactory'>`
- **Cause**: The singleton was not registered in the `DependencyContainer` before use.
- **Fix**: Ensure that `app/ui/app.py` properly initializes the container and registers the `ModelFactory` before calling the `AgentPipeline`.

## 4. Model Strict Schema Errors
- **Error**: `additionalProperties is only supported in Gemini Enterprise Agent Platform mode`
- **Cause**: The standard Gemini Developer API strictly forbids `additionalProperties: true` or `Dict[str, Any]` inside response schemas.
- **Fix**: Use the Dual-Schema architecture. Define the output field as a `str` (JSON string) in the LLM-facing schema, and manually parse it using `json.loads()` inside the agent's `_execute` method.

## 5. MCP Connection Issues
- **Error**: `Failed to fetch MCP template: unhandled errors in a TaskGroup`
- **Cause**: The `FastMCP` subprocess crashed or the stdio stream was corrupted.
- **Fix**: Ensure the payload sent to the tool matches the required format: `{"input_data": {"query": "..."}}`.

## 6. Docker Issues
- **Error**: Database is locked or not persisting.
- **Fix**: Ensure that SQLite is mounted to a volume in `docker-compose.yml`, and avoid running concurrent local Streamlit instances while the Docker container is running.
