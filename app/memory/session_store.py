"""
Session memory abstraction.
"""
import json
from typing import List, Dict, Any, Optional
from app.memory.sqlite_store import SQLiteStore
from app.orchestrator.context import WorkflowContext

class SessionStore:
    def __init__(self, db: SQLiteStore):
        self.db = db

    def save_session(self, context: WorkflowContext):
        """Upserts a session and its full context blob."""
        context_dict = context.model_dump(mode="json")
        context_json = json.dumps(context_dict)
        
        # Upsert session metadata
        self.db.execute_query('''
            INSERT INTO sessions (session_id, user_prompt, status, start_time, end_time)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(session_id) DO UPDATE SET
                status=excluded.status,
                end_time=excluded.end_time
        ''', (context.session_id, context.user_prompt, context.status, context.start_time, context.end_time))
        
        # Upsert context blob
        self.db.execute_query('''
            INSERT INTO workflow_contexts (session_id, context_json)
            VALUES (?, ?)
            ON CONFLICT(session_id) DO UPDATE SET
                context_json=excluded.context_json
        ''', (context.session_id, context_json))

    def load_session(self, session_id: str) -> Optional[WorkflowContext]:
        """Loads a full workflow context from the database."""
        row = self.db.fetch_one("SELECT context_json FROM workflow_contexts WHERE session_id = ?", (session_id,))
        if row and row['context_json']:
            data = json.loads(row['context_json'])
            return WorkflowContext(**data)
        return None

    def list_sessions(self) -> List[Dict[str, Any]]:
        """Returns lightweight metadata for all sessions."""
        return self.db.fetch_all("SELECT session_id, user_prompt, status, start_time FROM sessions ORDER BY start_time DESC")

    def delete_session(self, session_id: str):
        """Deletes a session and its cascaded context."""
        self.db.execute_query("DELETE FROM sessions WHERE session_id = ?", (session_id,))
