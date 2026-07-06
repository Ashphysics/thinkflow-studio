"""
Unit tests for MCP framework tools.
"""

import pytest
from app.mcp.tools.swot import SWOTInput, generate_swot_template
from app.mcp.tools.smart_goals import SMARTGoalsInput, generate_smart_goals_template
from pydantic import ValidationError

def test_swot_tool_valid_input():
    input_data = SWOTInput(topic="New Product Launch", context="Q4 Launch")
    result = generate_swot_template(input_data)
    
    assert result["topic"] == "New Product Launch"
    assert len(result["strengths"]) == 2
    assert result["strengths"][0] == "[Strength 1]"

def test_swot_tool_invalid_input():
    with pytest.raises(ValidationError):
        SWOTInput() # Missing required 'topic'

def test_smart_goals_tool():
    input_data = SMARTGoalsInput(raw_goal="Get more users")
    result = generate_smart_goals_template(input_data)
    
    assert result["raw_goal"] == "Get more users"
    assert "[What exactly needs to be done?]" in result["specific"]
