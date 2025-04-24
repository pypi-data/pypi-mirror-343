"""
Agent-to-Agent (A2A) protocol support for the Scoras library.

This module provides integration with Google's A2A protocol,
allowing Scoras agents to communicate with other agents across
different frameworks and vendors with built-in complexity scoring.

Author: Anderson L. Amaral
"""

import asyncio
import json
import logging
import os
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Type, Union, TypeVar
from urllib.parse import urljoin

import aiohttp
from pydantic import BaseModel, Field, create_model

from .core import Agent, Tool, Message, ScoreTracker, ScorasConfig

# Configure logging
logger = logging.getLogger(__name__)

class TaskState(str, Enum):
    """States that an A2A task can be in."""
    SUBMITTED = "submitted"
    WORKING = "working"
    INPUT_REQUIRED = "input-required"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"

class MessageRole(str, Enum):
    """Roles in A2A messages."""
    USER = "user"
    AGENT = "agent"

class PartType(str, Enum):
    """Types of parts in A2A messages."""
    TEXT = "text"
    FILE = "file"
    DATA = "data"

class TextPart(BaseModel):
    """Text part in an A2A message."""
    type: str = Field("text", const=True)
    text: str = Field(..., description="Text content")

class FilePart(BaseModel):
    """File part in an A2A message."""
    type: str = Field("file", const=True)
    mime_type: str = Field(..., description="MIME type of the file")
    file_name: Optional[str] = Field(None, description="Name of the file")
    bytes: Optional[str] = Field(None, description="Base64-encoded file content")
    uri: Optional[str] = Field(None, description="URI to the file")

class DataPart(BaseModel):
    """Data part in an A2A message."""
    type: str = Field("data", const=True)
    mime_type: str = Field("application/json", const=True)
    data: Dict[str, Any] = Field(..., description="JSON data")

class A2AMessage(BaseModel):
    """Message in an A2A task."""
    role: str = Field(..., description="Role of the message sender")
    parts: List[Union[TextPart, FilePart, DataPart]] = Field(
        default_factory=list, description="Parts of the message"
    )

class A2AArtifact(BaseModel):
    """Artifact produced by an A2A agent."""
    id: str = Field(..., description="Artifact ID")
    type: str = Field(..., description="Artifact type")
    parts: List[Union[TextPart, FilePart, DataPart]] = Field(
        default_factory=list, description="Parts of the artifact"
    )

class A2ATask(BaseModel):
    """Task in the A2A protocol."""
    id: str = Field(..., description="Task ID")
    state: str = Field(..., description="Current state of the task")
    messages: List[A2AMessage] = Field(default_factory=list, description="Messages in the task")
    artifacts: List[A2AArtifact] = Field(default_factory=list, description="Artifacts produced by the task")
    created_at: str = Field(..., description="ISO timestamp when the task was created")
    updated_at: str = Field(..., description="ISO timestamp when the task was last updated")
    session_id: Optional[str] = Field(None, description="Session ID for related tasks")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class AgentSkill(BaseModel):
    """Skill of an A2A agent."""
    id: str = Field(..., description="Skill ID")
    name: str = Field(..., description="Skill name")
    description: str = Field(..., description="Skill description")
    tags: List[str] = Field(default_factory=list, description="Tags for the skill")
    examples: Optional[List[str]] = Field(None, description="Example uses of the skill")
    input_modes: Optional[List[str]] = Field(None, description="Supported input modes")
    output_modes: Optional[List[str]] = Field(None, description="Supported output modes")
    complexity: str = Field("standard", description="Complexity of the skill (simple, standard, complex)")

class AgentProvider(BaseModel):
    """Provider information for an A2A agent."""
    organization: str = Field(..., description="Organization name")
    url: str = Field(..., description="Organization URL")

class AgentCapabilities(BaseModel):
    """Capabilities of an A2A agent."""
    streaming: Optional[bool] = Field(None, description="Whether the agent supports streaming")
    push_notifications: Optional[bool] = Field(None, description="Whether the agent supports push notifications")
    state_transition_history: Optional[bool] = Field(None, description="Whether the agent supports state transition history")

class AgentAuthentication(BaseModel):
    """Authentication requirements for an A2A agent."""
    schemes: List[str] = Field(..., description="Authentication schemes supported")
    credentials: Optional[str] = Field(None, description="URL to obtain credentials")

class AgentCard(BaseModel):
    """Card describing an A2A agent."""
    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="Agent description")
    url: str = Field(..., description="Agent URL")
    provider: Optional[AgentProvider] = Field(None, description="Provider information")
    version: str = Field(..., description="Agent version")
    documentation_url: Optional[str] = Field(None, description="Documentation URL")
    capabilities: AgentCapabilities = Field(default_factory=AgentCapabilities, description="Agent capabilities")
    authentication: AgentAuthentication = Field(..., description="Authentication requirements")
    default_input_modes: List[str] = Field(default_factory=list, description="Default input modes")
    default_output_modes: List[str] = Field(default_factory=list, description="Default output modes")
    skills: List[AgentSkill] = Field(default_factory=list, description="Agent skills")

class A2AClient:
    """Client for interacting with A2A agents."""
    
    def __init__(
        self,
        agent_url: str,
        api_key: Optional[str] = None,
        timeout: int = 60,
        enable_scoring: bool = True
    ):
        """
        Initialize an A2A client.
        
        Args:
            agent_url: URL of the A2A agent
            api_key: API key for authentication
            timeout: Timeout for requests in seconds
            enable_scoring: Whether to enable complexity scoring
        """
        self.agent_url = agent_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.enable_scoring = enable_scoring
        self.score_tracker = ScoreTracker() if enable_scoring else None
        self.agent_card: Optional[AgentCard] = None
        
        # Add score for client creation
        if self.score_tracker:
            self.score_tracker.add_node("standard")
    
    async def get_agent_card(self) -> AgentCard:
        """
        Get the agent card.
        
        Returns:
            Agent card
        """
        if self.agent_card:
            return self.agent_card
        
        async with aiohttp.ClientSession() as session:
            headers = self._get_headers()
            
            # Try the well-known location first
            well_known_url = f"{self.agent_url}/.well-known/agent.json"
            try:
                async with session.get(
                    well_known_url,
                    headers=headers,
                    timeout=self.timeout
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.agent_card = AgentCard.model_validate(data)
                        return self.agent_card
            except Exception as e:
                logger.warning(f"Failed to get agent card from well-known location: {e}")
            
            # Try the API endpoint
            api_url = f"{self.agent_url}/agent/card"
            try:
                async with session.get(
                    api_url,
                    headers=headers,
                    timeout=self.timeout
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.agent_card = AgentCard.model_validate(data)
                        return self.agent_card
            except Exception as e:
                logger.warning(f"Failed to get agent card from API endpoint: {e}")
            
            raise A2AError(
                code=404,
                message="Agent card not found"
            )
    
    async def send_task(
        self,
        message: str,
        task_id: Optional[str] = None,
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        files: Optional[List[Dict[str, Any]]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> A2ATask:
        """
        Send a task to the agent.
        
        Args:
            message: Message to send
            task_id: Task ID (generated if not provided)
            session_id: Session ID for related tasks
            metadata: Additional metadata
            files: List of files to include
            data: Structured data to include
            
        Returns:
            Task object
        """
        task_id = task_id or str(uuid.uuid4())
        
        # Create the message parts
        parts = [TextPart(text=message)]
        
        # Add files if provided
        if files:
            for file in files:
                parts.append(FilePart(
                    mime_type=file["mime_type"],
                    file_name=file.get("file_name"),
                    bytes=file.get("bytes"),
                    uri=file.get("uri")
                ))
        
        # Add data if provided
        if data:
            parts.append(DataPart(data=data))
        
        # Create the request payload
        payload = {
            "jsonrpc": "2.0",
            "method": "tasks/send",
            "params": {
                "task": {
                    "id": task_id,
                    "messages": [
                        {
                            "role": MessageRole.USER.value,
                            "parts": [part.model_dump() for part in parts]
                        }
                    ]
                }
            },
            "id": str(uuid.uuid4())
        }
        
        # Add session ID if provided
        if session_id:
            payload["params"]["task"]["sessionId"] = session_id
        
        # Add metadata if provided
        if metadata:
            payload["params"]["task"]["metadata"] = metadata
        
        # Add score for task sending
        if self.score_tracker:
            self.score_tracker.add_edge()
            
            # Add complexity based on parts
            if len(parts) > 1:
                self.score_tracker.add_node("complex")
            else:
                self.score_tracker.add_node("standard")
        
        # Send the request
        async with aiohttp.ClientSession() as session:
            headers = self._get_headers()
            async with session.post(
                f"{self.agent_url}/",
                headers=headers,
                json=payload,
                timeout=self.timeout
            ) as response:
                response.raise_for_status()
                data = await response.json()
                
                if "error" in data:
                    raise A2AError(
                        code=data["error"].get("code", -1),
                        message=data["error"].get("message", "Unknown error")
                    )
                
                return A2ATask.model_validate(data["result"]["task"])
    
    async def get_task(self, task_id: str) -> A2ATask:
        """
        Get a task by ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task object
        """
        payload = {
            "jsonrpc": "2.0",
            "method": "tasks/get",
            "params": {
                "taskId": task_id
            },
            "id": str(uuid.uuid4())
        }
        
        # Add score for task retrieval
        if self.score_tracker:
            self.score_tracker.add_edge()
        
        async with aiohttp.ClientSession() as session:
            headers = self._get_headers()
            async with session.post(
                f"{self.agent_url}/",
                headers=headers,
                json=payload,
                timeout=self.timeout
            ) as response:
                response.raise_for_status()
                data = await response.json()
                
                if "error" in data:
                    raise A2AError(
                        code=data["error"].get("code", -1),
                        message=data["error"].get("message", "Unknown error")
                    )
                
                return A2ATask.model_validate(data["result"]["task"])
    
    async def cancel_task(self, task_id: str) -> A2ATask:
        """
        Cancel a task.
        
        Args:
            task_id: Task ID
            
        Returns:
            Updated task object
        """
        payload = {
            "jsonrpc": "2.0",
            "method": "tasks/cancel",
            "params": {
                "taskId": task_id
            },
            "id": str(uuid.uuid4())
        }
        
        # Add score for task cancellation
        if self.score_tracker:
            self.score_tracker.add_edge()
        
        async with aiohttp.ClientSession() as session:
            headers = self._get_headers()
            async with session.post(
                f"{self.agent_url}/",
                headers=headers,
                json=payload,
                timeout=self.timeout
            ) as response:
                response.raise_for_status()
                data = await response.json()
                
                if "error" in data:
                    raise A2AError(
                        code=data["error"].get("code", -1),
                        message=data["error"].get("message", "Unknown error")
                    )
                
                return A2ATask.model_validate(data["result"]["task"])
    
    async def send_message(
        self,
        task_id: str,
        message: str,
        files: Optional[List[Dict[str, Any]]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> A2ATask:
        """
        Send a message to an existing task.
        
        Args:
            task_id: Task ID
            message: Message to send
            files: List of files to include
            data: Structured data to include
            
        Returns:
            Updated task object
        """
        # Create the message parts
        parts = [TextPart(text=message)]
        
        # Add files if provided
        if files:
            for file in files:
                parts.append(FilePart(
                    mime_type=file["mime_type"],
                    file_name=file.get("file_name"),
                    bytes=file.get("bytes"),
                    uri=file.get("uri")
                ))
        
        # Add data if provided
        if data:
            parts.append(DataPart(data=data))
        
        # Create the request payload
        payload = {
            "jsonrpc": "2.0",
            "method": "tasks/send",
            "params": {
                "task": {
                    "id": task_id,
                    "messages": [
                        {
                            "role": MessageRole.USER.value,
                            "parts": [part.model_dump() for part in parts]
                        }
                    ]
                }
            },
            "id": str(uuid.uuid4())
        }
        
        # Add score for message sending
        if self.score_tracker:
            self.score_tracker.add_edge()
            
            # Add complexity based on parts
            if len(parts) > 1:
                self.score_tracker.add_node("complex")
            else:
                self.score_tracker.add_node("standard")
        
        # Send the request
        async with aiohttp.ClientSession() as session:
            headers = self._get_headers()
            async with session.post(
                f"{self.agent_url}/",
                headers=headers,
                json=payload,
                timeout=self.timeout
            ) as response:
                response.raise_for_status()
                data = await response.json()
                
                if "error" in data:
                    raise A2AError(
                        code=data["error"].get("code", -1),
                        message=data["error"].get("message", "Unknown error")
                    )
                
                return A2ATask.model_validate(data["result"]["task"])
    
    async def stream_task(
        self,
        task_id: str,
        message: Optional[str] = None,
        files: Optional[List[Dict[str, Any]]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream updates from a task.
        
        Args:
            task_id: Task ID
            message: Optional message to send
            files: Optional list of files to include
            data: Optional structured data to include
            
        Yields:
            Task updates
        """
        # Check if the agent supports streaming
        agent_card = await self.get_agent_card()
        if not agent_card.capabilities.streaming:
            raise A2AError(
                code=400,
                message="Agent does not support streaming"
            )
        
        # Create the request payload
        payload = {
            "jsonrpc": "2.0",
            "method": "tasks/sendSubscribe",
            "params": {
                "task": {
                    "id": task_id
                }
            },
            "id": str(uuid.uuid4())
        }
        
        # Add message if provided
        if message or files or data:
            # Create the message parts
            parts = []
            if message:
                parts.append(TextPart(text=message))
            
            # Add files if provided
            if files:
                for file in files:
                    parts.append(FilePart(
                        mime_type=file["mime_type"],
                        file_name=file.get("file_name"),
                        bytes=file.get("bytes"),
                        uri=file.get("uri")
                    ))
            
            # Add data if provided
            if data:
                parts.append(DataPart(data=data))
            
            payload["params"]["task"]["messages"] = [
                {
                    "role": MessageRole.USER.value,
                    "parts": [part.model_dump() for part in parts]
                }
            ]
        
        # Add score for streaming
        if self.score_tracker:
            self.score_tracker.add_edge()
            self.score_tracker.add_node("complex")
        
        # Send the request
        async with aiohttp.ClientSession() as session:
            headers = self._get_headers()
            headers["Accept"] = "text/event-stream"
            
            async with session.post(
                f"{self.agent_url}/",
                headers=headers,
                json=payload,
                timeout=self.timeout
            ) as response:
                response.raise_for_status()
                
                # Process SSE stream
                async for line in response.content:
                    line = line.decode("utf-8").strip()
                    if not line:
                        continue
                    
                    if line.startswith("data:"):
                        data = line[5:].strip()
                        if data == "[DONE]":
                            break
                        
                        try:
                            event = json.loads(data)
                            yield event
                        except json.JSONDecodeError:
                            logger.error(f"Failed to parse SSE data: {data}")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for requests to the A2A agent."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        return headers
    
    def get_complexity_score(self) -> Optional[Dict[str, Any]]:
        """Get the complexity score of the A2A client."""
        if not self.score_tracker:
            return None
        
        return self.score_tracker.get_report()

class A2AError(Exception):
    """Error from an A2A agent."""
    
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"A2A Error {code}: {message}")

class A2AServer:
    """Server for handling A2A requests."""
    
    def __init__(
        self,
        name: str,
        description: str,
        agent: Agent,
        skills: List[AgentSkill] = None,
        version: str = "1.0.0",
        provider: Optional[AgentProvider] = None,
        documentation_url: Optional[str] = None,
        capabilities: Optional[AgentCapabilities] = None,
        authentication_schemes: List[str] = None,
        default_input_modes: List[str] = None,
        default_output_modes: List[str] = None,
        enable_scoring: bool = True
    ):
        """
        Initialize an A2A server.
        
        Args:
            name: Name of the server
            description: Description of the server
            agent: Scoras agent to use for handling tasks
            skills: Skills of the agent
            version: Version of the server
            provider: Provider information
            documentation_url: Documentation URL
            capabilities: Agent capabilities
            authentication_schemes: Authentication schemes supported
            default_input_modes: Default input modes
            default_output_modes: Default output modes
            enable_scoring: Whether to enable complexity scoring
        """
        self.name = name
        self.description = description
        self.agent = agent
        self.skills = skills or []
        self.version = version
        self.provider = provider
        self.documentation_url = documentation_url
        self.capabilities = capabilities or AgentCapabilities(
            streaming=True,
            push_notifications=False,
            state_transition_history=True
        )
        self.authentication_schemes = authentication_schemes or []
        self.default_input_modes = default_input_modes or ["text"]
        self.default_output_modes = default_output_modes or ["text"]
        self.enable_scoring = enable_scoring
        self.score_tracker = ScoreTracker() if enable_scoring else None
        self.tasks: Dict[str, A2ATask] = {}
        
        # Add score for server creation
        if self.score_tracker:
            self.score_tracker.add_node("complex")
            
            # Add complexity based on skills
            for skill in self.skills:
                self.score_tracker.add_node(skill.complexity)
    
    def get_agent_card(self) -> AgentCard:
        """
        Get the agent card.
        
        Returns:
            Agent card
        """
        return AgentCard(
            name=self.name,
            description=self.description,
            url="",  # Will be set by the HTTP server
            provider=self.provider,
            version=self.version,
            documentation_url=self.documentation_url,
            capabilities=self.capabilities,
            authentication=AgentAuthentication(
                schemes=self.authentication_schemes
            ),
            default_input_modes=self.default_input_modes,
            default_output_modes=self.default_output_modes,
            skills=self.skills
        )
    
    async def handle_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle an A2A request.
        
        Args:
            request_data: Request data
            
        Returns:
            Response data
        """
        try:
            method = request_data.get("method")
            params = request_data.get("params", {})
            request_id = request_data.get("id")
            
            if not method:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32600,
                        "message": "Invalid request: method is required"
                    },
                    "id": request_id
                }
            
            # Add score for request handling
            if self.score_tracker:
                self.score_tracker.add_edge()
            
            # Handle different methods
            if method == "tasks/send":
                task_data = params.get("task", {})
                task = await self._handle_send_task(task_data)
                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "task": task.model_dump()
                    },
                    "id": request_id
                }
            elif method == "tasks/get":
                task_id = params.get("taskId")
                task = await self._handle_get_task(task_id)
                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "task": task.model_dump()
                    },
                    "id": request_id
                }
            elif method == "tasks/cancel":
                task_id = params.get("taskId")
                task = await self._handle_cancel_task(task_id)
                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "task": task.model_dump()
                    },
                    "id": request_id
                }
            else:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    },
                    "id": request_id
                }
        except A2AError as e:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": e.code,
                    "message": e.message
                },
                "id": request_id
            }
        except Exception as e:
            logger.exception("Error handling A2A request")
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                },
                "id": request_id
            }
    
    async def _handle_send_task(self, task_data: Dict[str, Any]) -> A2ATask:
        """
        Handle a tasks/send request.
        
        Args:
            task_data: Task data
            
        Returns:
            Task object
        """
        task_id = task_data.get("id")
        if not task_id:
            raise A2AError(
                code=-32602,
                message="Invalid params: task.id is required"
            )
        
        # Check if the task already exists
        existing_task = self.tasks.get(task_id)
        if existing_task:
            # Add new messages to the existing task
            new_messages = task_data.get("messages", [])
            if new_messages:
                existing_task.messages.extend([
                    A2AMessage.model_validate(msg) for msg in new_messages
                ])
                existing_task.updated_at = datetime.utcnow().isoformat() + "Z"
                
                # Process the new messages
                await self._process_task(existing_task)
            
            return existing_task
        
        # Create a new task
        messages = task_data.get("messages", [])
        session_id = task_data.get("sessionId")
        metadata = task_data.get("metadata", {})
        
        task = A2ATask(
            id=task_id,
            state=TaskState.SUBMITTED.value,
            messages=[A2AMessage.model_validate(msg) for msg in messages],
            artifacts=[],
            created_at=datetime.utcnow().isoformat() + "Z",
            updated_at=datetime.utcnow().isoformat() + "Z",
            session_id=session_id,
            metadata=metadata
        )
        
        # Store the task
        self.tasks[task_id] = task
        
        # Process the task
        await self._process_task(task)
        
        return task
    
    async def _handle_get_task(self, task_id: str) -> A2ATask:
        """
        Handle a tasks/get request.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task object
        """
        if not task_id:
            raise A2AError(
                code=-32602,
                message="Invalid params: taskId is required"
            )
        
        task = self.tasks.get(task_id)
        if not task:
            raise A2AError(
                code=404,
                message=f"Task not found: {task_id}"
            )
        
        return task
    
    async def _handle_cancel_task(self, task_id: str) -> A2ATask:
        """
        Handle a tasks/cancel request.
        
        Args:
            task_id: Task ID
            
        Returns:
            Updated task object
        """
        if not task_id:
            raise A2AError(
                code=-32602,
                message="Invalid params: taskId is required"
            )
        
        task = self.tasks.get(task_id)
        if not task:
            raise A2AError(
                code=404,
                message=f"Task not found: {task_id}"
            )
        
        # Only cancel if the task is not already in a terminal state
        if task.state not in [
            TaskState.COMPLETED.value,
            TaskState.FAILED.value,
            TaskState.CANCELED.value
        ]:
            task.state = TaskState.CANCELED.value
            task.updated_at = datetime.utcnow().isoformat() + "Z"
        
        return task
    
    async def _process_task(self, task: A2ATask) -> None:
        """
        Process a task.
        
        Args:
            task: Task to process
        """
        # Update task state
        task.state = TaskState.WORKING.value
        task.updated_at = datetime.utcnow().isoformat() + "Z"
        
        try:
            # Extract the user messages
            user_messages = []
            for msg in task.messages:
                if msg.role == MessageRole.USER.value:
                    # Extract text parts
                    text_parts = [
                        part.text for part in msg.parts
                        if isinstance(part, TextPart) or (
                            isinstance(part, dict) and part.get("type") == "text"
                        )
                    ]
                    
                    # Extract file parts
                    file_parts = [
                        part for part in msg.parts
                        if isinstance(part, FilePart) or (
                            isinstance(part, dict) and part.get("type") == "file"
                        )
                    ]
                    
                    # Extract data parts
                    data_parts = [
                        part for part in msg.parts
                        if isinstance(part, DataPart) or (
                            isinstance(part, dict) and part.get("type") == "data"
                        )
                    ]
                    
                    # Combine text parts
                    text = "\n".join(text_parts)
                    
                    # Add to user messages
                    user_messages.append({
                        "text": text,
                        "files": file_parts,
                        "data": data_parts
                    })
            
            # Combine all user messages
            combined_message = "\n".join([msg["text"] for msg in user_messages])
            
            # Add score for message processing
            if self.score_tracker:
                self.score_tracker.add_edge()
                
                # Add complexity based on message count and parts
                if len(user_messages) > 1:
                    self.score_tracker.add_node("complex")
                else:
                    self.score_tracker.add_node("standard")
            
            # Run the agent
            agent_response = await self.agent.run(combined_message)
            
            # Create an agent message
            agent_message = A2AMessage(
                role=MessageRole.AGENT.value,
                parts=[TextPart(text=agent_response)]
            )
            
            # Add the agent message to the task
            task.messages.append(agent_message)
            
            # Update task state
            task.state = TaskState.COMPLETED.value
        except Exception as e:
            logger.exception(f"Error processing task {task.id}")
            
            # Create an error message
            error_message = A2AMessage(
                role=MessageRole.AGENT.value,
                parts=[TextPart(text=f"Error: {str(e)}")]
            )
            
            # Add the error message to the task
            task.messages.append(error_message)
            
            # Update task state
            task.state = TaskState.FAILED.value
        
        # Update task timestamp
        task.updated_at = datetime.utcnow().isoformat() + "Z"
    
    def get_complexity_score(self) -> Optional[Dict[str, Any]]:
        """Get the complexity score of the A2A server."""
        if not self.score_tracker:
            return None
        
        # Add agent score if available
        if hasattr(self.agent, "get_complexity_score") and callable(self.agent.get_complexity_score):
            agent_score = self.agent.get_complexity_score()
            if agent_score:
                for component_type, score in agent_score["component_scores"].items():
                    self.score_tracker.components[component_type] += score
                
                for component_type, count in agent_score["component_counts"].items():
                    self.score_tracker.component_counts[component_type] += count
        
        return self.score_tracker.get_report()

class A2AAgentAdapter:
    """Adapter for using a Scoras agent with the A2A protocol."""
    
    def __init__(
        self,
        agent: Agent,
        enable_scoring: bool = True
    ):
        """
        Initialize an A2A agent adapter.
        
        Args:
            agent: Scoras agent to adapt
            enable_scoring: Whether to enable complexity scoring
        """
        self.agent = agent
        self.enable_scoring = enable_scoring
        self.score_tracker = ScoreTracker() if enable_scoring else None
        self.a2a_clients: Dict[str, A2AClient] = {}
        
        # Add score for adapter creation
        if self.score_tracker:
            self.score_tracker.add_node("standard")
    
    async def connect_to_agent(
        self,
        agent_url: str,
        api_key: Optional[str] = None,
        agent_id: Optional[str] = None
    ) -> str:
        """
        Connect to an A2A agent.
        
        Args:
            agent_url: URL of the A2A agent
            api_key: API key for authentication
            agent_id: ID to use for the agent (defaults to URL hostname)
            
        Returns:
            ID of the connected agent
        """
        if not agent_id:
            from urllib.parse import urlparse
            parsed_url = urlparse(agent_url)
            agent_id = parsed_url.netloc
        
        client = A2AClient(
            agent_url=agent_url,
            api_key=api_key,
            enable_scoring=self.enable_scoring
        )
        
        # Test the connection by getting the agent card
        await client.get_agent_card()
        
        # Store the client
        self.a2a_clients[agent_id] = client
        
        # Add score for connection
        if self.score_tracker:
            self.score_tracker.add_edge()
        
        return agent_id
    
    async def disconnect_from_agent(self, agent_id: str) -> None:
        """
        Disconnect from an A2A agent.
        
        Args:
            agent_id: ID of the agent to disconnect from
        """
        if agent_id in self.a2a_clients:
            del self.a2a_clients[agent_id]
    
    async def send_task(
        self,
        agent_id: str,
        message: str,
        task_id: Optional[str] = None,
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        files: Optional[List[Dict[str, Any]]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> A2ATask:
        """
        Send a task to an A2A agent.
        
        Args:
            agent_id: ID of the agent to send the task to
            message: Message to send
            task_id: Task ID (generated if not provided)
            session_id: Session ID for related tasks
            metadata: Additional metadata
            files: List of files to include
            data: Structured data to include
            
        Returns:
            Task object
        """
        if agent_id not in self.a2a_clients:
            raise ValueError(f"Not connected to agent '{agent_id}'")
        
        client = self.a2a_clients[agent_id]
        
        # Add score for task sending
        if self.score_tracker:
            self.score_tracker.add_edge()
            
            # Add complexity based on parts
            if files or data:
                self.score_tracker.add_node("complex")
            else:
                self.score_tracker.add_node("standard")
        
        return await client.send_task(
            message=message,
            task_id=task_id,
            session_id=session_id,
            metadata=metadata,
            files=files,
            data=data
        )
    
    async def get_task(self, agent_id: str, task_id: str) -> A2ATask:
        """
        Get a task from an A2A agent.
        
        Args:
            agent_id: ID of the agent to get the task from
            task_id: Task ID
            
        Returns:
            Task object
        """
        if agent_id not in self.a2a_clients:
            raise ValueError(f"Not connected to agent '{agent_id}'")
        
        client = self.a2a_clients[agent_id]
        
        # Add score for task retrieval
        if self.score_tracker:
            self.score_tracker.add_edge()
        
        return await client.get_task(task_id)
    
    async def cancel_task(self, agent_id: str, task_id: str) -> A2ATask:
        """
        Cancel a task on an A2A agent.
        
        Args:
            agent_id: ID of the agent to cancel the task on
            task_id: Task ID
            
        Returns:
            Updated task object
        """
        if agent_id not in self.a2a_clients:
            raise ValueError(f"Not connected to agent '{agent_id}'")
        
        client = self.a2a_clients[agent_id]
        
        # Add score for task cancellation
        if self.score_tracker:
            self.score_tracker.add_edge()
        
        return await client.cancel_task(task_id)
    
    async def send_message(
        self,
        agent_id: str,
        task_id: str,
        message: str,
        files: Optional[List[Dict[str, Any]]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> A2ATask:
        """
        Send a message to an existing task on an A2A agent.
        
        Args:
            agent_id: ID of the agent to send the message to
            task_id: Task ID
            message: Message to send
            files: List of files to include
            data: Structured data to include
            
        Returns:
            Updated task object
        """
        if agent_id not in self.a2a_clients:
            raise ValueError(f"Not connected to agent '{agent_id}'")
        
        client = self.a2a_clients[agent_id]
        
        # Add score for message sending
        if self.score_tracker:
            self.score_tracker.add_edge()
            
            # Add complexity based on parts
            if files or data:
                self.score_tracker.add_node("complex")
            else:
                self.score_tracker.add_node("standard")
        
        return await client.send_message(
            task_id=task_id,
            message=message,
            files=files,
            data=data
        )
    
    async def stream_task(
        self,
        agent_id: str,
        task_id: str,
        message: Optional[str] = None,
        files: Optional[List[Dict[str, Any]]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream updates from a task on an A2A agent.
        
        Args:
            agent_id: ID of the agent to stream from
            task_id: Task ID
            message: Optional message to send
            files: Optional list of files to include
            data: Optional structured data to include
            
        Yields:
            Task updates
        """
        if agent_id not in self.a2a_clients:
            raise ValueError(f"Not connected to agent '{agent_id}'")
        
        client = self.a2a_clients[agent_id]
        
        # Add score for streaming
        if self.score_tracker:
            self.score_tracker.add_edge()
            self.score_tracker.add_node("complex")
        
        async for update in client.stream_task(
            task_id=task_id,
            message=message,
            files=files,
            data=data
        ):
            yield update
    
    def get_complexity_score(self) -> Optional[Dict[str, Any]]:
        """Get the complexity score of the A2A agent adapter."""
        if not self.score_tracker:
            return None
        
        # Combine scores from all clients
        for client in self.a2a_clients.values():
            client_score = client.get_complexity_score()
            if client_score:
                for component_type, score in client_score["component_scores"].items():
                    self.score_tracker.components[component_type] += score
                
                for component_type, count in client_score["component_counts"].items():
                    self.score_tracker.component_counts[component_type] += count
        
        return self.score_tracker.get_report()

def create_agent_skill(
    id: str,
    name: str,
    description: str,
    tags: List[str] = None,
    examples: List[str] = None,
    input_modes: List[str] = None,
    output_modes: List[str] = None,
    complexity: str = "standard"
) -> AgentSkill:
    """
    Create an A2A agent skill.
    
    Args:
        id: Skill ID
        name: Skill name
        description: Skill description
        tags: Tags for the skill
        examples: Example uses of the skill
        input_modes: Supported input modes
        output_modes: Supported output modes
        complexity: Complexity of the skill (simple, standard, complex)
        
    Returns:
        An A2A agent skill
    """
    return AgentSkill(
        id=id,
        name=name,
        description=description,
        tags=tags or [],
        examples=examples,
        input_modes=input_modes or ["text"],
        output_modes=output_modes or ["text"],
        complexity=complexity
    )

def create_a2a_server(
    name: str,
    description: str,
    agent: Agent,
    skills: List[AgentSkill] = None,
    version: str = "1.0.0",
    provider: Optional[Dict[str, str]] = None,
    documentation_url: Optional[str] = None,
    capabilities: Optional[Dict[str, bool]] = None,
    authentication_schemes: List[str] = None,
    default_input_modes: List[str] = None,
    default_output_modes: List[str] = None,
    enable_scoring: bool = True
) -> A2AServer:
    """
    Create an A2A server.
    
    Args:
        name: Name of the server
        description: Description of the server
        agent: Scoras agent to use for handling tasks
        skills: Skills of the agent
        version: Version of the server
        provider: Provider information
        documentation_url: Documentation URL
        capabilities: Agent capabilities
        authentication_schemes: Authentication schemes supported
        default_input_modes: Default input modes
        default_output_modes: Default output modes
        enable_scoring: Whether to enable complexity scoring
        
    Returns:
        An A2A server
    """
    provider_obj = None
    if provider:
        provider_obj = AgentProvider(
            organization=provider.get("organization", ""),
            url=provider.get("url", "")
        )
    
    capabilities_obj = None
    if capabilities:
        capabilities_obj = AgentCapabilities(
            streaming=capabilities.get("streaming", True),
            push_notifications=capabilities.get("push_notifications", False),
            state_transition_history=capabilities.get("state_transition_history", True)
        )
    
    return A2AServer(
        name=name,
        description=description,
        agent=agent,
        skills=skills or [],
        version=version,
        provider=provider_obj,
        documentation_url=documentation_url,
        capabilities=capabilities_obj,
        authentication_schemes=authentication_schemes or [],
        default_input_modes=default_input_modes or ["text"],
        default_output_modes=default_output_modes or ["text"],
        enable_scoring=enable_scoring
    )

def create_a2a_agent_adapter(
    agent: Agent,
    enable_scoring: bool = True
) -> A2AAgentAdapter:
    """
    Create an A2A agent adapter.
    
    Args:
        agent: Scoras agent to adapt
        enable_scoring: Whether to enable complexity scoring
        
    Returns:
        An A2A agent adapter
    """
    return A2AAgentAdapter(
        agent=agent,
        enable_scoring=enable_scoring
    )

async def run_a2a_server(
    server: A2AServer,
    host: str = "0.0.0.0",
    port: int = 8000,
    api_keys: List[str] = None
) -> None:
    """
    Run an A2A server using aiohttp.
    
    Args:
        server: A2A server to run
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
                        "jsonrpc": "2.0",
                        "error": {
                            "code": 401,
                            "message": "Authentication required"
                        },
                        "id": None
                    },
                    status=401
                )
            
            api_key = auth_header[7:]
            if api_key not in api_keys:
                return web.json_response(
                    {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": 403,
                            "message": "Invalid API key"
                        },
                        "id": None
                    },
                    status=403
                )
        
        return await handler(request)
    
    if api_keys:
        app.middlewares.append(auth_middleware)
    
    # Set the server URL
    server_url = f"http://{host}:{port}"
    
    # Routes
    async def handle_agent_json(request):
        agent_card = server.get_agent_card()
        agent_card.url = server_url
        return web.json_response(agent_card.model_dump())
    
    async def handle_jsonrpc(request):
        try:
            data = await request.json()
            response = await server.handle_request(data)
            return web.json_response(response)
        except json.JSONDecodeError:
            return web.json_response(
                {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    },
                    "id": None
                },
                status=400
            )
        except Exception as e:
            logger.exception("Error handling JSON-RPC request")
            return web.json_response(
                {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    },
                    "id": None
                },
                status=500
            )
    
    # Add routes
    app.router.add_get("/.well-known/agent.json", handle_agent_json)
    app.router.add_get("/agent/card", handle_agent_json)
    app.router.add_post("/", handle_jsonrpc)
    
    # Run the server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    
    logger.info(f"Starting A2A server at {server_url}")
    await site.start()
    
    # Keep the server running
    while True:
        await asyncio.sleep(3600)  # Sleep for an hour
