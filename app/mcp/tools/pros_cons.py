"""
Pros & Cons Analysis thinking framework tool.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field

class ProConItem(BaseModel):
    point: str
    weight: int = Field(ge=1, le=5, description="Weight or importance from 1 (low) to 5 (high)")

class ProsConsInput(BaseModel):
    """Input schema for Pros & Cons Analysis."""
    decision_topic: str = Field(description="The decision or topic to evaluate.")

class ProsConsOutput(BaseModel):
    """Structured output template for Pros & Cons Analysis."""
    decision_topic: str
    pros: List[ProConItem]
    cons: List[ProConItem]
    total_pro_weight: int
    total_con_weight: int
    conclusion: str

def generate_pros_cons_template(input_data: ProsConsInput) -> Dict[str, Any]:
    """
    Generates a structured JSON template for a Pros & Cons Analysis.
    
    Args:
        input_data (ProsConsInput): The validated input data.
        
    Returns:
        Dict[str, Any]: A dictionary representing the ProsConsOutput schema.
    """
    output = ProsConsOutput(
        decision_topic=input_data.decision_topic,
        pros=[ProConItem(point="[Pro point 1]", weight=3), ProConItem(point="[Pro point 2]", weight=3)],
        cons=[ProConItem(point="[Con point 1]", weight=3), ProConItem(point="[Con point 2]", weight=3)],
        total_pro_weight=0,
        total_con_weight=0,
        conclusion="[Summary of which side outweighs the other based on weights]"
    )
    return output.model_dump()
