"""
Integration test verifying framework selector agent auto-registration.
"""

def test_framework_selector_registration():
    """
    Verify that importing the framework_selector module automatically 
    registers the agent in the central AgentRegistry.
    """
    from app.agents.agent_registry import agent_registry
    import app.agents.__init__  # Triggers auto-imports
    
    registered_agents = agent_registry.list_agents()
    assert "framework_selector" in registered_agents
    
    agent_class = agent_registry.get_agent("framework_selector")
    assert agent_class.__name__ == "FrameworkSelectorAgent"
