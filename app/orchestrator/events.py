"""
Event system for tracing and observing the workflow execution.
"""

from typing import Callable, Dict, Any, List
from pydantic import BaseModel

class WorkflowEvent(BaseModel):
    """Represents a state change or lifecycle event in the orchestrator."""
    event_type: str
    session_id: str
    agent_name: str
    details: Dict[str, Any]

class EventDispatcher:
    """
    Pub/Sub mechanism to decouple pipeline execution from logging, metrics, or UI updates.
    """
    def __init__(self):
        self._subscribers: List[Callable[[WorkflowEvent], None]] = []

    def subscribe(self, callback: Callable[[WorkflowEvent], None]) -> None:
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def dispatch(self, event: WorkflowEvent) -> None:
        for callback in self._subscribers:
            try:
                callback(event)
            except Exception:
                pass  # Do not let observer exceptions crash the pipeline

# Singleton dispatcher
dispatcher = EventDispatcher()
