"""
Main Streamlit Application Entry Point.
"""
import asyncio
import streamlit as st

st.set_page_config(page_title="ThinkFlow Studio", page_icon="🧠", layout="wide")

from app.orchestrator.pipeline import AgentPipeline
from app.ui.components.sidebar import render_sidebar
from app.ui.components.progress import UIProgressTracker
from app.ui.components.results import render_results
from app.telemetry.dashboard import get_dashboard_metrics
import os

# Check for required API Key
if not os.environ.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY") == "your_google_api_key_here":
    st.error("🚨 Configuration Error: `GOOGLE_API_KEY` is missing. Please set it in your environment or `.env` file.")
    st.stop()

def main():
    st.title("🧠 ThinkFlow Studio")
    st.markdown("Transform raw ideas into structured execution plans using multi-agent orchestration.")
    
    # Initialize session state for the context if not exists
    if "workflow_context" not in st.session_state:
        st.session_state.workflow_context = None

    # Render Sidebar
    render_sidebar(st.session_state.workflow_context)

    # Input Area
    prompt = st.text_area(
        "Describe your idea:", 
        placeholder="e.g., I want to build an AI startup for teachers...",
        height=150
    )

    if st.button("Run Analysis", type="primary"):
        if not prompt.strip():
            st.warning("Please enter an idea to analyze.")
            return

        # Instantiate pipeline and UI tracker
        pipeline = AgentPipeline()
        tracker = UIProgressTracker()

        try:
            # Run the asynchronous pipeline synchronously within Streamlit
            result = asyncio.run(pipeline.run(prompt))
            st.session_state.workflow_context = result
            
            if result.status == "failed":
                st.error(f"Pipeline Execution Failed: {result.error_message}")
                
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

    # Render Results if available
    if st.session_state.workflow_context:
        render_results(st.session_state.workflow_context)

# Configure Multipage Navigation
pg = st.navigation([
    st.Page(main, title="ThinkFlow Studio", icon="🧠"),
    st.Page("app/ui/pages/architecture.py", title="Architecture", icon="🏗️")
])

if __name__ == "__main__":
    pg.run()
