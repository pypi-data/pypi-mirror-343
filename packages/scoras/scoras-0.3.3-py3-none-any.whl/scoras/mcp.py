"""
Model Context Protocol (MCP) implementation for Scoras.

This module provides classes and functions for implementing the MCP protocol,
allowing Scoras agents to act as MCP clients and servers.
"""

from typing import Dict, List, Any, Optional, Union, Callable, AsyncGenerator
import uuid
import json
import asyncio
from pydantic import BaseModel, Field

from .core import ScoringMixin

class MCPRequest(BaseModel):
    """
    Represents a request in the Model Context Protocol.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str
    content: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

class MCPResponse(BaseModel):
    """
    Represents a response in the Model Context Protocol.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    type: str
    content: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

class MCPSkill(ScoringMixin):
    """
    Represents a skill that can be registered with an MCP server.
    
    A skill is a capability that can be invoked by clients through the MCP protocol.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        handler: Callable,
        parameters: Optional[Dict[str, Any]] = None,
        enable_scoring: bool = True
    ):
        """
        Initialize an MCP skill.
        
        Args:
            name: Name of the skill
            description: Description of what the skill does
            handler: Function that implements the skill
            parameters: Optional parameters schema for the skill
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(enable_scoring=enable_scoring)
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.handler = handler
        self.parameters = parameters or {}
        
        # Add skill complexity score
        if self._enable_scoring:
            self._add_node_score(f"mcp_skill:{self.id}", inputs=1, outputs=1)
            self._complexity_score.components[f"skill:{name}"] = 1.0
            self._complexity_score.total_score += 1.0
            self._complexity_score.update()
    
    async def invoke(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke the skill with the given parameters.
        
        Args:
            params: Parameters for the skill
            
        Returns:
            Result of the skill execution
        """
        # In a real implementation, this would validate parameters against the schema
        result = await self.handler(params)
        return result

class MCPServer(ScoringMixin):
    """
    Implements an MCP server that can register skills and handle client requests.
    """
    
    def __init__(
        self,
        name: str = "mcp_server",
        enable_scoring: bool = True
    ):
        """
        Initialize an MCP server.
        
        Args:
            name: Name of the server
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(enable_scoring=enable_scoring)
        self.id = str(uuid.uuid4())
        self.name = name
        self.skills: Dict[str, MCPSkill] = {}
        
        # Add server complexity score
        if self._enable_scoring:
            self._add_node_score(f"mcp_server:{self.id}", inputs=1, outputs=1)
            self._complexity_score.components[f"server:{name}"] = 1.0
            self._complexity_score.total_score += 1.0
            self._complexity_score.update()
    
    def register_skill(self, skill: MCPSkill) -> None:
        """
        Register a skill with the server.
        
        Args:
            skill: Skill to register
        """
        self.skills[skill.name] = skill
        
        # Update complexity score
        if self._enable_scoring:
            self._add_edge_score(
                f"skill_connection:{skill.name}",
                path_distance=1.0,
                information_content=0.8
            )
            
            # Incorporate skill's own complexity score
            if hasattr(skill, "get_complexity_score"):
                skill_score = skill.get_complexity_score()
                if isinstance(skill_score, dict) and "total_score" in skill_score:
                    self._complexity_score.total_score += skill_score["total_score"] * 0.5
                    self._complexity_score.components[f"skill:{skill.name}"] = skill_score["total_score"] * 0.5
            
            self._complexity_score.update()
    
    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """
        Handle an MCP request.
        
        Args:
            request: Request to handle
            
        Returns:
            Response to the request
        """
        if request.type == "skill_invocation":
            skill_name = request.content.get("skill_name")
            params = request.content.get("parameters", {})
            
            if skill_name in self.skills:
                try:
                    result = await self.skills[skill_name].invoke(params)
                    return MCPResponse(
                        request_id=request.id,
                        type="skill_result",
                        content={"result": result}
                    )
                except Exception as e:
                    return MCPResponse(
                        request_id=request.id,
                        type="error",
                        content={"error": str(e)}
                    )
            else:
                return MCPResponse(
                    request_id=request.id,
                    type="error",
                    content={"error": f"Skill '{skill_name}' not found"}
                )
        elif request.type == "list_skills":
            skills_info = [
                {
                    "name": skill.name,
                    "description": skill.description,
                    "parameters": skill.parameters
                }
                for skill in self.skills.values()
            ]
            return MCPResponse(
                request_id=request.id,
                type="skills_list",
                content={"skills": skills_info}
            )
        else:
            return MCPResponse(
                request_id=request.id,
                type="error",
                content={"error": f"Unknown request type: {request.type}"}
            )

class MCPClient(ScoringMixin):
    """
    Implements an MCP client that can connect to servers and invoke skills.
    """
    
    def __init__(
        self,
        name: str = "mcp_client",
        enable_scoring: bool = True
    ):
        """
        Initialize an MCP client.
        
        Args:
            name: Name of the client
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(enable_scoring=enable_scoring)
        self.id = str(uuid.uuid4())
        self.name = name
        self.servers: Dict[str, str] = {}  # Map of server name to URL
        
        # Add client complexity score
        if self._enable_scoring:
            self._add_node_score(f"mcp_client:{self.id}", inputs=1, outputs=1)
            self._complexity_score.components[f"client:{name}"] = 1.0
            self._complexity_score.total_score += 1.0
            self._complexity_score.update()
    
    def register_server(self, server_name: str, server_url: str) -> None:
        """
        Register a server with the client.
        
        Args:
            server_name: Name of the server
            server_url: URL of the server
        """
        self.servers[server_name] = server_url
        
        # Update complexity score
        if self._enable_scoring:
            self._add_edge_score(
                f"server_connection:{server_name}",
                path_distance=1.0,
                information_content=0.8
            )
            self._complexity_score.update()
    
    async def list_skills(self, server_name: str) -> List[Dict[str, Any]]:
        """
        List skills available on a server.
        
        Args:
            server_name: Name of the server
            
        Returns:
            List of skills
        """
        if server_name not in self.servers:
            raise ValueError(f"Server '{server_name}' not registered")
        
        # In a real implementation, this would make an HTTP request to the server
        # For now, we'll just return a placeholder response
        request = MCPRequest(
            type="list_skills",
            content={}
        )
        
        # This would be the result of the HTTP request
        response = MCPResponse(
            request_id=request.id,
            type="skills_list",
            content={"skills": []}
        )
        
        return response.content["skills"]
    
    async def invoke_skill(
        self,
        server_name: str,
        skill_name: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Invoke a skill on a server.
        
        Args:
            server_name: Name of the server
            skill_name: Name of the skill to invoke
            parameters: Parameters for the skill
            
        Returns:
            Result of the skill invocation
        """
        if server_name not in self.servers:
            raise ValueError(f"Server '{server_name}' not registered")
        
        # In a real implementation, this would make an HTTP request to the server
        # For now, we'll just return a placeholder response
        request = MCPRequest(
            type="skill_invocation",
            content={
                "skill_name": skill_name,
                "parameters": parameters
            }
        )
        
        # This would be the result of the HTTP request
        response = MCPResponse(
            request_id=request.id,
            type="skill_result",
            content={"result": f"Placeholder result for {skill_name}"}
        )
        
        return response.content["result"]
    
    async def stream_skill(
        self,
        server_name: str,
        skill_name: str,
        parameters: Dict[str, Any]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream results from a skill on a server.
        
        Args:
            server_name: Name of the server
            skill_name: Name of the skill to invoke
            parameters: Parameters for the skill
            
        Yields:
            Streaming results from the skill invocation
        """
        if server_name not in self.servers:
            raise ValueError(f"Server '{server_name}' not registered")
        
        # In a real implementation, this would make a streaming HTTP request to the server
        # For now, we'll just yield a few placeholder responses
        for i in range(3):
            await asyncio.sleep(0.5)  # Simulate delay
            yield {"chunk": f"Placeholder chunk {i+1} for {skill_name}"}

def create_mcp_server(name: str = "mcp_server") -> MCPServer:
    """
    Create an MCP server.
    
    Args:
        name: Name of the server
        
    Returns:
        MCP server instance
    """
    return MCPServer(name=name)

def create_mcp_client(name: str = "mcp_client") -> MCPClient:
    """
    Create an MCP client.
    
    Args:
        name: Name of the client
        
    Returns:
        MCP client instance
    """
    return MCPClient(name=name)

# Example skill handler
async def example_skill_handler(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Example skill handler.
    
    Args:
        params: Parameters for the skill
        
    Returns:
        Result of the skill execution
    """
    return {"message": f"Processed parameters: {params}"}
