"""
Integration test verifying planner agent auto-registration.
"""

def test_planner_registration():
    """
    Verify that importing the planner module automatically 
    registers the agent in the central AgentRegistry.
    """
    from app.agents.agent_registry import agent_registry
    import app.agents.__init__  # Triggers auto-imports
    
    registered_agents = agent_registry.list_agents()
    assert "planner" in registered_agents
    
    agent_class = agent_registry.get_agent("planner")
    assert agent_class.__name__ == "PlannerAgent"
