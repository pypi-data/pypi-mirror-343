"""
Scoras: Intelligent Agent Framework with Complexity Scoring

This module provides tool functionality for the Scoras framework.
"""

from typing import Any, Dict, List, Optional, Union, Callable, TypeVar, Generic
import asyncio
import inspect
from pydantic import BaseModel, Field, create_model
import json
import httpx
import functools

from .core import ScoringMixin, Tool

class ToolParameter(BaseModel):
    """Model representing a parameter for a tool."""
    
    name: str = Field(..., description="Name of the parameter")
    type: str = Field(..., description="Type of the parameter")
    description: str = Field(..., description="Description of the parameter")
    required: bool = Field(True, description="Whether the parameter is required")
    default: Optional[Any] = Field(None, description="Default value for the parameter")

class ToolDefinition(BaseModel):
    """Model representing a tool definition."""
    
    name: str = Field(..., description="Name of the tool")
    description: str = Field(..., description="Description of what the tool does")
    parameters: List[ToolParameter] = Field(default_factory=list, description="Parameters for the tool")
    complexity: str = Field("standard", description="Complexity level of the tool")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the tool definition to a dictionary format."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": [param.model_dump() for param in self.parameters],
            "complexity": self.complexity
        }
    
    def to_json_schema(self) -> Dict[str, Any]:
        """Convert the tool definition to a JSON Schema format."""
        properties = {}
        required = []
        
        for param in self.parameters:
            param_schema = {"type": param.type, "description": param.description}
            
            if param.default is not None:
                param_schema["default"] = param.default
            
            properties[param.name] = param_schema
            
            if param.required:
                required.append(param.name)
        
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }

class ToolResult(BaseModel):
    """Model representing the result of a tool execution."""
    
    tool_name: str = Field(..., description="Name of the tool that was executed")
    success: bool = Field(..., description="Whether the tool execution was successful")
    result: Any = Field(None, description="Result of the tool execution")
    error: Optional[str] = Field(None, description="Error message if the tool execution failed")

class ToolChain(ScoringMixin):
    """
    A chain of tools that can be executed in sequence.
    
    Tool chains allow for composing multiple tools together to perform complex tasks.
    """
    
    def __init__(
        self,
        name: str,
        tools: List[Tool],
        enable_scoring: bool = True
    ):
        """
        Initialize a ToolChain.
        
        Args:
            name: Name of the tool chain
            tools: List of tools in the chain
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(enable_scoring=enable_scoring)
        self.name = name
        self.tools = tools
        
        # Add complexity score for the tool chain
        self._add_node_score(f"toolchain_{name}", inputs=1, outputs=1)
        
        # Add edges between tools in the chain
        for i in range(len(tools) - 1):
            self._add_edge_score(
                f"{tools[i].name}_to_{tools[i+1].name}",
                path_distance=1.0,
                information_content=0.6
            )
        
        # Incorporate tool complexity scores
        for tool in tools:
            if tool._enable_scoring:
                tool_score = tool.get_complexity_score()
                self._complexity_score.total_score += tool_score["total_score"]
                self._complexity_score.components[f"tool_{tool.name}"] = tool_score["total_score"]
        
        # Update the complexity rating
        self._complexity_score.update()
    
    async def execute(self, initial_input: Dict[str, Any]) -> List[Any]:
        """
        Execute the tool chain with the provided initial input.
        
        Args:
            initial_input: Initial input for the first tool
            
        Returns:
            List of results from each tool in the chain
        """
        results = []
        current_input = initial_input
        
        for tool in self.tools:
            # Execute the tool with the current input
            result = await tool.execute(**current_input)
            results.append(result)
            
            # Prepare input for the next tool
            if isinstance(result, dict):
                # If the result is a dictionary, use it as the input for the next tool
                current_input = result
            else:
                # Otherwise, wrap the result in a dictionary
                current_input = {"result": result}
        
        return results
    
    def execute_sync(self, initial_input: Dict[str, Any]) -> List[Any]:
        """
        Execute the tool chain synchronously with the provided initial input.
        
        Args:
            initial_input: Initial input for the first tool
            
        Returns:
            List of results from each tool in the chain
        """
        # Create an event loop if there isn't one
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Run the async method in the event loop
        return loop.run_until_complete(self.execute(initial_input))

class ToolRouter(ScoringMixin):
    """
    A router that selects the appropriate tool based on input.
    
    Tool routers enable dynamic tool selection based on the input context.
    """
    
    def __init__(
        self,
        name: str,
        tools: Dict[str, Tool],
        selector: Callable[[Dict[str, Any]], str],
        enable_scoring: bool = True
    ):
        """
        Initialize a ToolRouter.
        
        Args:
            name: Name of the tool router
            tools: Dictionary mapping tool names to tools
            selector: Function that selects a tool name based on input
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(enable_scoring=enable_scoring)
        self.name = name
        self.tools = tools
        self.selector = selector
        
        # Add complexity score for the tool router
        self._add_node_score(f"toolrouter_{name}", inputs=1, outputs=len(tools))
        self._add_condition_score(f"toolrouter_selection_{name}", branches=len(tools))
        
        # Incorporate tool complexity scores
        for tool_name, tool in tools.items():
            if tool._enable_scoring:
                tool_score = tool.get_complexity_score()
                self._complexity_score.total_score += tool_score["total_score"] * 0.5  # Discount to avoid double-counting
                self._complexity_score.components[f"tool_{tool_name}"] = tool_score["total_score"] * 0.5
        
        # Update the complexity rating
        self._complexity_score.update()
    
    async def execute(self, **kwargs) -> Any:
        """
        Execute the appropriate tool based on the input.
        
        Args:
            **kwargs: Parameters for the tool
            
        Returns:
            Result of the selected tool execution
        """
        # Select the appropriate tool
        tool_name = self.selector(kwargs)
        
        if tool_name not in self.tools:
            raise ValueError(f"Selected tool not found: {tool_name}")
        
        # Execute the selected tool
        tool = self.tools[tool_name]
        return await tool.execute(**kwargs)
    
    def execute_sync(self, **kwargs) -> Any:
        """
        Execute the appropriate tool synchronously based on the input.
        
        Args:
            **kwargs: Parameters for the tool
            
        Returns:
            Result of the selected tool execution
        """
        # Create an event loop if there isn't one
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Run the async method in the event loop
        return loop.run_until_complete(self.execute(**kwargs))

class ToolBuilder:
    """
    A builder for creating tools.
    
    Tool builders provide a convenient way to create tools with specific configurations.
    """
    
    def __init__(self, complexity: str = "standard", enable_scoring: bool = True):
        """
        Initialize a ToolBuilder.
        
        Args:
            complexity: Default complexity level for tools
            enable_scoring: Whether to enable complexity scoring for tools
        """
        self.complexity = complexity
        self.enable_scoring = enable_scoring
    
    def create_tool(
        self,
        name: str,
        description: str,
        function: Callable,
        parameters: Optional[List[Dict[str, Any]]] = None
    ) -> Tool:
        """
        Create a tool.
        
        Args:
            name: Name of the tool
            description: Description of what the tool does
            function: Function to call when the tool is used
            parameters: Optional list of parameter specifications
            
        Returns:
            Created tool
        """
        return Tool(
            name=name,
            description=description,
            function=function,
            parameters=parameters,
            complexity=self.complexity,
            enable_scoring=self.enable_scoring
        )
    
    def create_http_tool(
        self,
        name: str,
        description: str,
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        parameters: Optional[List[Dict[str, Any]]] = None
    ) -> Tool:
        """
        Create an HTTP tool.
        
        Args:
            name: Name of the tool
            description: Description of what the tool does
            url: URL to make requests to
            method: HTTP method to use
            headers: Optional headers to include in the request
            parameters: Optional list of parameter specifications
            
        Returns:
            Created HTTP tool
        """
        from .tools import HTTPTool
        
        return HTTPTool(
            name=name,
            description=description,
            url=url,
            method=method,
            headers=headers,
            params=parameters,
            complexity=self.complexity,
            enable_scoring=self.enable_scoring
        )

# Add the missing tool decorator
def tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    complexity: str = "standard",
    enable_scoring: bool = True
):
    """
    Decorator for creating tools from functions.
    
    Args:
        name: Optional name for the tool (defaults to function name)
        description: Optional description for the tool (defaults to function docstring)
        complexity: Complexity level of the tool ("simple", "standard", "complex")
        enable_scoring: Whether to track complexity scoring
        
    Returns:
        Decorated function that can be used as a tool
    """
    def decorator(func):
        # Get the tool name
        tool_name = name or func.__name__
        
        # Get the tool description
        tool_description = description or func.__doc__ or f"Tool for {tool_name}"
        
        # Create the tool
        tool_instance = Tool(
            name=tool_name,
            description=tool_description,
            function=func,
            complexity=complexity,
            enable_scoring=enable_scoring
        )
        
        # Add tool attributes to the function
        func.tool = tool_instance
        func.tool_name = tool_name
        func.tool_description = tool_description
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        # Add tool attributes to the wrapper
        wrapper.tool = tool_instance
        wrapper.tool_name = tool_name
        wrapper.tool_description = tool_description
        
        return wrapper
    
    return decorator
