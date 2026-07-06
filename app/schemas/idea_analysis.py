"""
Schemas for Idea Analyzer Agent structured output.
"""

from typing import List, Optional
from pydantic import BaseModel, Field

class IdeaAnalysisOutput(BaseModel):
    """
    Structured output returned by the Idea Analyzer Agent.
    Strictly focuses on parsing and understanding, not planning.
    """
    idea_title: str = Field(description="A concise, catchy title for the idea.")
    one_sentence_summary: str = Field(description="A clear, single-sentence summary of the core concept.")
    category: str = Field(description="The primary category (e.g., 'SaaS', 'Mobile App', 'Physical Product').")
    domain: str = Field(description="The industry or domain (e.g., 'Education', 'Healthcare').")
    primary_goal: str = Field(description="What the user ultimately wants to achieve.")
    target_users: List[str] = Field(description="List of intended user demographics or personas.")
    assumptions: List[str] = Field(default_factory=list, description="Unstated assumptions the user is making.")
    constraints: List[str] = Field(default_factory=list, description="Explicit or implicit constraints.")
    missing_information: List[str] = Field(default_factory=list, description="Critical information not provided in the prompt.")
    required_clarifications: List[str] = Field(default_factory=list, description="Questions that should be asked to the user later.")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Confidence in understanding the idea based on provided text (0.0 to 1.0).")
