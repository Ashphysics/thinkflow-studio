"""
SQLite Database manager for memory persistence.
"""
import sqlite3
import os
import json
from loguru import logger

class SQLiteStore:
    def __init__(self, db_path: str = "thinkflow_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Creates tables if they don't exist."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Session Table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sessions (
                        session_id TEXT PRIMARY KEY,
                        user_prompt TEXT,
                        status TEXT,
                        start_time REAL,
                        end_time REAL
                    )
                ''')
                
                # Context Table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS workflow_contexts (
                        session_id TEXT PRIMARY KEY,
                        context_json TEXT,
                        FOREIGN KEY (session_id) REFERENCES sessions (session_id) ON DELETE CASCADE
                    )
                ''')
                
                # Long Term Memory Table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS long_term_memory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        entity_type TEXT,
                        content TEXT,
                        metadata_json TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
                logger.info(f"Initialized SQLite database at {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to initialize SQLite database: {e}")

    def execute_query(self, query: str, params: tuple = ()):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
        except Exception as e:
            logger.error(f"SQLite execute error: {e}")
            raise

    def fetch_all(self, query: str, params: tuple = ()):
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"SQLite fetch error: {e}")
            raise
            
    def fetch_one(self, query: str, params: tuple = ()):
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, params)
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"SQLite fetch one error: {e}")
            raise
