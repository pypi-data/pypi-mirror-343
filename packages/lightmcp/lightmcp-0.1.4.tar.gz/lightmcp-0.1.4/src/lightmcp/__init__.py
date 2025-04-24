"""
LightMCP: A lightweight MCP tool layer for LLM agent frameworks.
"""
from typing import Dict, Any
from lightmcp.tool_loader import load_tool, MCPTool, ToolRegistry

__version__ = "0.1.4"

def add(tool_id: str) -> MCPTool:
    """
    Add and load an MCP tool by its ID.
    
    Args:
        tool_id: The ID of the tool to load (e.g., "notion.query_tasks")
        
    Returns:
        An MCPTool instance that can be used to run the tool
        
    Example:
        from lightmcp import add
        tool = add("notion.query_tasks")
        server_info = tool.run()
    """
    return load_tool(tool_id)

__all__ = ["add", "load_tool", "MCPTool", "ToolRegistry"]