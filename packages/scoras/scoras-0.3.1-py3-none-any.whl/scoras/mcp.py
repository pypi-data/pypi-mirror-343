"""
Model Context Protocol (MCP) support for the Scoras library.

This module provides integration with the Model Context Protocol (MCP),
allowing Scoras agents to act as MCP clients and servers, and enabling
the creation of MCP servers with built-in complexity scoring.

Author: Anderson L. Amaral
"""

import asyncio
import json
import logging
import os
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type, Union, TypeVar
from urllib.parse import urlparse

import aiohttp
from pydantic import BaseModel, Field, create_model

from .core import Agent, Tool, Message, ScoreTracker, ScorasConfig

# Configure logging
logger = logging.getLogger(__name__)

class MCPCapability(str, Enum):
    """Capabilities that an MCP server can support."""
    TOOLS = "tools"
    FILE_SYSTEM = "file_system"
    DATABASE = "database"
    WEB_SEARCH = "web_search"
    CODE_EXECUTION = "code_execution"
    VECTOR_STORE = "vector_store"
    STREAMING = "streaming"
    MEMORY = "memory"

class MCPServerInfo(BaseModel):
    """Information about an MCP server."""
    name: str = Field(..., description="Name of the MCP server")
    description: str = Field(..., description="Description of the MCP server")
    version: str = Field(..., description="Version of the MCP server")
    capabilities: List[str] = Field(default_factory=list, description="Capabilities of the MCP server")
    url: str = Field(..., description="URL of the MCP server")
    
    class Config:
        extra = "allow"

class MCPRequest(BaseModel):
    """Base class for MCP requests."""
    id: str = Field(..., description="Request ID")
    method: str = Field(..., description="Method name")
    params: Dict[str, Any] = Field(default_factory=dict, description="Method parameters")

class MCPResponse(BaseModel):
    """Base class for MCP responses."""
    id: str = Field(..., description="Request ID")
    result: Optional[Dict[str, Any]] = Field(None, description="Result of the method call")
    error: Optional[Dict[str, Any]] = Field(None, description="Error information if the method call failed")

class MCPContext(BaseModel):
    """Context information for an MCP request."""
    request_id: str = Field(..., description="Request ID")
    user_id: Optional[str] = Field(None, description="User ID")
    session_id: Optional[str] = Field(None, description="Session ID")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class MCPTool(BaseModel):
    """Definition of a tool in MCP."""
    name: str = Field(..., description="Name of the tool")
    description: str = Field(..., description="Description of the tool")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Parameters of the tool")
    returns: Dict[str, Any] = Field(default_factory=dict, description="Return type of the tool")
    complexity: str = Field("standard", description="Complexity of the tool (simple, standard, complex)")

class MCPClient:
    """Client for interacting with MCP servers."""
    
    def __init__(
        self,
        server_url: str,
        api_key: Optional[str] = None,
        timeout: int = 60,
        enable_scoring: bool = True
    ):
        """
        Initialize an MCP client.
        
        Args:
            server_url: URL of the MCP server
            api_key: API key for authentication
            timeout: Timeout for requests in seconds
            enable_scoring: Whether to enable complexity scoring
        """
        self.server_url = server_url
        self.api_key = api_key
        self.timeout = timeout
        self.enable_scoring = enable_scoring
        self.score_tracker = ScoreTracker() if enable_scoring else None
        
        # Add score for client creation
        if self.score_tracker:
            self.score_tracker.add_node("standard")
    
    async def get_server_info(self) -> MCPServerInfo:
        """
        Get information about the MCP server.
        
        Returns:
            Server information
        """
        async with aiohttp.ClientSession() as session:
            headers = self._get_headers()
            async with session.get(
                f"{self.server_url}/info",
                headers=headers,
                timeout=self.timeout
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return MCPServerInfo.model_validate(data)
    
    async def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        context: Optional[MCPContext] = None
    ) -> Dict[str, Any]:
        """
        Execute a tool on the MCP server.
        
        Args:
            tool_name: Name of the tool to execute
            parameters: Parameters for the tool
            context: Context information for the request
            
        Returns:
            Result of the tool execution
        """
        request_id = context.request_id if context else f"req_{os.urandom(8).hex()}"
        
        request = MCPRequest(
            id=request_id,
            method="execute_tool",
            params={
                "tool_name": tool_name,
                "parameters": parameters,
                "context": context.model_dump() if context else {}
            }
        )
        
        # Add score for tool execution
        if self.score_tracker:
            self.score_tracker.add_edge()
            self.score_tracker.add_tool()
        
        async with aiohttp.ClientSession() as session:
            headers = self._get_headers()
            async with session.post(
                f"{self.server_url}/execute",
                headers=headers,
                json=request.model_dump(),
                timeout=self.timeout
            ) as response:
                response.raise_for_status()
                data = await response.json()
                response_obj = MCPResponse.model_validate(data)
                
                if response_obj.error:
                    raise MCPError(
                        code=response_obj.error.get("code", -1),
                        message=response_obj.error.get("message", "Unknown error")
                    )
                
                return response_obj.result or {}
    
    async def get_available_tools(self) -> List[MCPTool]:
        """
        Get the list of available tools on the MCP server.
        
        Returns:
            List of available tools
        """
        async with aiohttp.ClientSession() as session:
            headers = self._get_headers()
            async with session.get(
                f"{self.server_url}/tools",
                headers=headers,
                timeout=self.timeout
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return [MCPTool.model_validate(tool) for tool in data]
    
    async def stream_tool_execution(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        context: Optional[MCPContext] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream the execution of a tool on the MCP server.
        
        Args:
            tool_name: Name of the tool to execute
            parameters: Parameters for the tool
            context: Context information for the request
            
        Yields:
            Chunks of the tool execution result
        """
        request_id = context.request_id if context else f"req_{os.urandom(8).hex()}"
        
        request = MCPRequest(
            id=request_id,
            method="stream_tool_execution",
            params={
                "tool_name": tool_name,
                "parameters": parameters,
                "context": context.model_dump() if context else {}
            }
        )
        
        # Add score for streaming tool execution
        if self.score_tracker:
            self.score_tracker.add_edge()
            self.score_tracker.add_tool("complex")
        
        async with aiohttp.ClientSession() as session:
            headers = self._get_headers()
            async with session.post(
                f"{self.server_url}/stream",
                headers=headers,
                json=request.model_dump(),
                timeout=self.timeout
            ) as response:
                response.raise_for_status()
                
                # Process SSE stream
                buffer = ""
                async for line in response.content:
                    line = line.decode("utf-8")
                    if line.startswith("data:"):
                        data = line[5:].strip()
                        if data == "[DONE]":
                            break
                        
                        try:
                            chunk = json.loads(data)
                            yield chunk
                        except json.JSONDecodeError:
                            logger.error(f"Failed to parse SSE data: {data}")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for requests to the MCP server."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        return headers
    
    def get_complexity_score(self) -> Optional[Dict[str, Any]]:
        """Get the complexity score of the MCP client."""
        if not self.score_tracker:
            return None
        
        return self.score_tracker.get_report()

class MCPError(Exception):
    """Error from an MCP server."""
    
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"MCP Error {code}: {message}")

class MCPServer:
    """Server for handling MCP requests."""
    
    def __init__(
        self,
        name: str,
        description: str,
        version: str = "1.0.0",
        capabilities: List[str] = None,
        tools: List[Tool] = None,
        enable_scoring: bool = True
    ):
        """
        Initialize an MCP server.
        
        Args:
            name: Name of the server
            description: Description of the server
            version: Version of the server
            capabilities: Capabilities of the server
            tools: Tools available on the server
            enable_scoring: Whether to enable complexity scoring
        """
        self.name = name
        self.description = description
        self.version = version
        self.capabilities = capabilities or []
        self.tools = tools or []
        self.enable_scoring = enable_scoring
        self.score_tracker = ScoreTracker() if enable_scoring else None
        
        # Add score for server creation
        if self.score_tracker:
            self.score_tracker.add_node("complex")
            
            # Add tools
            for tool in self.tools:
                self.score_tracker.add_tool(tool.complexity)
    
    def get_server_info(self) -> Dict[str, Any]:
        """
        Get information about the server.
        
        Returns:
            Server information
        """
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "capabilities": self.capabilities,
            "tools_count": len(self.tools)
        }
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Get the list of available tools.
        
        Returns:
            List of available tools
        """
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters,
                "complexity": tool.complexity
            }
            for tool in self.tools
        ]
    
    async def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Execute a tool.
        
        Args:
            tool_name: Name of the tool to execute
            parameters: Parameters for the tool
            context: Context information for the request
            
        Returns:
            Result of the tool execution
        """
        # Find the tool
        tool = next((t for t in self.tools if t.name == tool_name), None)
        if not tool:
            raise MCPError(
                code=404,
                message=f"Tool '{tool_name}' not found"
            )
        
        # Add score for tool execution
        if self.score_tracker:
            self.score_tracker.add_edge()
            self.score_tracker.add_tool(tool.complexity)
        
        # Execute the tool
        try:
            result = await tool.execute(**parameters)
            return {"result": result}
        except Exception as e:
            raise MCPError(
                code=500,
                message=f"Tool execution failed: {str(e)}"
            )
    
    def get_complexity_score(self) -> Optional[Dict[str, Any]]:
        """Get the complexity score of the MCP server."""
        if not self.score_tracker:
            return None
        
        return self.score_tracker.get_report()

class MCPAgentAdapter:
    """Adapter for using a Scoras agent as an MCP client."""
    
    def __init__(
        self,
        agent: Agent,
        enable_scoring: bool = True
    ):
        """
        Initialize an MCP agent adapter.
        
        Args:
            agent: Scoras agent to adapt
            enable_scoring: Whether to enable complexity scoring
        """
        self.agent = agent
        self.enable_scoring = enable_scoring
        self.score_tracker = ScoreTracker() if enable_scoring else None
        self.mcp_clients: Dict[str, MCPClient] = {}
        
        # Add score for adapter creation
        if self.score_tracker:
            self.score_tracker.add_node("standard")
    
    async def connect_to_server(
        self,
        server_url: str,
        api_key: Optional[str] = None,
        server_id: Optional[str] = None
    ) -> str:
        """
        Connect to an MCP server.
        
        Args:
            server_url: URL of the MCP server
            api_key: API key for authentication
            server_id: ID to use for the server (defaults to URL hostname)
            
        Returns:
            ID of the connected server
        """
        if not server_id:
            parsed_url = urlparse(server_url)
            server_id = parsed_url.netloc
        
        client = MCPClient(
            server_url=server_url,
            api_key=api_key,
            enable_scoring=self.enable_scoring
        )
        
        # Test the connection
        await client.get_server_info()
        
        # Store the client
        self.mcp_clients[server_id] = client
        
        # Add score for connection
        if self.score_tracker:
            self.score_tracker.add_edge()
        
        return server_id
    
    async def disconnect_from_server(self, server_id: str) -> None:
        """
        Disconnect from an MCP server.
        
        Args:
            server_id: ID of the server to disconnect from
        """
        if server_id in self.mcp_clients:
            del self.mcp_clients[server_id]
    
    async def execute_tool(
        self,
        server_id: str,
        tool_name: str,
        parameters: Dict[str, Any],
        context: Optional[MCPContext] = None
    ) -> Dict[str, Any]:
        """
        Execute a tool on an MCP server.
        
        Args:
            server_id: ID of the server to execute the tool on
            tool_name: Name of the tool to execute
            parameters: Parameters for the tool
            context: Context information for the request
            
        Returns:
            Result of the tool execution
        """
        if server_id not in self.mcp_clients:
            raise ValueError(f"Not connected to server '{server_id}'")
        
        client = self.mcp_clients[server_id]
        
        # Add score for tool execution
        if self.score_tracker:
            self.score_tracker.add_edge()
            self.score_tracker.add_tool()
        
        return await client.execute_tool(
            tool_name=tool_name,
            parameters=parameters,
            context=context
        )
    
    async def get_available_tools(self, server_id: str) -> List[MCPTool]:
        """
        Get the list of available tools on an MCP server.
        
        Args:
            server_id: ID of the server to get tools from
            
        Returns:
            List of available tools
        """
        if server_id not in self.mcp_clients:
            raise ValueError(f"Not connected to server '{server_id}'")
        
        client = self.mcp_clients[server_id]
        return await client.get_available_tools()
    
    async def add_mcp_tools_to_agent(self, server_id: str) -> List[Tool]:
        """
        Add tools from an MCP server to the agent.
        
        Args:
            server_id: ID of the server to get tools from
            
        Returns:
            List of added tools
        """
        if server_id not in self.mcp_clients:
            raise ValueError(f"Not connected to server '{server_id}'")
        
        client = self.mcp_clients[server_id]
        mcp_tools = await client.get_available_tools()
        
        added_tools = []
        for mcp_tool in mcp_tools:
            # Create a function that calls the MCP tool
            async def tool_function(**kwargs):
                return await client.execute_tool(
                    tool_name=mcp_tool.name,
                    parameters=kwargs
                )
            
            # Create a Scoras tool
            tool = Tool(
                name=f"mcp_{server_id}_{mcp_tool.name}",
                description=mcp_tool.description,
                function=tool_function,
                parameters=mcp_tool.parameters,
                complexity=mcp_tool.complexity
            )
            
            # Add the tool to the agent
            self.agent.add_tool(tool)
            added_tools.append(tool)
            
            # Add score for tool addition
            if self.score_tracker:
                self.score_tracker.add_tool(mcp_tool.complexity)
        
        return added_tools
    
    def get_complexity_score(self) -> Optional[Dict[str, Any]]:
        """Get the complexity score of the MCP agent adapter."""
        if not self.score_tracker:
            return None
        
        # Combine scores from all clients
        for client in self.mcp_clients.values():
            client_score = client.get_complexity_score()
            if client_score:
                for component_type, score in client_score["component_scores"].items():
                    self.score_tracker.components[component_type] += score
                
                for component_type, count in client_score["component_counts"].items():
                    self.score_tracker.component_counts[component_type] += count
        
        return self.score_tracker.get_report()

def create_mcp_server(
    name: str,
    description: str,
    tools: List[Tool],
    capabilities: List[str] = None,
    version: str = "1.0.0",
    enable_scoring: bool = True
) -> MCPServer:
    """
    Create an MCP server.
    
    Args:
        name: Name of the server
        description: Description of the server
        tools: Tools available on the server
        capabilities: Capabilities of the server
        version: Version of the server
        enable_scoring: Whether to enable complexity scoring
        
    Returns:
        An MCP server
    """
    return MCPServer(
        name=name,
        description=description,
        version=version,
        capabilities=capabilities or [MCPCapability.TOOLS.value],
        tools=tools,
        enable_scoring=enable_scoring
    )

def create_mcp_agent_adapter(
    agent: Agent,
    enable_scoring: bool = True
) -> MCPAgentAdapter:
    """
    Create an MCP agent adapter.
    
    Args:
        agent: Scoras agent to adapt
        enable_scoring: Whether to enable complexity scoring
        
    Returns:
        An MCP agent adapter
    """
    return MCPAgentAdapter(
        agent=agent,
        enable_scoring=enable_scoring
    )

async def run_mcp_server(
    server: MCPServer,
    host: str = "0.0.0.0",
    port: int = 8000,
    api_keys: List[str] = None
) -> None:
    """
    Run an MCP server using aiohttp.
    
    Args:
        server: MCP server to run
        host: Host to bind to
        port: Port to bind to
        api_keys: List of valid API keys (if None, no authentication is required)
    """
    from aiohttp import web
    
    # Create the web application
    app = web.Application()
    
    # Middleware for authentication
    @web.middleware
    async def auth_middleware(request, handler):
        if api_keys:
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return web.json_response(
                    {
                        "error": {
                            "code": 401,
                            "message": "Authentication required"
                        }
                    },
                    status=401
                )
            
            api_key = auth_header[7:]
            if api_key not in api_keys:
                return web.json_response(
                    {
                        "error": {
                            "code": 403,
                            "message": "Invalid API key"
                        }
                    },
                    status=403
                )
        
        return await handler(request)
    
    if api_keys:
        app.middlewares.append(auth_middleware)
    
    # Routes
    async def handle_info(request):
        return web.json_response(server.get_server_info())
    
    async def handle_tools(request):
        return web.json_response(server.get_available_tools())
    
    async def handle_execute(request):
        try:
            data = await request.json()
            request_obj = MCPRequest.model_validate(data)
            
            if request_obj.method != "execute_tool":
                return web.json_response(
                    {
                        "id": request_obj.id,
                        "error": {
                            "code": 400,
                            "message": f"Unsupported method: {request_obj.method}"
                        }
                    },
                    status=400
                )
            
            params = request_obj.params
            result = await server.execute_tool(
                tool_name=params["tool_name"],
                parameters=params["parameters"],
                context=params.get("context")
            )
            
            return web.json_response({
                "id": request_obj.id,
                "result": result
            })
        except MCPError as e:
            return web.json_response(
                {
                    "id": data.get("id", "unknown"),
                    "error": {
                        "code": e.code,
                        "message": e.message
                    }
                },
                status=e.code if e.code >= 400 and e.code < 600 else 500
            )
        except Exception as e:
            logger.exception("Error handling execute request")
            return web.json_response(
                {
                    "id": data.get("id", "unknown"),
                    "error": {
                        "code": 500,
                        "message": str(e)
                    }
                },
                status=500
            )
    
    async def handle_stream(request):
        try:
            data = await request.json()
            request_obj = MCPRequest.model_validate(data)
            
            if request_obj.method != "stream_tool_execution":
                return web.json_response(
                    {
                        "id": request_obj.id,
                        "error": {
                            "code": 400,
                            "message": f"Unsupported method: {request_obj.method}"
                        }
                    },
                    status=400
                )
            
            params = request_obj.params
            
            # Set up SSE response
            response = web.StreamResponse()
            response.headers["Content-Type"] = "text/event-stream"
            response.headers["Cache-Control"] = "no-cache"
            response.headers["Connection"] = "keep-alive"
            await response.prepare(request)
            
            # Find the tool
            tool_name = params["tool_name"]
            tool = next((t for t in server.tools if t.name == tool_name), None)
            if not tool:
                await response.write(
                    f"data: {json.dumps({'error': {'code': 404, 'message': f'Tool {tool_name} not found'}})}\n\n".encode()
                )
                await response.write(b"data: [DONE]\n\n")
                return response
            
            # Execute the tool
            try:
                result = await tool.execute(**params["parameters"])
                
                # Send the result
                await response.write(
                    f"data: {json.dumps({'result': result})}\n\n".encode()
                )
            except Exception as e:
                await response.write(
                    f"data: {json.dumps({'error': {'code': 500, 'message': str(e)}})}\n\n".encode()
                )
            
            # End the stream
            await response.write(b"data: [DONE]\n\n")
            return response
        except Exception as e:
            logger.exception("Error handling stream request")
            return web.json_response(
                {
                    "id": data.get("id", "unknown"),
                    "error": {
                        "code": 500,
                        "message": str(e)
                    }
                },
                status=500
            )
    
    # Add routes
    app.router.add_get("/info", handle_info)
    app.router.add_get("/tools", handle_tools)
    app.router.add_post("/execute", handle_execute)
    app.router.add_post("/stream", handle_stream)
    
    # Add a well-known agent.json endpoint
    async def handle_agent_json(request):
        return web.json_response({
            "name": server.name,
            "description": server.description,
            "version": server.version,
            "capabilities": server.capabilities,
            "url": f"http://{host}:{port}",
            "authentication": {
                "schemes": ["bearer"] if api_keys else []
            },
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "complexity": tool.complexity
                }
                for tool in server.tools
            ]
        })
    
    app.router.add_get("/.well-known/agent.json", handle_agent_json)
    
    # Run the server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    
    logger.info(f"Starting MCP server at http://{host}:{port}")
    await site.start()
    
    # Keep the server running
    while True:
        await asyncio.sleep(3600)  # Sleep for an hour
