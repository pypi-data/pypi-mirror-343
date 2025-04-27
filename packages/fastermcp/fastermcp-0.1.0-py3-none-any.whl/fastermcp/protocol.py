"""Core protocol module for FasterMCP."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union, Callable, get_type_hints
from functools import wraps
import inspect
from pydantic import BaseModel, create_model

@dataclass
class Tool:
    """Represents a tool that can be used by the LLM."""
    name: str
    description: str
    parameters: Dict[str, Any]
    required_params: List[str] = field(default_factory=list)

@dataclass
class Resource:
    """Represents a resource that can be accessed by the LLM."""
    id: str
    type: str
    content: Any
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Context:
    """Represents the context for LLM interactions."""
    prompt: str
    tools: List[Tool] = field(default_factory=list)
    resources: List[Resource] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

class MCPProtocol:
    """Core protocol class for handling MCP communications."""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.resources: Dict[str, Resource] = {}
        
    def register_tool(self, tool: Tool) -> None:
        """Register a new tool."""
        self.tools[tool.name] = tool
        
    def tool(self, name: Optional[str] = None, description: Optional[str] = None) -> Callable:
        """Decorator to convert a Python function into an MCP tool.
        
        Args:
            name: Optional name for the tool. If not provided, uses the function name.
            description: Optional description of the tool. If not provided, uses the function's docstring.
        """
        def decorator(func: Callable) -> Callable:
            # Get function metadata
            func_name = name or func.__name__
            func_doc = description or inspect.getdoc(func) or ""
            type_hints = get_type_hints(func)
            
            # Create parameters schema
            parameters = {}
            required_params = []
            sig = inspect.signature(func)
            
            for param_name, param in sig.parameters.items():
                if param.annotation == inspect._empty:
                    param_type = Any
                else:
                    param_type = type_hints[param_name]
                
                param_schema = {"type": "any"}
                if param_type in (str, int, float, bool):
                    param_schema["type"] = param_type.__name__
                
                parameters[param_name] = param_schema
                
                if param.default == inspect._empty:
                    required_params.append(param_name)
            
            # Create and register tool
            tool = Tool(
                name=func_name,
                description=func_doc,
                parameters=parameters,
                required_params=required_params
            )
            self.register_tool(tool)
            
            @wraps(func)
            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs) if inspect.iscoroutinefunction(func) else func(*args, **kwargs)
            
            return wrapper
        return decorator
        
    def register_resource(self, resource: Resource) -> None:
        """Register a new resource."""
        self.resources[resource.id] = resource
        
    def create_context(self, prompt: str, tool_names: Optional[List[str]] = None,
                      resource_ids: Optional[List[str]] = None) -> Context:
        """Create a new context with specified tools and resources."""
        tools = [self.tools[name] for name in (tool_names or []) if name in self.tools]
        resources = [self.resources[rid] for rid in (resource_ids or []) if rid in self.resources]
        return Context(prompt=prompt, tools=tools, resources=resources)