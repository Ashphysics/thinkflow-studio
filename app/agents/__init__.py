"""
Agents package initialization.
Ensures that all agents are imported so they register themselves with the AgentRegistry.
"""

from app.agents.agent_registry import agent_registry
from app.agents.coordinator import CoordinatorAgent

# Import specialized agents to trigger their auto-registration
try:
    from app.agents.idea_analyzer import IdeaAnalyzerAgent
    from app.agents.critic import CriticAgent
    from app.agents.framework_selector import FrameworkSelectorAgent
    from app.agents.planner import PlannerAgent
except ImportError:
    pass

__all__ = ["agent_registry", "CoordinatorAgent"]
