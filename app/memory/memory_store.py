"""
Long-term memory abstraction.
"""
import json
from typing import List, Dict, Any
from app.memory.sqlite_store import SQLiteStore

class MemoryStore:
    def __init__(self, db: SQLiteStore):
        self.db = db

    def save_insight(self, entity_type: str, content: str, metadata: Dict[str, Any] = None):
        """Persists isolated knowledge facts."""
        meta_json = json.dumps(metadata) if metadata else "{}"
        self.db.execute_query('''
            INSERT INTO long_term_memory (entity_type, content, metadata_json)
            VALUES (?, ?, ?)
        ''', (entity_type, content, meta_json))

    def search_insights(self, entity_type: str = None) -> List[Dict[str, Any]]:
        """Basic keyword search across insights."""
        query = "SELECT * FROM long_term_memory"
        params = []
        if entity_type:
            query += " WHERE entity_type = ?"
            params.append(entity_type)
        query += " ORDER BY created_at DESC"
        
        results = self.db.fetch_all(query, tuple(params))
        for row in results:
            if row.get('metadata_json'):
                row['metadata'] = json.loads(row['metadata_json'])
        return results
