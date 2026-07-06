"""
Decision Matrix thinking framework tool.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field

class Criteria(BaseModel):
    name: str
    weight: float = Field(ge=0.0, le=1.0, description="Weight of the criteria from 0.0 to 1.0")

class OptionScore(BaseModel):
    criteria_name: str
    score: int = Field(ge=1, le=5, description="Score from 1 to 5")

class DecisionOption(BaseModel):
    option_name: str
    scores: List[OptionScore]
    total_weighted_score: float

class DecisionMatrixInput(BaseModel):
    """Input schema for Decision Matrix."""
    decision_topic: str = Field(description="The main decision to be made.")
    options: List[str] = Field(description="List of options to evaluate.")
    criteria: List[str] = Field(description="List of criteria to evaluate against.")

class DecisionMatrixOutput(BaseModel):
    """Structured output template for Decision Matrix."""
    decision_topic: str
    criteria_weights: List[Criteria]
    evaluations: List[DecisionOption]
    recommended_option: str

def generate_decision_matrix_template(input_data: DecisionMatrixInput) -> Dict[str, Any]:
    """
    Generates a structured JSON template for a Decision Matrix.
    
    Args:
        input_data (DecisionMatrixInput): The validated input data.
        
    Returns:
        Dict[str, Any]: A dictionary representing the DecisionMatrixOutput schema.
    """
    criteria_weights = [Criteria(name=c, weight=1.0 / len(input_data.criteria) if input_data.criteria else 1.0) for c in input_data.criteria]
    
    evaluations = []
    for opt in input_data.options:
        scores = [OptionScore(criteria_name=c, score=3) for c in input_data.criteria]
        evaluations.append(DecisionOption(option_name=opt, scores=scores, total_weighted_score=0.0))
        
    output = DecisionMatrixOutput(
        decision_topic=input_data.decision_topic,
        criteria_weights=criteria_weights,
        evaluations=evaluations,
        recommended_option="[Option Name]"
    )
    return output.model_dump()
