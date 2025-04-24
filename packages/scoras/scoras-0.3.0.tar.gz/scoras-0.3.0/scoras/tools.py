"""
Tools module for the Scoras library.

This module contains implementations for creating and managing tools that can be used by agents,
with integrated scoring to measure workflow complexity.

Author: Anderson L. Amaral
"""

from typing import Any, Callable, Dict, List, Optional, Type, Union, TypeVar
import inspect
import json
import asyncio
import re
import requests
import subprocess
from pydantic import BaseModel, Field, create_model

from .core import Tool, ScoreTracker, ScorasConfig

class ToolRegistry:
    """Registry for tools that can be used by agents."""
    
    _tools: Dict[str, Tool] = {}
    
    @classmethod
    def register(cls, tool: Tool) -> Tool:
        """Register a tool in the registry."""
        cls._tools[tool.name] = tool
        return tool
    
    @classmethod
    def get(cls, name: str) -> Optional[Tool]:
        """Get a tool from the registry by name."""
        return cls._tools.get(name)
    
    @classmethod
    def list(cls) -> List[Tool]:
        """List all registered tools."""
        return list(cls._tools.values())
    
    @classmethod
    def clear(cls) -> None:
        """Clear the registry."""
        cls._tools.clear()

def register_tool(name: str = None, description: str = None, complexity: str = "standard"):
    """Decorator to register a tool in the registry."""
    def decorator(func):
        tool_name = name or func.__name__
        tool_description = description or func.__doc__ or f"Tool for {tool_name}"
        
        tool = Tool(
            name=tool_name,
            description=tool_description,
            function=func,
            complexity=complexity
        )
        
        return ToolRegistry.register(tool)
    
    return decorator

class ToolChain:
    """Chain of tools that can be executed in sequence."""
    
    def __init__(
        self, 
        tools: List[Tool],
        name: str = "tool_chain",
        description: str = "Chain of tools executed in sequence",
        enable_scoring: bool = True
    ):
        self.tools = tools
        self.name = name
        self.description = description
        self.enable_scoring = enable_scoring
        self.score_tracker = ScoreTracker() if enable_scoring else None
        
        # Add score for tool chain
        if self.score_tracker:
            self.score_tracker.add_node("complex")
            
            # Add tools and edges between them
            for tool in tools:
                self.score_tracker.add_tool(tool.complexity)
            
            # Add edges between tools (n-1 edges for n tools)
            for _ in range(len(tools) - 1):
                self.score_tracker.add_edge()
    
    async def execute(self, initial_input: Any) -> Any:
        """Execute the chain of tools."""
        current_input = initial_input
        
        for tool in self.tools:
            # Execute the tool with the current input
            if isinstance(current_input, dict):
                result = await tool.execute(**current_input)
            else:
                # Try to convert to string if not a dict
                result = await tool.execute(input=str(current_input))
            
            # The output of this tool becomes the input for the next
            current_input = result
        
        return current_input
    
    def execute_sync(self, initial_input: Any) -> Any:
        """Synchronous version of execute."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        return loop.run_until_complete(self.execute(initial_input))
    
    def to_tool(self) -> Tool:
        """Convert the tool chain to a single tool."""
        async def chain_function(**kwargs):
            return await self.execute(kwargs)
        
        return Tool(
            name=self.name,
            description=self.description,
            function=chain_function,
            complexity="complex"
        )
    
    def get_complexity_score(self) -> Optional[Dict[str, Any]]:
        """Get the complexity score of the tool chain."""
        if not self.score_tracker:
            return None
        
        return self.score_tracker.get_report()

class ToolRouter:
    """Router that selects the appropriate tool based on input."""
    
    def __init__(
        self,
        tools: Dict[str, Tool],
        router_function: Callable[[Dict[str, Any]], str],
        name: str = "tool_router",
        description: str = "Router that selects the appropriate tool based on input",
        enable_scoring: bool = True
    ):
        self.tools = tools
        self.router_function = router_function
        self.name = name
        self.description = description
        self.enable_scoring = enable_scoring
        self.score_tracker = ScoreTracker() if enable_scoring else None
        
        # Add score for tool router
        if self.score_tracker:
            self.score_tracker.add_node("complex")
            
            # Add tools
            for tool in tools.values():
                self.score_tracker.add_tool(tool.complexity)
            
            # Add conditional edges from router to each tool
            for _ in range(len(tools)):
                self.score_tracker.add_edge(True)
    
    async def execute(self, **kwargs) -> Any:
        """Execute the router to select and run the appropriate tool."""
        # Determine which tool to use
        tool_name = self.router_function(kwargs)
        
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found in router")
        
        # Execute the selected tool
        tool = self.tools[tool_name]
        return await tool.execute(**kwargs)
    
    def execute_sync(self, **kwargs) -> Any:
        """Synchronous version of execute."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        return loop.run_until_complete(self.execute(**kwargs))
    
    def to_tool(self) -> Tool:
        """Convert the tool router to a single tool."""
        async def router_function(**kwargs):
            return await self.execute(**kwargs)
        
        return Tool(
            name=self.name,
            description=self.description,
            function=router_function,
            complexity="complex"
        )
    
    def get_complexity_score(self) -> Optional[Dict[str, Any]]:
        """Get the complexity score of the tool router."""
        if not self.score_tracker:
            return None
        
        return self.score_tracker.get_report()

def create_http_tool(
    name: str,
    description: str,
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    params_mapping: Optional[Dict[str, str]] = None,
    result_model: Optional[Type[BaseModel]] = None,
    complexity: str = "standard",
    enable_scoring: bool = True
) -> Tool:
    """
    Create a tool that makes HTTP requests.
    
    Args:
        name: Name of the tool
        description: Description of the tool
        url: URL template with placeholders (e.g., "https://api.example.com/{param}")
        method: HTTP method (GET, POST, PUT, DELETE)
        headers: HTTP headers
        params_mapping: Mapping from function parameters to request parameters
        result_model: Pydantic model for the result
        complexity: Complexity of the tool (simple, standard, complex)
        enable_scoring: Whether to enable complexity scoring
        
    Returns:
        A configured HTTP tool
    """
    async def http_function(**kwargs):
        # Replace placeholders in URL
        formatted_url = url
        for param_name, param_value in kwargs.items():
            if f"{{{param_name}}}" in formatted_url:
                formatted_url = formatted_url.replace(f"{{{param_name}}}", str(param_value))
        
        # Prepare request parameters
        request_params = {}
        request_json = None
        
        if params_mapping:
            for param_name, request_key in params_mapping.items():
                if param_name in kwargs:
                    request_params[request_key] = kwargs[param_name]
        else:
            # Use all parameters that weren't used in URL
            for param_name, param_value in kwargs.items():
                if f"{{{param_name}}}" not in url:
                    request_params[param_name] = param_value
        
        # For POST/PUT, use json parameter instead of params
        if method.upper() in ["POST", "PUT"]:
            request_json = request_params
            request_params = {}
        
        # Make the request
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.request(
                method=method.upper(),
                url=formatted_url,
                headers=headers,
                params=request_params,
                json=request_json
            )
        )
        
        # Raise exception for error status codes
        response.raise_for_status()
        
        # Parse the response
        try:
            result = response.json()
        except ValueError:
            # Not JSON, return text
            result = response.text
        
        # Convert to result model if specified
        if result_model and isinstance(result, dict):
            return result_model.model_validate(result)
        
        return result
    
    # Extract parameters from URL
    url_params = re.findall(r'{([^}]+)}', url)
    
    # Create parameter info
    parameters = {}
    for param in url_params:
        parameters[param] = {
            "type": "string",
            "description": f"Parameter '{param}' for the URL"
        }
    
    # Add parameters from mapping
    if params_mapping:
        for param_name in params_mapping.keys():
            if param_name not in parameters:
                parameters[param_name] = {
                    "type": "string",
                    "description": f"Parameter '{param_name}' for the request"
                }
    
    # Create the tool
    tool = Tool(
        name=name,
        description=description,
        function=http_function,
        parameters=parameters,
        complexity=complexity
    )
    
    return tool

def create_python_tool(
    function: Callable,
    name: Optional[str] = None,
    description: Optional[str] = None,
    is_async: bool = False,
    complexity: str = "standard",
    enable_scoring: bool = True
) -> Tool:
    """
    Create a tool from a Python function.
    
    Args:
        function: Python function to wrap
        name: Name of the tool (defaults to function name)
        description: Description of the tool (defaults to function docstring)
        is_async: Whether the function is asynchronous
        complexity: Complexity of the tool (simple, standard, complex)
        enable_scoring: Whether to enable complexity scoring
        
    Returns:
        A configured Python tool
    """
    tool_name = name or function.__name__
    tool_description = description or function.__doc__ or f"Tool for {tool_name}"
    
    if is_async:
        # Function is already async
        async_function = function
    else:
        # Wrap in async function
        async def async_function(**kwargs):
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, lambda: function(**kwargs))
    
    return Tool(
        name=tool_name,
        description=tool_description,
        function=async_function,
        complexity=complexity
    )

def create_system_tool(
    name: str,
    description: str,
    command: str,
    working_dir: Optional[str] = None,
    parse_json: bool = False,
    result_model: Optional[Type[BaseModel]] = None,
    complexity: str = "complex",
    enable_scoring: bool = True
) -> Tool:
    """
    Create a tool that executes system commands.
    
    Args:
        name: Name of the tool
        description: Description of the tool
        command: Command template with placeholders (e.g., "ls {directory}")
        working_dir: Working directory for the command
        parse_json: Whether to parse the output as JSON
        result_model: Pydantic model for the result
        complexity: Complexity of the tool (simple, standard, complex)
        enable_scoring: Whether to enable complexity scoring
        
    Returns:
        A configured system tool
    """
    async def system_function(**kwargs):
        # Replace placeholders in command
        formatted_command = command
        for param_name, param_value in kwargs.items():
            if f"{{{param_name}}}" in formatted_command:
                formatted_command = formatted_command.replace(f"{{{param_name}}}", str(param_value))
        
        # Execute the command
        loop = asyncio.get_event_loop()
        process = await loop.run_in_executor(
            None,
            lambda: subprocess.run(
                formatted_command,
                shell=True,
                cwd=working_dir,
                capture_output=True,
                text=True
            )
        )
        
        # Check for errors
        if process.returncode != 0:
            raise RuntimeError(f"Command failed with error: {process.stderr}")
        
        # Parse the output
        output = process.stdout.strip()
        
        if parse_json:
            try:
                result = json.loads(output)
                
                # Convert to result model if specified
                if result_model and isinstance(result, dict):
                    return result_model.model_validate(result)
                
                return result
            except json.JSONDecodeError:
                raise ValueError(f"Failed to parse command output as JSON: {output}")
        
        return output
    
    # Extract parameters from command
    command_params = re.findall(r'{([^}]+)}', command)
    
    # Create parameter info
    parameters = {}
    for param in command_params:
        parameters[param] = {
            "type": "string",
            "description": f"Parameter '{param}' for the command"
        }
    
    # Create the tool
    tool = Tool(
        name=name,
        description=description,
        function=system_function,
        parameters=parameters,
        complexity=complexity
    )
    
    return tool

def create_composite_tool(
    name: str,
    description: str,
    tools: List[Tool],
    result_key: Optional[str] = None,
    complexity: str = "complex",
    enable_scoring: bool = True
) -> Tool:
    """
    Create a composite tool that combines multiple tools.
    
    Args:
        name: Name of the tool
        description: Description of the tool
        tools: List of tools to combine
        result_key: Key to extract from the final result (if it's a dict)
        complexity: Complexity of the tool (simple, standard, complex)
        enable_scoring: Whether to enable complexity scoring
        
    Returns:
        A configured composite tool
    """
    # Create a tool chain
    tool_chain = ToolChain(
        tools=tools,
        name=name,
        description=description,
        enable_scoring=enable_scoring
    )
    
    async def composite_function(**kwargs):
        result = await tool_chain.execute(kwargs)
        
        # Extract result key if specified
        if result_key and isinstance(result, dict) and result_key in result:
            return result[result_key]
        
        return result
    
    # Create parameter info by combining parameters from all tools
    parameters = {}
    for tool in tools:
        if tool.parameters:
            for param_name, param_info in tool.parameters.items():
                if param_name not in parameters:
                    parameters[param_name] = param_info
    
    # Create the tool
    tool = Tool(
        name=name,
        description=description,
        function=composite_function,
        parameters=parameters,
        complexity=complexity
    )
    
    return tool

class ToolBuilder:
    """Builder for creating complex tools with a fluent interface."""
    
    def __init__(self, name: str, description: str = None):
        self.name = name
        self.description = description or f"Tool for {name}"
        self.steps = []
        self.parameters = {}
        self.result_processor = None
        self.complexity = "standard"
        self.enable_scoring = True
    
    def add_step(self, tool: Tool, input_mapping: Optional[Dict[str, str]] = None) -> 'ToolBuilder':
        """Add a step to the tool."""
        self.steps.append((tool, input_mapping))
        
        # Add parameters from the tool
        if tool.parameters:
            for param_name, param_info in tool.parameters.items():
                # If there's an input mapping, use the mapped name
                if input_mapping and param_name in input_mapping:
                    mapped_name = input_mapping[param_name]
                    self.parameters[mapped_name] = param_info
                else:
                    self.parameters[param_name] = param_info
        
        return self
    
    def set_result_processor(self, processor: Callable[[Any], Any]) -> 'ToolBuilder':
        """Set a function to process the final result."""
        self.result_processor = processor
        return self
    
    def set_complexity(self, complexity: str) -> 'ToolBuilder':
        """Set the complexity of the tool."""
        self.complexity = complexity
        return self
    
    def set_enable_scoring(self, enable_scoring: bool) -> 'ToolBuilder':
        """Set whether to enable complexity scoring."""
        self.enable_scoring = enable_scoring
        return self
    
    def build(self) -> Tool:
        """Build the tool."""
        async def tool_function(**kwargs):
            current_result = kwargs
            
            for tool, input_mapping in self.steps:
                # Map inputs if needed
                if input_mapping:
                    mapped_inputs = {}
                    for param_name, mapped_name in input_mapping.items():
                        if mapped_name in current_result:
                            mapped_inputs[param_name] = current_result[mapped_name]
                    step_input = mapped_inputs
                else:
                    step_input = current_result
                
                # Execute the step
                if isinstance(step_input, dict):
                    step_result = await tool.execute(**step_input)
                else:
                    step_result = await tool.execute(input=str(step_input))
                
                # Update the current result
                if isinstance(step_result, dict):
                    if isinstance(current_result, dict):
                        current_result.update(step_result)
                    else:
                        current_result = step_result
                else:
                    current_result = step_result
            
            # Process the final result if needed
            if self.result_processor:
                return self.result_processor(current_result)
            
            return current_result
        
        # Create the tool
        tool = Tool(
            name=self.name,
            description=self.description,
            function=tool_function,
            parameters=self.parameters,
            complexity=self.complexity
        )
        
        return tool

# Common tools that can be used by agents
@register_tool(name="search", description="Search for information on the web", complexity="standard")
async def search(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Search for information on the web.
    
    Args:
        query: Search query
        num_results: Number of results to return
        
    Returns:
        List of search results with title and snippet
    """
    # This is a mock implementation
    await asyncio.sleep(1)  # Simulate network delay
    
    # Return mock results
    return [
        {
            "title": f"Result {i+1} for '{query}'",
            "snippet": f"This is a snippet for result {i+1} about {query}.",
            "url": f"https://example.com/result{i+1}"
        }
        for i in range(min(num_results, 10))
    ]

@register_tool(name="calculator", description="Perform mathematical calculations", complexity="simple")
async def calculator(expression: str) -> float:
    """
    Perform mathematical calculations.
    
    Args:
        expression: Mathematical expression to evaluate
        
    Returns:
        Result of the calculation
    """
    # Sanitize the expression to prevent code injection
    if not re.match(r'^[\d\s\+\-\*\/\(\)\.\,\%\^\&\|]*$', expression):
        raise ValueError("Invalid expression. Only basic mathematical operations are allowed.")
    
    # Replace ^ with ** for exponentiation
    expression = expression.replace('^', '**')
    
    # Evaluate the expression
    try:
        return eval(expression, {"__builtins__": {}})
    except Exception as e:
        raise ValueError(f"Error evaluating expression: {str(e)}")

@register_tool(name="weather", description="Get weather information for a location", complexity="standard")
async def weather(location: str, units: str = "metric") -> Dict[str, Any]:
    """
    Get weather information for a location.
    
    Args:
        location: Location to get weather for
        units: Units to use (metric or imperial)
        
    Returns:
        Weather information
    """
    # This is a mock implementation
    await asyncio.sleep(1)  # Simulate network delay
    
    import random
    
    # Generate random weather data
    temp = random.uniform(0, 30) if units == "metric" else random.uniform(32, 90)
    conditions = random.choice(["Sunny", "Cloudy", "Rainy", "Snowy", "Partly Cloudy"])
    humidity = random.uniform(30, 90)
    wind_speed = random.uniform(0, 20) if units == "metric" else random.uniform(0, 45)
    
    return {
        "location": location,
        "temperature": round(temp, 1),
        "temperature_unit": "C" if units == "metric" else "F",
        "conditions": conditions,
        "humidity": round(humidity, 1),
        "humidity_unit": "%",
        "wind_speed": round(wind_speed, 1),
        "wind_speed_unit": "km/h" if units == "metric" else "mph"
    }

@register_tool(name="translate", description="Translate text between languages", complexity="standard")
async def translate(text: str, source_language: str = "auto", target_language: str = "en") -> Dict[str, str]:
    """
    Translate text between languages.
    
    Args:
        text: Text to translate
        source_language: Source language code (or "auto" for auto-detection)
        target_language: Target language code
        
    Returns:
        Translation information
    """
    # This is a mock implementation
    await asyncio.sleep(1)  # Simulate network delay
    
    # Simple mock translation (just append language code)
    translated_text = f"{text} [{target_language}]"
    
    return {
        "original_text": text,
        "translated_text": translated_text,
        "source_language": source_language if source_language != "auto" else "en",
        "target_language": target_language
    }

@register_tool(name="summarize", description="Summarize a long text", complexity="complex")
async def summarize(text: str, max_length: int = 100) -> str:
    """
    Summarize a long text.
    
    Args:
        text: Text to summarize
        max_length: Maximum length of the summary in characters
        
    Returns:
        Summarized text
    """
    # This is a mock implementation
    await asyncio.sleep(1)  # Simulate processing delay
    
    # Simple mock summarization (just take the first sentence or truncate)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    if sentences:
        summary = sentences[0]
        if len(summary) > max_length:
            summary = summary[:max_length-3] + "..."
        return summary
    else:
        return ""
