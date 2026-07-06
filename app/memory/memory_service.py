"""
Facade mapping workflow events to persistence operations.
"""
from typing import List, Dict, Any, Optional
from loguru import logger
from app.memory.sqlite_store import SQLiteStore
from app.memory.session_store import SessionStore
from app.memory.memory_store import MemoryStore
from app.orchestrator.context import WorkflowContext

class MemoryService:
    def __init__(self, db_path: str = "thinkflow_memory.db"):
        self.db = SQLiteStore(db_path)
        self.sessions = SessionStore(self.db)
        self.ltm = MemoryStore(self.db)

    def save_session(self, context: WorkflowContext):
        """Saves session and attempts to index long-term insights."""
        try:
            self.sessions.save_session(context)
            
            # Simple heuristic: if Idea Analysis is done, index the domain
            if context.idea_analysis and context.status == "completed":
                domain = context.idea_analysis.domain
                # We don't want a million duplicates, so in a real app we'd use vector search or dedupe.
                # For this implementation, just store it.
                self.ltm.save_insight(
                    entity_type="domain",
                    content=domain,
                    metadata={"session_id": context.session_id}
                )
        except Exception as e:
            logger.error(f"MemoryService failed to save session: {e}")

    def load_session(self, session_id: str) -> Optional[WorkflowContext]:
        try:
            return self.sessions.load_session(session_id)
        except Exception as e:
            logger.error(f"MemoryService failed to load session: {e}")
            return None

    def list_sessions(self) -> List[Dict[str, Any]]:
        try:
            return self.sessions.list_sessions()
        except Exception as e:
            logger.error(f"MemoryService failed to list sessions: {e}")
            return []

    def delete_session(self, session_id: str):
        self.sessions.delete_session(session_id)

    def summarize_previous_conversations(self) -> List[str]:
        """Returns high-level ideas mapped previously."""
        sessions = self.list_sessions()
        summaries = []
        for s in sessions:
            prompt = s.get("user_prompt", "")
            if len(prompt) > 50:
                prompt = prompt[:47] + "..."
            summaries.append(f"{s['session_id'][:8]}: {prompt} ({s['status']})")
        return summaries

# Singleton instance
memory_service = MemoryService()
