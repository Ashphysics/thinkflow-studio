"""
Integration test verifying critic agent auto-registration.
"""

def test_critic_registration():
    """
    Verify that importing the critic module automatically 
    registers the agent in the central AgentRegistry.
    """
    # Import the registry to check state
    from app.agents.agent_registry import agent_registry
    
    # Import the module which should trigger registration
    import app.agents.critic
    
    registered_agents = agent_registry.list_agents()
    
    assert "critic" in registered_agents
    
    # Verify we can retrieve it
    agent_class = agent_registry.get_agent("critic")
    assert agent_class.__name__ == "CriticAgent"
