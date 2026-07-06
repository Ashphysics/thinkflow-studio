"""
Sidebar component for Streamlit UI.
"""
import streamlit as st
from app.orchestrator.context import WorkflowContext
from app.memory.memory_service import memory_service

def render_sidebar(context: WorkflowContext = None):
    st.sidebar.title("ThinkFlow Studio")
    st.sidebar.markdown("---")
    
    # Session Loading
    st.sidebar.subheader("Session History")
    sessions = memory_service.list_sessions()
    
    if sessions:
        session_options = {
            s["session_id"]: f"{s['session_id'][:8]} - {s.get('user_prompt', 'No prompt')[:20]}..."
            for s in sessions
        }
        selected_session_id = st.sidebar.selectbox(
            "Load previous session:",
            options=[""] + list(session_options.keys()),
            format_func=lambda x: "Select a session..." if x == "" else session_options[x]
        )
        
        if selected_session_id and st.sidebar.button("Load Session"):
            loaded_context = memory_service.load_session(selected_session_id)
            if loaded_context:
                st.session_state.workflow_context = loaded_context
                st.sidebar.success("Session loaded!")
                st.rerun()
            else:
                st.sidebar.error("Failed to load session.")
    else:
        st.sidebar.info("No previous sessions found.")

    st.sidebar.markdown("---")
    
    # Active Session Details
    if context:
        st.sidebar.subheader("Active Session")
        st.sidebar.text(f"Session ID:\n{context.session_id}")
        
        status_color = "🟢" if context.status == "completed" else "🔴" if context.status == "failed" else "🟡"
        st.sidebar.markdown(f"**Status:** {status_color} {context.status.capitalize()}")
        
        if context.end_time and context.start_time:
            duration = context.end_time - context.start_time
            st.sidebar.markdown(f"**Execution Time:** {duration:.2f}s")
            
        if context.framework_selection:
            st.sidebar.markdown(f"**Selected Framework:**\n`{context.framework_selection.selected_framework}`")
            
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Execution Logs")
        for log in context.execution_logs:
            icon = "✅" if log.get("status") == "success" else "❌"
            st.sidebar.text(f"{icon} {log.get('agent')}")
            
        st.sidebar.markdown("---")
        dev_mode = st.sidebar.checkbox("🛠️ Developer Mode")
        if dev_mode:
            from app.telemetry.dashboard import get_dashboard_metrics
            metrics = get_dashboard_metrics()
            with st.sidebar.expander("Telemetry Metrics", expanded=True):
                st.json(metrics)
                
    else:
        st.sidebar.info("No active session. Enter an idea and run analysis to start.")
