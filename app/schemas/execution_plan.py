"""
Schemas for Planner Agent structured output.
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field

class ExecutionPhase(BaseModel):
    """
    Represents a single sequential or parallel execution phase in the roadmap.
    """
    phase_name: str = Field(description="Name of the execution phase.")
    description: str = Field(description="Summary of what this phase accomplishes.")

class ExecutionPlanOutput(BaseModel):
    """
    Structured output returned by the Planner Agent.
    Synthesizes upstream analysis into an actionable roadmap and fills out the MCP framework template.
    """
    project_title: str = Field(description="Title of the project.")
    project_summary: str = Field(description="Brief summary of the project goals.")
    recommended_strategy: str = Field(description="Overall recommended strategy for execution.")
    execution_phases: List[ExecutionPhase] = Field(description="The chronological sequence of execution phases.")
    milestones: List[str] = Field(description="Key deliverables or milestones for the project.")
    tasks: List[str] = Field(description="High level tasks.")
    priority_order: List[str] = Field(description="The order in which phases/tasks should be prioritized.")
    estimated_duration: str = Field(description="High-level estimated timeline (e.g., '3 months').")
    estimated_difficulty: str = Field(description="Difficulty estimation.")
    required_resources: List[str] = Field(description="Resources or personnel required.")
    potential_risks: List[str] = Field(description="Key risks mitigating the weaknesses identified by the Critic.")
    success_metrics: List[str] = Field(description="Measurable KPIs to determine project success.")
    next_best_action: str = Field(description="The immediate next actionable step for the user.")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Confidence in the plan based on the inputs.")
    filled_framework: Dict[str, Any] = Field(
        default_factory=dict, 
        description="The MCP framework template fully populated with the project details."
    )
