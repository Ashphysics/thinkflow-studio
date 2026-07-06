"""
Unit tests for core infrastructure modules (DI container, Factory, Session).
"""

import pytest
from app.core.dependency_container import DependencyContainer, DependencyError
from app.core.session_manager import SessionManager

class MockService:
    def __init__(self):
        self.value = "test"

def test_dependency_container_singleton():
    """Verify dependency container acts as a singleton and resolves correctly."""
    container = DependencyContainer()
    container.clear()
    
    instance1 = MockService()
    container.register_singleton(MockService, instance1)
    
    resolved_instance = container.resolve(MockService)
    
    assert resolved_instance is instance1
    assert resolved_instance.value == "test"

def test_dependency_container_factory():
    """Verify dependency container resolves factories."""
    container = DependencyContainer()
    container.clear()
    
    container.register_factory(MockService, lambda: MockService())
    
    instance1 = container.resolve(MockService)
    instance2 = container.resolve(MockService)
    
    assert instance1 is not instance2
    assert isinstance(instance1, MockService)

def test_dependency_container_missing():
    """Verify exception on missing dependency."""
    container = DependencyContainer()
    container.clear()
    
    with pytest.raises(DependencyError):
        container.resolve(MockService)

def test_session_manager():
    """Verify session tracking."""
    manager = SessionManager()
    session = manager.create_session({"user": "admin"})
    
    assert session.session_id is not None
    assert session.context["user"] == "admin"
    
    manager.update_session_context(session.session_id, {"role": "tester"})
    updated = manager.get_session(session.session_id)
    assert updated.context["role"] == "tester"
    
    manager.end_session(session.session_id)
    with pytest.raises(KeyError):
        manager.get_session(session.session_id)
