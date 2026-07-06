"""
Deterministic Workflow definitions.
"""

from typing import List

def get_ideation_workflow() -> List[str]:
    """
    Returns the strict sequence of agents for the ideation pipeline.
    Coordinator is the entry point, but it delegates to this pipeline.
    """
    return [
        "analyzer",          # IdeaAnalyzerAgent
        "critic",            # CriticAgent
        "framework_selector",# FrameworkSelectorAgent
        "planner"            # PlannerAgent
    ]
