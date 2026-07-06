"""
Tool registry for the ThinkFlow MCP Server.
"""

from mcp.server.fastmcp import FastMCP
from typing import Dict, Any

from app.mcp.tools.swot import SWOTInput, generate_swot_template
from app.mcp.tools.five_whys import FiveWhysInput, generate_five_whys_template
from app.mcp.tools.first_principles import FirstPrinciplesInput, generate_first_principles_template
from app.mcp.tools.decision_matrix import DecisionMatrixInput, generate_decision_matrix_template
from app.mcp.tools.pros_cons import ProsConsInput, generate_pros_cons_template
from app.mcp.tools.smart_goals import SMARTGoalsInput, generate_smart_goals_template
from app.mcp.tools.eisenhower import EisenhowerInput, generate_eisenhower_template

def register_tools(mcp: FastMCP) -> None:
    """
    Registers all thinking framework tools to the FastMCP server instance.
    
    Args:
        mcp (FastMCP): The FastMCP server instance.
    """
    
    @mcp.tool()
    def swot_analysis(input_data: SWOTInput) -> Dict[str, Any]:
        """Provides a structured template for a SWOT Analysis."""
        return generate_swot_template(input_data)

    @mcp.tool()
    def five_whys(input_data: FiveWhysInput) -> Dict[str, Any]:
        """Provides a structured template for a 5 Whys Root Cause Analysis."""
        return generate_five_whys_template(input_data)

    @mcp.tool()
    def first_principles(input_data: FirstPrinciplesInput) -> Dict[str, Any]:
        """Provides a structured template for First Principles Thinking."""
        return generate_first_principles_template(input_data)

    @mcp.tool()
    def decision_matrix(input_data: DecisionMatrixInput) -> Dict[str, Any]:
        """Provides a structured template for a Weighted Decision Matrix."""
        return generate_decision_matrix_template(input_data)

    @mcp.tool()
    def pros_cons(input_data: ProsConsInput) -> Dict[str, Any]:
        """Provides a structured template for a Pros & Cons Analysis."""
        return generate_pros_cons_template(input_data)

    @mcp.tool()
    def smart_goals(input_data: SMARTGoalsInput) -> Dict[str, Any]:
        """Provides a structured template for creating SMART Goals."""
        return generate_smart_goals_template(input_data)

    @mcp.tool()
    def eisenhower_matrix(input_data: EisenhowerInput) -> Dict[str, Any]:
        """Provides a structured template for an Eisenhower Task Matrix."""
        return generate_eisenhower_template(input_data)
