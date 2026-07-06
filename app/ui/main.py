"""
Main Streamlit Entrypoint for ThinkFlow Studio.

Initializes settings, starts logging, builds sidebar navigation and serves the
home dashboard layout.

TODOs:
    - [ ] Dynamic loading of multi-page layouts via streamlit routing.
    - [ ] Integrate real-time websockets or SSE streaming for agent output status panels.
"""

import streamlit as st

from app.config import configure_logging, settings

# Initialize Logging configuration
configure_logging(log_level=settings.log_level)


def main() -> None:
    """
    Main application UI execution thread.
    """
    st.set_page_config(
        page_title="ThinkFlow Studio",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🧠 ThinkFlow Studio")
    st.caption(
        "An AI Thinking Partner that transforms raw ideas into structured action plans "
        "using multiple specialized AI agents."
    )

    st.sidebar.title("Navigation")
    st.sidebar.info("Select a workspace page to begin configuration.")
    st.sidebar.markdown("---")
    st.sidebar.write(f"Environment: `{settings.app_env}`")

    # Placeholder status indicator
    st.info(
        "Welcome to ThinkFlow Studio! The system foundation is successfully "
        "configured and ready for Google Gen AI SDK and Multi-Agent system "
        "logic integrations in the next phase."
    )

    # Core Idea Input Placeholder
    st.subheader("Submit Your Project Concept")
    st.text_area(
        label="Enter project descriptions, constraints, or competitor details...",
        placeholder="e.g. Building an automated Kaggle classifier pipeline...",
        disabled=True
    )

    st.button("Synthesize Plan (Disabled - Foundation Stage)", disabled=True)


if __name__ == "__main__":
    main()
