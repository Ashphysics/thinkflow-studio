"""
Progress tracker component for Streamlit UI.
"""
import streamlit as st
from app.orchestrator.events import dispatcher, WorkflowEvent

class UIProgressTracker:
    def __init__(self):
        self.status_container = st.empty()
        self.current_status = None
        dispatcher.subscribe(self.handle_event)
        
    def handle_event(self, event: WorkflowEvent):
        if event.event_type == "pipeline_started":
            self.current_status = self.status_container.status("Initializing ThinkFlow Pipeline...", expanded=True)
            self.current_status.write("Starting orchestration...")
            
        elif event.event_type == "agent_started":
            if self.current_status:
                self.current_status.write(f"⏳ Running {event.agent_name}...")
                
        elif event.event_type == "agent_completed":
            if self.current_status:
                self.current_status.write(f"✅ {event.agent_name} completed successfully.")
                
        elif event.event_type == "agent_failed":
            if self.current_status:
                self.current_status.update(label="Pipeline Failed", state="error", expanded=True)
                self.current_status.write(f"❌ {event.agent_name} failed: {event.details.get('error')}")
                
        elif event.event_type == "pipeline_completed":
            if self.current_status:
                self.current_status.update(label="Analysis Complete", state="complete", expanded=False)
