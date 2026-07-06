import streamlit as st
import os
import sys

# Ensure the root directory is in sys.path so 'app' can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

st.set_page_config(page_title="ThinkFlow Architecture", page_icon="🏗️", layout="wide")

st.title("🏗️ ThinkFlow Studio Architecture")
st.markdown("This page explains the internal multi-agent orchestrations and deployments.")

# Helper to read markdown files
def load_doc(filename):
    path = os.path.join("docs", "architecture", filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return f"Documentation for {filename} not found."

tab1, tab2, tab3, tab4 = st.tabs([
    "System Overview", 
    "Pipeline & Agents", 
    "Memory & Persistence", 
    "MCP Integration"
])

with tab1:
    st.markdown(load_doc("overall_architecture.md"))
    st.markdown("### Deployment Architecture")
    st.markdown(load_doc("deployment.md"))

with tab2:
    st.markdown(load_doc("pipeline.md"))
    st.markdown("""
    ### The Agents
    - **Coordinator**: Entry point, initializes the deterministic pipeline.
    - **Idea Analyzer**: Parses raw intent into structured demographics and assumptions.
    - **Critic**: Challenges the idea, identifying weaknesses and required validations.
    - **Framework Selector**: Interfaces with FastMCP to fetch the correct structural tool.
    - **Planner**: Acts as a compiler, turning the intelligence and framework into an execution roadmap.
    """)

with tab3:
    st.markdown(load_doc("memory.md"))

with tab4:
    st.markdown(load_doc("mcp_communication.md"))
    st.info("The FastMCP Server runs as a separate subprocess using stdio transport. It guarantees that agents always receive perfectly structured cognitive templates without hallucinating the JSON fields.")
