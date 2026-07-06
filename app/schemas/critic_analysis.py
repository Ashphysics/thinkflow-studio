"""
Schemas for Critic Agent structured output.
"""

from typing import List
from pydantic import BaseModel, Field

class CriticOutput(BaseModel):
    """
    Structured output returned by the Critic Agent.
    Evaluates an IdeaAnalysisOutput without rejecting it.
    """
    strengths: List[str] = Field(description="Identified strengths of the idea.")
    weaknesses: List[str] = Field(description="Identified weaknesses or flaws in the idea.")
    risks: List[str] = Field(description="Potential risks associated with the idea.")
    assumptions: List[str] = Field(description="Hidden assumptions identified that need validation.")
    missing_information: List[str] = Field(description="Information missing from the analysis.")
    validation_questions: List[str] = Field(description="Questions that must be answered to validate the idea.")
    opportunities: List[str] = Field(description="Potential opportunities or pivots.")
    overall_readiness_score: float = Field(ge=0.0, le=1.0, description="Score from 0.0 to 1.0 indicating readiness for planning.")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Confidence in the critique based on provided context.")
