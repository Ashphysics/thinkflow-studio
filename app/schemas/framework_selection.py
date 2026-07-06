"""
Schemas for Framework Selector Agent.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field

class LLMFrameworkSelection(BaseModel):
    """
    Schema provided to the LLM to select the framework.
    Excludes the framework_template dictionary to avoid additionalProperties API errors.
    """
    selected_framework: str = Field(description="The exact name of the MCP tool selected (e.g., 'swot_analysis').")
    selection_reason: str = Field(description="Detailed reasoning for why this framework was chosen.")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Confidence in the selection based on context provided.")

class FrameworkSelectionOutput(BaseModel):
    """
    Structured output returned by the Framework Selector Agent.
    Contains the chosen MCP framework and the retrieved template.
    """
    selected_framework: str = Field(description="The exact name of the MCP tool selected (e.g., 'swot_analysis').")
    selection_reason: str = Field(description="Detailed reasoning for why this framework was chosen.")
    framework_template: Dict[str, Any] = Field(default_factory=dict, description="The empty JSON template retrieved from the MCP Server.")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Confidence in the selection based on context provided.")
