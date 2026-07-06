"""
Integration test verifying agent auto-registration.
"""

def test_idea_analyzer_registration():
    """
    Verify that importing the idea_analyzer module automatically 
    registers the agent in the central AgentRegistry.
    """
    # Import the registry to check state
    from app.agents.agent_registry import agent_registry
    
    # Import the module which should trigger registration
    import app.agents.idea_analyzer
    
    registered_agents = agent_registry.list_agents()
    
    assert "analyzer" in registered_agents
    
    # Verify we can retrieve it
    agent_class = agent_registry.get_agent("analyzer")
    assert agent_class.__name__ == "IdeaAnalyzerAgent"
