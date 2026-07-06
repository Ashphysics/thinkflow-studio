"""
SMART Goals thinking framework tool.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field

class SMARTGoalsInput(BaseModel):
    """Input schema for SMART Goals Analysis."""
    raw_goal: str = Field(description="The initial, unstructured goal.")

class SMARTGoalsOutput(BaseModel):
    """Structured output template for SMART Goals Analysis."""
    raw_goal: str
    specific: str
    measurable: str
    achievable: str
    relevant: str
    time_bound: str
    refined_goal: str

def generate_smart_goals_template(input_data: SMARTGoalsInput) -> Dict[str, Any]:
    """
    Generates a structured JSON template for SMART Goals.
    
    Args:
        input_data (SMARTGoalsInput): The validated input data.
        
    Returns:
        Dict[str, Any]: A dictionary representing the SMARTGoalsOutput schema.
    """
    output = SMARTGoalsOutput(
        raw_goal=input_data.raw_goal,
        specific="[What exactly needs to be done?]",
        measurable="[How will you track progress?]",
        achievable="[Is this realistic with current resources?]",
        relevant="[Why does this matter right now?]",
        time_bound="[When is the deadline?]",
        refined_goal="[The new SMART goal statement combining the above]"
    )
    return output.model_dump()
