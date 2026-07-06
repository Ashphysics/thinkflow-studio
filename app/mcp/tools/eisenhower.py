"""
Eisenhower Matrix thinking framework tool.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field

class EisenhowerInput(BaseModel):
    """Input schema for Eisenhower Matrix Analysis."""
    tasks: List[str] = Field(description="List of tasks to categorize.")

class EisenhowerOutput(BaseModel):
    """Structured output template for Eisenhower Matrix Analysis."""
    urgent_important: List[str] = Field(description="Do first")
    not_urgent_important: List[str] = Field(description="Schedule")
    urgent_not_important: List[str] = Field(description="Delegate")
    not_urgent_not_important: List[str] = Field(description="Eliminate")

def generate_eisenhower_template(input_data: EisenhowerInput) -> Dict[str, Any]:
    """
    Generates a structured JSON template for an Eisenhower Matrix.
    
    Args:
        input_data (EisenhowerInput): The validated input data.
        
    Returns:
        Dict[str, Any]: A dictionary representing the EisenhowerOutput schema.
    """
    output = EisenhowerOutput(
        urgent_important=["[Task 1 from list]", "[Task 2 from list]"],
        not_urgent_important=["[Task 3 from list]"],
        urgent_not_important=["[Task 4 from list]"],
        not_urgent_not_important=["[Task 5 from list]"]
    )
    return output.model_dump()
