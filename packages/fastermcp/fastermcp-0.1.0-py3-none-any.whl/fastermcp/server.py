"""Server module for FasterMCP."""

from typing import Dict, List, Optional, Any, Callable, Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .protocol import MCPProtocol, Tool, Resource, Context

class ToolRequest(BaseModel):
    name: str
    parameters: Dict[str, Any]

class ContextRequest(BaseModel):
    prompt: str
    tool_names: Optional[List[str]] = None
    resource_ids: Optional[List[str]] = None

class MCPServer:
    """Server class for handling MCP requests."""
    
    def __init__(self):
        self.app = FastAPI()
        self.protocol = MCPProtocol()
        self._setup_routes()
        
    def _setup_routes(self) -> None:
        """Setup FastAPI routes."""
        @self.app.post("/tools")
        async def register_tool(tool: Tool):
            self.protocol.register_tool(tool)
            return {"status": "success", "message": f"Tool {tool.name} registered"}
            
        @self.app.post("/resources")
        async def register_resource(resource: Resource):
            self.protocol.register_resource(resource)
            return {"status": "success", "message": f"Resource {resource.id} registered"}
            
        @self.app.post("/context")
        async def create_context(request: ContextRequest):
            context = self.protocol.create_context(
                prompt=request.prompt,
                tool_names=request.tool_names,
                resource_ids=request.resource_ids
            )
            return context
            
        @self.app.post("/execute")
        async def execute_tool(request: ToolRequest):
            tool = self.protocol.tools.get(request.name)
            if not tool:
                raise HTTPException(status_code=404, detail=f"Tool {request.name} not found")
            
            # Validate required parameters
            missing_params = [param for param in tool.required_params if param not in request.parameters]
            if missing_params:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required parameters: {', '.join(missing_params)}"
                )
            
            # Execute the tool function if it exists
            if hasattr(tool, 'func'):
                try:
                    result = await tool.func(**request.parameters)
                    return {"status": "success", "result": result}
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            else:
                return {"status": "success", "message": f"Tool {request.name} executed"}
    
    def run(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        """Run the MCP server."""
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)