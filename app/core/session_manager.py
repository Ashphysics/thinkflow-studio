"""
Session Manager for tracking multi-turn agent interactions and state.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import uuid
from loguru import logger

class SessionState(BaseModel):
    """
    Represents the state of an active session.
    """
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    context: Dict[str, Any] = Field(default_factory=dict)
    history: list[Dict[str, Any]] = Field(default_factory=list)
    active_agent: Optional[str] = None


class SessionManager:
    """
    Manages in-memory distributed session states.
    Can be extended to persist states to a database using `app/memory`.
    """
    def __init__(self) -> None:
        self._sessions: Dict[str, SessionState] = {}

    def create_session(self, initial_context: Optional[Dict[str, Any]] = None) -> SessionState:
        """
        Creates a new tracking session.
        """
        state = SessionState(context=initial_context or {})
        self._sessions[state.session_id] = state
        logger.info(f"Created new session: {state.session_id}")
        return state

    def get_session(self, session_id: str) -> SessionState:
        """
        Retrieves an active session.
        """
        if session_id not in self._sessions:
            logger.error(f"Session not found: {session_id}")
            raise KeyError(f"Session {session_id} does not exist.")
        return self._sessions[session_id]

    def update_session_context(self, session_id: str, updates: Dict[str, Any]) -> None:
        """
        Updates the context variables of an existing session.
        """
        session = self.get_session(session_id)
        session.context.update(updates)
        logger.debug(f"Updated context for session: {session_id}")

    def append_history(self, session_id: str, message: Dict[str, Any]) -> None:
        """
        Appends an interaction message to the session history.
        """
        session = self.get_session(session_id)
        session.history.append(message)
        
    def end_session(self, session_id: str) -> None:
        """
        Clears and terminates a session.
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            logger.info(f"Ended session: {session_id}")
