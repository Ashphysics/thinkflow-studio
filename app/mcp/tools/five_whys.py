"""
5 Whys root cause analysis thinking framework tool.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field

class FiveWhysInput(BaseModel):
    """Input schema for 5 Whys Analysis."""
    problem_statement: str = Field(description="The core problem to analyze.")

class WhyNode(BaseModel):
    """A single 'Why' step."""
    question: str
    answer: str

class FiveWhysOutput(BaseModel):
    """Structured output template for 5 Whys Analysis."""
    problem_statement: str
    whys: List[WhyNode]
    root_cause: str
    action_item: str

def generate_five_whys_template(input_data: FiveWhysInput) -> Dict[str, Any]:
    """
    Generates a structured JSON template for a 5 Whys Analysis.
    
    Args:
        input_data (FiveWhysInput): The validated input data.
        
    Returns:
        Dict[str, Any]: A dictionary representing the FiveWhysOutput schema, filled with empty placeholders.
    """
    output = FiveWhysOutput(
        problem_statement=input_data.problem_statement,
        whys=[
            WhyNode(question="Why did the problem occur?", answer="[Answer 1]"),
            WhyNode(question="Why did [Answer 1] happen?", answer="[Answer 2]"),
            WhyNode(question="Why did [Answer 2] happen?", answer="[Answer 3]"),
            WhyNode(question="Why did [Answer 3] happen?", answer="[Answer 4]"),
            WhyNode(question="Why did [Answer 4] happen?", answer="[Answer 5]")
        ],
        root_cause="[Identified Root Cause]",
        action_item="[Action to address root cause]"
    )
    return output.model_dump()
