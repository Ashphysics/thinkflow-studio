"""
Integration tests for the MCP Server initialization and routing.
"""

import pytest
from app.mcp.server import create_mcp_server

def test_mcp_server_initialization():
    """Verify that the MCP server initializes and registers tools correctly."""
    mcp = create_mcp_server()
    
    assert mcp.name == "ThinkFlow Studio MCP Server"
    
    # FastMCP stores tools in _tool_manager.
    # The tools should include our 7 framework tools + health_check
    tools = mcp.list_tools()
    
    tool_names = [tool.name for tool in tools]
    
    assert "health_check" in tool_names
    assert "swot_analysis" in tool_names
    assert "five_whys" in tool_names
    assert "first_principles" in tool_names
    assert "decision_matrix" in tool_names
    assert "pros_cons" in tool_names
    assert "smart_goals" in tool_names
    assert "eisenhower_matrix" in tool_names

