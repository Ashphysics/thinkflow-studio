"""
Main entry point for the ThinkFlow MCP Server.
"""

from mcp.server.fastmcp import FastMCP
from app.mcp.registry import register_tools
from loguru import logger
import sys

def create_mcp_server() -> FastMCP:
    """
    Initializes and configures the FastMCP server.
    
    Returns:
        FastMCP: The configured server instance.
    """
    mcp = FastMCP("ThinkFlow Studio MCP Server")
    
    # Register all framework tools
    register_tools(mcp)
    
    # Simple health check endpoint (as a tool or prompt)
    @mcp.tool()
    def health_check() -> str:
        """Returns the health status of the MCP server."""
        return "ThinkFlow MCP Server is running."

    logger.info("ThinkFlow MCP Server initialized with 7 core framework tools + health_check.")
    return mcp

def run_stdio() -> None:
    """
    Runs the MCP server using STDIO transport.
    Suitable for local agent-to-mcp communication.
    """
    mcp = create_mcp_server()
    logger.info("Starting MCP Server on STDIO transport...")
    try:
        mcp.run()
    except KeyboardInterrupt:
        logger.info("MCP Server stopped by user.")
    except Exception as e:
        logger.exception("MCP Server encountered an error.")
        sys.exit(1)

if __name__ == "__main__":
    run_stdio()
