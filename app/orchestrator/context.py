"""
Workflow Context definitions.
Maintains the strongly typed state payload passed between pipeline agents.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

from app.schemas.idea_analysis import IdeaAnalysisOutput
from app.schemas.critic_analysis import CriticOutput
from app.schemas.framework_selection import FrameworkSelectionOutput
from app.schemas.execution_plan import ExecutionPlanOutput

class WorkflowContext(BaseModel):
    """
    Maintains the execution state and inputs/outputs across the pipeline.
    """
    session_id: str = Field(description="Unique session identifier.")
    request_id: str = Field(description="Unique request identifier.")
    user_prompt: str = Field(description="The original user input.")
    status: str = Field(default="pending", description="Pipeline status: pending, running, completed, failed.")
    
    # Evolving Context Payloads
    idea_analysis: Optional[IdeaAnalysisOutput] = None
    critic_analysis: Optional[CriticOutput] = None
    framework_selection: Optional[FrameworkSelectionOutput] = None
    execution_plan: Optional[ExecutionPlanOutput] = None
    
    # Execution Metadata
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    error_message: Optional[str] = None
    execution_logs: list[Dict[str, Any]] = Field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert state to a dictionary for Agent context injection."""
        return {
            "session_id": self.session_id,
            "request_id": self.request_id,
            "user_prompt": self.user_prompt,
            "idea_analysis": self.idea_analysis.model_dump() if self.idea_analysis else None,
            "critic_analysis": self.critic_analysis.model_dump() if self.critic_analysis else None,
            "framework_selection": self.framework_selection.model_dump() if self.framework_selection else None,
            "execution_plan": self.execution_plan.model_dump() if self.execution_plan else None
        }
