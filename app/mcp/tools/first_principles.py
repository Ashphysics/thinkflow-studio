"""
First Principles Thinking framework tool.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field

class FirstPrinciplesInput(BaseModel):
    """Input schema for First Principles Thinking."""
    complex_problem: str = Field(description="The complex problem or current assumption to deconstruct.")

class FirstPrinciplesOutput(BaseModel):
    """Structured output template for First Principles Thinking."""
    complex_problem: str
    current_assumptions: List[str]
    fundamental_truths: List[str]
    new_solutions: List[str]

def generate_first_principles_template(input_data: FirstPrinciplesInput) -> Dict[str, Any]:
    """
    Generates a structured JSON template for First Principles Thinking.
    
    Args:
        input_data (FirstPrinciplesInput): The validated input data.
        
    Returns:
        Dict[str, Any]: A dictionary representing the FirstPrinciplesOutput schema.
    """
    output = FirstPrinciplesOutput(
        complex_problem=input_data.complex_problem,
        current_assumptions=["[Assumption 1]", "[Assumption 2]"],
        fundamental_truths=["[Truth 1 - empirically proven]", "[Truth 2 - basic laws]"],
        new_solutions=["[Solution built from truths 1]", "[Solution built from truths 2]"]
    )
    return output.model_dump()
