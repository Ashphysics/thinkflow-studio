"""
Integration tests for SQLite memory store.
"""
import pytest
import os
import json
from app.memory.sqlite_store import SQLiteStore
from app.memory.session_store import SessionStore
from app.memory.memory_store import MemoryStore
from app.memory.memory_service import MemoryService
from app.orchestrator.context import WorkflowContext

TEST_DB_PATH = "test_memory.db"

@pytest.fixture
def clean_db():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    service = MemoryService(TEST_DB_PATH)
    yield service
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_session_lifecycle(clean_db):
    service = clean_db
    
    context = WorkflowContext(
        session_id="test_session_1",
        request_id="req1",
        user_prompt="Build a game",
        status="running"
    )
    
    # Save
    service.save_session(context)
    
    # List
    sessions = service.list_sessions()
    assert len(sessions) == 1
    assert sessions[0]["session_id"] == "test_session_1"
    
    # Load
    loaded = service.load_session("test_session_1")
    assert loaded is not None
    assert loaded.session_id == "test_session_1"
    assert loaded.user_prompt == "Build a game"
    
    # Delete
    service.delete_session("test_session_1")
    assert len(service.list_sessions()) == 0

def test_long_term_memory_indexing(clean_db):
    service = clean_db
    
    from app.schemas.idea_analysis import IdeaAnalysisOutput
    
    context = WorkflowContext(
        session_id="test_session_2",
        request_id="req2",
        user_prompt="Build a SaaS",
        status="completed",
        idea_analysis=IdeaAnalysisOutput(
            idea_title="SaaS", one_sentence_summary="App", category="Tech",
            domain="B2B Software", primary_goal="Sales", target_users=[],
            assumptions=[], constraints=[], missing_information=[],
            required_clarifications=[], confidence_score=0.9
        )
    )
    
    service.save_session(context)
    
    # Check LTM extracted the domain since status is 'completed'
    insights = service.ltm.search_insights(entity_type="domain")
    assert len(insights) == 1
    assert insights[0]["content"] == "B2B Software"
    assert insights[0]["metadata"]["session_id"] == "test_session_2"
