import logging
import os
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

logger = logging.getLogger(__name__)


async def serve() -> None:
    """Start MCP server"""
    required_vars = ["JOBHAI_BASE_URL", "AUTH_TOKEN"]
    if not all(var in os.environ for var in required_vars):
        raise ValueError(f"Missing required environment variables: {required_vars}")

    server = Server("jobhai-mcp-server")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        try:
            return None
        except Exception as e:
            logger.error("Failed to list tools: %s", e)
            raise

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        try:
            if not name.startswith("get_"):
                raise ValueError("Only GET operations allowed")
            tool = None
            async with tool.client:
                result = await tool.run(body=arguments)
            return [TextContent(type="text", text=str(result))]
        except Exception as e:
            logger.error("Tool execution failed: %s", e)
            raise

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)