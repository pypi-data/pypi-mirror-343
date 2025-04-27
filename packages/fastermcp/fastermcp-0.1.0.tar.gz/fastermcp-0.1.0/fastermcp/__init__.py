"""FasterMCP - A simple and intuitive library for building MCP servers and clients."""

from fastermcp.server import MCPServer
from fastermcp.client import MCPClient
from fastermcp.protocol import MCPProtocol, Tool, Resource, Context

__version__ = "0.1.0"
__all__ = [
    "MCPServer",
    "MCPClient",
    "MCPProtocol",
    "Tool",
    "Resource",
    "Context"
]