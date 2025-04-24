"""
Agent-to-Agent (A2A) protocol implementation for Scoras.

This module provides classes and functions for implementing the A2A protocol,
allowing Scoras agents to communicate with agents across different frameworks and vendors.
"""

from typing import Dict, List, Any, Optional, Union, Callable, AsyncGenerator, Literal
import uuid
import json
import asyncio
from pydantic import BaseModel, Field

from .core import ScoringMixin, Message

class TextPart(BaseModel):
    """
    Represents a text part in an A2A message.
    """
    type: Literal["text"] = "text"
    text: str

class ImagePart(BaseModel):
    """
    Represents an image part in an A2A message.
    """
    type: Literal["image"] = "image"
    image_url: str
    alt_text: Optional[str] = None

class FilePart(BaseModel):
    """
    Represents a file part in an A2A message.
    """
    type: Literal["file"] = "file"
    file_url: str
    file_name: str
    mime_type: str

class A2AMessage(BaseModel):
    """
    Represents a message in the Agent-to-Agent protocol.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str
    receiver_id: str
    content: List[Union[TextPart, ImagePart, FilePart]]
    metadata: Optional[Dict[str, Any]] = None

class A2AAgent(ScoringMixin):
    """
    Implements an A2A agent that can communicate with other agents.
    """
    
    def __init__(
        self,
        name: str,
        agent_id: Optional[str] = None,
        enable_scoring: bool = True
    ):
        """
        Initialize an A2A agent.
        
        Args:
            name: Name of the agent
            agent_id: Optional unique identifier for the agent
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(enable_scoring=enable_scoring)
        self.id = agent_id or str(uuid.uuid4())
        self.name = name
        self.connections: Dict[str, "A2AAgent"] = {}
        self.message_history: List[A2AMessage] = []
        
        # Add agent complexity score
        if self._enable_scoring:
            self._add_node_score(f"a2a_agent:{self.id}", inputs=1, outputs=1)
            self._complexity_score.components[f"agent:{name}"] = 1.0
            self._complexity_score.total_score += 1.0
            self._complexity_score.update()
    
    def connect(self, agent: "A2AAgent") -> None:
        """
        Connect to another A2A agent.
        
        Args:
            agent: Agent to connect to
        """
        self.connections[agent.id] = agent
        
        # Update complexity score
        if self._enable_scoring:
            self._add_edge_score(
                f"agent_connection:{agent.id}",
                path_distance=1.0,
                information_content=0.8
            )
            self._complexity_score.update()
    
    async def send_message(
        self,
        receiver_id: str,
        content: Union[str, List[Union[TextPart, ImagePart, FilePart]]]
    ) -> A2AMessage:
        """
        Send a message to another agent.
        
        Args:
            receiver_id: ID of the receiving agent
            content: Content of the message
            
        Returns:
            Sent message
        """
        if receiver_id not in self.connections:
            raise ValueError(f"Agent '{receiver_id}' not connected")
        
        # Convert string content to TextPart
        if isinstance(content, str):
            content = [TextPart(text=content)]
        
        message = A2AMessage(
            sender_id=self.id,
            receiver_id=receiver_id,
            content=content
        )
        
        self.message_history.append(message)
        
        # In a real implementation, this would send the message to the receiver
        # For now, we'll just add it to the receiver's message history
        receiver = self.connections[receiver_id]
        receiver.message_history.append(message)
        
        return message
    
    def get_messages(
        self,
        sender_id: Optional[str] = None,
        limit: int = 10
    ) -> List[A2AMessage]:
        """
        Get messages from the message history.
        
        Args:
            sender_id: Optional ID of the sender to filter by
            limit: Maximum number of messages to return
            
        Returns:
            List of messages
        """
        if sender_id:
            messages = [m for m in self.message_history if m.sender_id == sender_id]
        else:
            messages = self.message_history.copy()
        
        return messages[-limit:]

class A2AHub(ScoringMixin):
    """
    Implements a hub for A2A agents to discover and connect to each other.
    """
    
    def __init__(
        self,
        name: str = "a2a_hub",
        enable_scoring: bool = True
    ):
        """
        Initialize an A2A hub.
        
        Args:
            name: Name of the hub
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(enable_scoring=enable_scoring)
        self.id = str(uuid.uuid4())
        self.name = name
        self.agents: Dict[str, A2AAgent] = {}
        
        # Add hub complexity score
        if self._enable_scoring:
            self._add_node_score(f"a2a_hub:{self.id}", inputs=1, outputs=1)
            self._complexity_score.components[f"hub:{name}"] = 1.5  # Hubs are more complex
            self._complexity_score.total_score += 1.5
            self._complexity_score.update()
    
    def register_agent(self, agent: A2AAgent) -> None:
        """
        Register an agent with the hub.
        
        Args:
            agent: Agent to register
        """
        self.agents[agent.id] = agent
        
        # Update complexity score
        if self._enable_scoring:
            self._add_edge_score(
                f"hub_connection:{agent.id}",
                path_distance=1.0,
                information_content=0.8
            )
            self._complexity_score.update()
    
    def get_agent(self, agent_id: str) -> Optional[A2AAgent]:
        """
        Get an agent by ID.
        
        Args:
            agent_id: ID of the agent
            
        Returns:
            Agent if found, None otherwise
        """
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """
        List all registered agents.
        
        Returns:
            List of agent information
        """
        return [
            {
                "id": agent.id,
                "name": agent.name
            }
            for agent in self.agents.values()
        ]
    
    def connect_agents(self, agent1_id: str, agent2_id: str) -> None:
        """
        Connect two agents.
        
        Args:
            agent1_id: ID of the first agent
            agent2_id: ID of the second agent
        """
        if agent1_id not in self.agents:
            raise ValueError(f"Agent '{agent1_id}' not registered")
        if agent2_id not in self.agents:
            raise ValueError(f"Agent '{agent2_id}' not registered")
        
        agent1 = self.agents[agent1_id]
        agent2 = self.agents[agent2_id]
        
        agent1.connect(agent2)
        agent2.connect(agent1)
        
        # Update complexity score
        if self._enable_scoring:
            self._add_edge_score(
                f"agent_connection:{agent1_id}_{agent2_id}",
                path_distance=1.0,
                information_content=0.9
            )
            self._complexity_score.update()

class A2ANetwork(ScoringMixin):
    """
    Implements a network of A2A agents.
    """
    
    def __init__(
        self,
        name: str = "a2a_network",
        hub: Optional[A2AHub] = None,
        enable_scoring: bool = True
    ):
        """
        Initialize an A2A network.
        
        Args:
            name: Name of the network
            hub: Optional hub for agent discovery
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(enable_scoring=enable_scoring)
        self.id = str(uuid.uuid4())
        self.name = name
        self.hub = hub or A2AHub()
        self.agents: Dict[str, A2AAgent] = {}
        
        # Add network complexity score
        if self._enable_scoring:
            self._add_node_score(f"a2a_network:{self.id}", inputs=1, outputs=1)
            self._complexity_score.components[f"network:{name}"] = 2.0  # Networks are complex
            self._complexity_score.total_score += 2.0
            
            # Incorporate hub's complexity score
            if hasattr(self.hub, "get_complexity_score"):
                hub_score = self.hub.get_complexity_score()
                if isinstance(hub_score, dict) and "total_score" in hub_score:
                    self._complexity_score.total_score += hub_score["total_score"] * 0.5
                    self._complexity_score.components[f"hub:{self.hub.id}"] = hub_score["total_score"] * 0.5
            
            self._complexity_score.update()
    
    def add_agent(self, agent: A2AAgent) -> None:
        """
        Add an agent to the network.
        
        Args:
            agent: Agent to add
        """
        self.agents[agent.id] = agent
        self.hub.register_agent(agent)
        
        # Update complexity score
        if self._enable_scoring:
            self._add_edge_score(
                f"network_connection:{agent.id}",
                path_distance=1.0,
                information_content=0.8
            )
            
            # Incorporate agent's complexity score
            if hasattr(agent, "get_complexity_score"):
                agent_score = agent.get_complexity_score()
                if isinstance(agent_score, dict) and "total_score" in agent_score:
                    self._complexity_score.total_score += agent_score["total_score"] * 0.5
                    self._complexity_score.components[f"agent:{agent.id}"] = agent_score["total_score"] * 0.5
            
            self._complexity_score.update()
    
    def connect_agents(self, agent1_id: str, agent2_id: str) -> None:
        """
        Connect two agents in the network.
        
        Args:
            agent1_id: ID of the first agent
            agent2_id: ID of the second agent
        """
        self.hub.connect_agents(agent1_id, agent2_id)
    
    def broadcast_message(
        self,
        sender_id: str,
        content: Union[str, List[Union[TextPart, ImagePart, FilePart]]]
    ) -> List[A2AMessage]:
        """
        Broadcast a message to all agents in the network.
        
        Args:
            sender_id: ID of the sending agent
            content: Content of the message
            
        Returns:
            List of sent messages
        """
        if sender_id not in self.agents:
            raise ValueError(f"Agent '{sender_id}' not in network")
        
        sender = self.agents[sender_id]
        messages = []
        
        for agent_id, agent in self.agents.items():
            if agent_id != sender_id:
                # Connect agents if not already connected
                if agent_id not in sender.connections:
                    sender.connect(agent)
                    agent.connect(sender)
                
                # Send message
                message = asyncio.run(sender.send_message(agent_id, content))
                messages.append(message)
        
        return messages

def create_a2a_agent(name: str, agent_id: Optional[str] = None) -> A2AAgent:
    """
    Create an A2A agent.
    
    Args:
        name: Name of the agent
        agent_id: Optional unique identifier for the agent
        
    Returns:
        A2A agent instance
    """
    return A2AAgent(name=name, agent_id=agent_id)

def create_a2a_network(name: str = "a2a_network") -> A2ANetwork:
    """
    Create an A2A network.
    
    Args:
        name: Name of the network
        
    Returns:
        A2A network instance
    """
    return A2ANetwork(name=name)

# Example message creation
def create_text_message(text: str) -> TextPart:
    """
    Create a text message part.
    
    Args:
        text: Text content
        
    Returns:
        Text part
    """
    return TextPart(text=text)

def create_image_message(image_url: str, alt_text: Optional[str] = None) -> ImagePart:
    """
    Create an image message part.
    
    Args:
        image_url: URL of the image
        alt_text: Optional alternative text
        
    Returns:
        Image part
    """
    return ImagePart(image_url=image_url, alt_text=alt_text)

def create_file_message(file_url: str, file_name: str, mime_type: str) -> FilePart:
    """
    Create a file message part.
    
    Args:
        file_url: URL of the file
        file_name: Name of the file
        mime_type: MIME type of the file
        
    Returns:
        File part
    """
    return FilePart(file_url=file_url, file_name=file_name, mime_type=mime_type)
