"""Client module for FasterMCP."""

from typing import Dict, List, Optional, Any, Union
import aiohttp
from pydantic import BaseModel
from .protocol import Tool, Resource, Context

class MCPClient:
    """Client class for interacting with MCP server."""
    
    def __init__(self, server_url: str):
        self.server_url = server_url.rstrip('/')
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    async def register_tool(self, tool: Tool) -> Dict[str, Any]:
        """Register a new tool with the MCP server."""
        if not self.session:
            raise RuntimeError("Client session not initialized")
        async with self.session.post(f"{self.server_url}/tools", json=tool.__dict__) as response:
            return await response.json()
            
    async def register_resource(self, resource: Resource) -> Dict[str, Any]:
        """Register a new resource with the MCP server."""
        if not self.session:
            raise RuntimeError("Client session not initialized")
        async with self.session.post(f"{self.server_url}/resources", json=resource.__dict__) as response:
            return await response.json()
            
    async def create_context(self, prompt: str, tool_names: Optional[List[str]] = None,
                           resource_ids: Optional[List[str]] = None) -> Context:
        """Create a new context with specified tools and resources."""
        if not self.session:
            raise RuntimeError("Client session not initialized")
        request_data = {
            "prompt": prompt,
            "tool_names": tool_names,
            "resource_ids": resource_ids
        }
        async with self.session.post(f"{self.server_url}/context", json=request_data) as response:
            data = await response.json()
            return Context(**data)
            
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool on the MCP server."""
        if not self.session:
            raise RuntimeError("Client session not initialized")
        request_data = {
            "name": tool_name,
            "parameters": parameters
        }
        async with self.session.post(f"{self.server_url}/execute", json=request_data) as response:
            return await response.json()