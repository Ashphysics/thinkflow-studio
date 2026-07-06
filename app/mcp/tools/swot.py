"""
SWOT Analysis thinking framework tool.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field

class SWOTInput(BaseModel):
    """Input schema for SWOT Analysis."""
    topic: str = Field(description="The topic, project, or decision to analyze.")
    context: str = Field(default="", description="Additional context or background information.")

class SWOTOutput(BaseModel):
    """Structured output template for SWOT Analysis."""
    topic: str
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]

def generate_swot_template(input_data: SWOTInput) -> Dict[str, Any]:
    """
    Generates a structured JSON template for a SWOT Analysis.
    
    Args:
        input_data (SWOTInput): The validated input data.
        
    Returns:
        Dict[str, Any]: A dictionary representing the SWOTOutput schema, filled with empty placeholders.
    """
    output = SWOTOutput(
        topic=input_data.topic,
        strengths=["[Strength 1]", "[Strength 2]"],
        weaknesses=["[Weakness 1]", "[Weakness 2]"],
        opportunities=["[Opportunity 1]", "[Opportunity 2]"],
        threats=["[Threat 1]", "[Threat 2]"]
    )
    return output.model_dump()
