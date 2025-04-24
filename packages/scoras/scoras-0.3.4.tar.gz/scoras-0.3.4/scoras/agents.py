"""
Fix for the agents.py file to resolve the TypeError: NoneType takes no arguments error.
This script provides a corrected implementation of the Agent class and its subclasses.
"""

from typing import Any, Dict, List, Optional, Union, Callable
import uuid
from pydantic import BaseModel, Field

from .core import ScoringMixin, Message, Tool

class Agent(ScoringMixin):
    """
    Represents an intelligent agent that can process messages and use tools.
    
    An agent is a high-level abstraction that can interact with users and other agents,
    process information, and take actions using tools.
    """
    
    def __init__(
        self,
        model: Union[str, ModelConfig],
        system_prompt: str = "You are a helpful assistant.",  # Add support for system_prompt
        tools: Optional[List[Union[Tool, Callable]]] = None,  # Add support for tools
        enable_scoring: bool = True
    ):
        """
        Initialize an Agent.
        
        Args:
            model: Model configuration or string in the format 'provider:model_name'
            system_prompt: System prompt to guide the agent's behavior
            tools: Optional list of tools available to the agent
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(enable_scoring=enable_scoring)
        
        # Set up model configuration
        self.model_config = model if isinstance(model, ModelConfig) else ModelConfig.from_string(model)
        
        # Set up conversation
        self.system_prompt = system_prompt
        self.messages = [Message(role="system", content=system_prompt)]
        
        # Set up tools
        self.tools = []
        if tools:
            for tool_item in tools:
                if callable(tool_item) and hasattr(tool_item, "_tool_name"):
                    # It's a decorated function
                    self.tools.append(Tool(
                        name=tool_item._tool_name,
                        description=tool_item._tool_description,
                        function=tool_item,
                        complexity=tool_item._tool_complexity
                    ))
                elif isinstance(tool_item, Tool):
                    # It's already a Tool instance
                    self.tools.append(tool_item)
                else:
                    raise ValueError(f"Unsupported tool type: {type(tool_item)}")
        
        # Add complexity scores for the agent and its tools
        self._add_node_score("agent", inputs=1, outputs=len(self.tools) if self.tools else 1)
        
        for tool_item in self.tools:
            params_count = len(tool_item.parameters) if tool_item.parameters else 1
            complexity_map = {"simple": 0.5, "standard": 1.0, "complex": 2.0}
            execution_time = complexity_map.get(tool_item.complexity.lower(), 1.0)
            
            self._add_tool_score(
                tool_item.name,
                parameters=params_count,
                execution_time=execution_time,
                resource_usage=0.5
            )


class ExpertAgent(Agent):
    """
    An agent specialized in expert knowledge in a specific domain.
    
    This agent has enhanced capabilities for reasoning and problem-solving
    in its area of expertise.
    """
    
    def __init__(
        self,
        model: str = "openai:gpt-4",
        domain: str = "general",
        expertise_level: str = "advanced",
        temperature: float = 0.3,  # Lower temperature for more deterministic responses
        max_tokens: int = 2000,    # Higher token limit for detailed explanations
        tools: Optional[List[Tool]] = None,
        enable_scoring: bool = True
    ):
        """
        Initialize an ExpertAgent.
        
        Args:
            model: Model identifier in format "provider:model_name"
            domain: Domain of expertise
            expertise_level: Level of expertise ("basic", "intermediate", "advanced", "expert")
            temperature: Temperature for model generation (0.0-1.0)
            max_tokens: Maximum tokens to generate
            tools: Optional list of tools available to the agent
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools,
            enable_scoring=enable_scoring
        )
        self.domain = domain
        self.expertise_level = expertise_level
        
        # Add additional complexity score for expertise
        if self._enable_scoring:
            expertise_factor = {
                "basic": 0.5,
                "intermediate": 1.0,
                "advanced": 1.5,
                "expert": 2.0
            }.get(expertise_level.lower(), 1.0)
            
            self._add_node_score(f"expert_agent:{self.id}", inputs=2, outputs=2)
            self._complexity_score.components[f"expertise:{domain}"] = expertise_factor
            self._complexity_score.total_score += expertise_factor
            self._complexity_score.update()
    
    async def run(self, input_text: str) -> str:
        """
        Run the expert agent on the given input text asynchronously.
        
        Args:
            input_text: Input text to process
            
        Returns:
            Expert agent's response
        """
        # Add user message to conversation history
        self.add_message("user", input_text)
        
        # In a real implementation, this would call the model API with expert prompting
        # For now, we'll just return a placeholder response
        response = f"This is an expert response in {self.domain} at {self.expertise_level} level (async)"
        
        # Add assistant message to conversation history
        self.add_message("assistant", response)
        
        return response
    
    def run_sync(self, input_text: str) -> str:
        """
        Run the expert agent on the given input text synchronously.
        
        Args:
            input_text: Input text to process
            
        Returns:
            Expert agent's response
        """
        # Add user message to conversation history
        self.add_message("user", input_text)
        
        # In a real implementation, this would call the model API with expert prompting
        # For now, we'll just return a placeholder response
        response = f"This is an expert response in {self.domain} at {self.expertise_level} level (sync)"
        
        # Add assistant message to conversation history
        self.add_message("assistant", response)
        
        return response

class CreativeAgent(Agent):
    """
    An agent specialized in creative tasks like writing, storytelling, and idea generation.
    
    This agent has enhanced capabilities for generating creative and diverse content.
    """
    
    def __init__(
        self,
        model: str = "openai:gpt-4",
        creative_domain: str = "writing",
        style: str = "neutral",
        temperature: float = 0.9,  # Higher temperature for more creative responses
        max_tokens: int = 2000,    # Higher token limit for creative content
        tools: Optional[List[Tool]] = None,
        enable_scoring: bool = True
    ):
        """
        Initialize a CreativeAgent.
        
        Args:
            model: Model identifier in format "provider:model_name"
            creative_domain: Domain of creativity (e.g., "writing", "storytelling", "ideation")
            style: Creative style (e.g., "neutral", "formal", "casual", "poetic")
            temperature: Temperature for model generation (0.0-1.0)
            max_tokens: Maximum tokens to generate
            tools: Optional list of tools available to the agent
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools,
            enable_scoring=enable_scoring
        )
        self.creative_domain = creative_domain
        self.style = style
        
        # Add additional complexity score for creativity
        if self._enable_scoring:
            creativity_factor = 1.5  # Creative tasks are generally more complex
            
            self._add_node_score(f"creative_agent:{self.id}", inputs=2, outputs=2)
            self._complexity_score.components[f"creativity:{creative_domain}"] = creativity_factor
            self._complexity_score.total_score += creativity_factor
            self._complexity_score.update()
    
    async def run(self, input_text: str) -> str:
        """
        Run the creative agent on the given input text asynchronously.
        
        Args:
            input_text: Input text to process
            
        Returns:
            Creative agent's response
        """
        # Add user message to conversation history
        self.add_message("user", input_text)
        
        # In a real implementation, this would call the model API with creative prompting
        # For now, we'll just return a placeholder response
        response = f"This is a creative response in {self.creative_domain} with {self.style} style (async)"
        
        # Add assistant message to conversation history
        self.add_message("assistant", response)
        
        return response
    
    def run_sync(self, input_text: str) -> str:
        """
        Run the creative agent on the given input text synchronously.
        
        Args:
            input_text: Input text to process
            
        Returns:
            Creative agent's response
        """
        # Add user message to conversation history
        self.add_message("user", input_text)
        
        # In a real implementation, this would call the model API with creative prompting
        # For now, we'll just return a placeholder response
        response = f"This is a creative response in {self.creative_domain} with {self.style} style (sync)"
        
        # Add assistant message to conversation history
        self.add_message("assistant", response)
        
        return response

class MultiAgentSystem(ScoringMixin):
    """
    A system of multiple agents working together to solve complex tasks.
    
    This system coordinates multiple agents, each with different capabilities,
    to collaborate on solving problems.
    """
    
    def __init__(
        self,
        agents: List[Agent],
        coordinator: Optional[Agent] = None,
        enable_scoring: bool = True
    ):
        """
        Initialize a MultiAgentSystem.
        
        Args:
            agents: List of agents in the system
            coordinator: Optional coordinator agent to manage the system
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(enable_scoring=enable_scoring)
        self.id = str(uuid.uuid4())
        self.agents = agents
        self.coordinator = coordinator or Agent(model="openai:gpt-4", temperature=0.5)
        self.conversation_history = []
        
        # Add complexity scores
        if self._enable_scoring:
            # Base score for the multi-agent system
            self._add_node_score(f"multi_agent_system:{self.id}", inputs=len(agents), outputs=1)
            
            # Add edge scores for agent connections
            for i, agent in enumerate(agents):
                self._add_edge_score(
                    f"agent_connection:{i}",
                    path_distance=1.0,
                    information_content=0.8
                )
                
                # Incorporate agent's own complexity score
                if hasattr(agent, "get_complexity_score"):
                    agent_score = agent.get_complexity_score()
                    if isinstance(agent_score, dict) and "total_score" in agent_score:
                        self._complexity_score.total_score += agent_score["total_score"] * 0.5
                        self._complexity_score.components[f"agent:{agent.id}"] = agent_score["total_score"] * 0.5
            
            self._complexity_score.update()
    
    def add_agent(self, agent: Agent) -> None:
        """
        Add an agent to the system.
        
        Args:
            agent: Agent to add
        """
        self.agents.append(agent)
        
        # Update complexity score
        if self._enable_scoring:
            self._add_edge_score(
                f"agent_connection:{len(self.agents)-1}",
                path_distance=1.0,
                information_content=0.8
            )
            
            # Incorporate agent's own complexity score
            if hasattr(agent, "get_complexity_score"):
                agent_score = agent.get_complexity_score()
                if isinstance(agent_score, dict) and "total_score" in agent_score:
                    self._complexity_score.total_score += agent_score["total_score"] * 0.5
                    self._complexity_score.components[f"agent:{agent.id}"] = agent_score["total_score"] * 0.5
            
            self._complexity_score.update()
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a message to the conversation history.
        
        Args:
            role: Role of the message sender (e.g., "user", "assistant", "system")
            content: Content of the message
            metadata: Optional metadata for the message
        """
        message = Message(role=role, content=content, metadata=metadata or {})
        self.conversation_history.append(message)
    
    async def run(self, input_text: str) -> str:
        """
        Run the multi-agent system on the given input text asynchronously.
        
        Args:
            input_text: Input text to process
            
        Returns:
            System's response
        """
        # Add user message to conversation history
        self.add_message("user", input_text)
        
        # In a real implementation, this would coordinate multiple agents
        # For now, we'll just return a placeholder response
        response = f"This is a response from a multi-agent system with {len(self.agents)} agents (async)"
        
        # Add assistant message to conversation history
        self.add_message("assistant", response)
        
        return response
    
    def run_sync(self, input_text: str) -> str:
        """
        Run the multi-agent system on the given input text synchronously.
        
        Args:
            input_text: Input text to process
            
        Returns:
            System's response
        """
        # Add user message to conversation history
        self.add_message("user", input_text)
        
        # In a real implementation, this would coordinate multiple agents
        # For now, we'll just return a placeholder response
        response = f"This is a response from a multi-agent system with {len(self.agents)} agents (sync)"
        
        # Add assistant message to conversation history
        self.add_message("assistant", response)
        
        return response

class AgentTeam(MultiAgentSystem):
    """
    A specialized multi-agent system where agents work as a team with defined roles.
    
    This system extends MultiAgentSystem with role-based coordination and
    structured collaboration patterns.
    """
    
    def __init__(
        self,
        agents: List[Agent],
        roles: Optional[Dict[str, Agent]] = None,
        team_name: str = "agent_team",
        coordinator: Optional[Agent] = None,
        enable_scoring: bool = True
    ):
        """
        Initialize an AgentTeam.
        
        Args:
            agents: List of agents in the team
            roles: Optional mapping of role names to agents
            team_name: Name of the team
            coordinator: Optional coordinator agent to manage the team
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(
            agents=agents,
            coordinator=coordinator,
            enable_scoring=enable_scoring
        )
        self.team_name = team_name
        self.roles = roles or {}
        
        # Assign default roles if not provided
        if not roles:
            role_names = ["lead", "researcher", "critic", "creative", "implementer"]
            for i, agent in enumerate(agents):
                if i < len(role_names):
                    self.roles[role_names[i]] = agent
        
        # Add additional complexity score for team coordination
        if self._enable_scoring:
            team_factor = 1.2  # Teams have additional coordination complexity
            
            self._add_node_score(f"agent_team:{self.id}", inputs=len(agents), outputs=1)
            self._complexity_score.components[f"team_coordination:{team_name}"] = team_factor
            self._complexity_score.total_score += team_factor
            
            # Add edge scores for role connections
            for role_name, agent in self.roles.items():
                self._add_edge_score(
                    f"role_connection:{role_name}",
                    path_distance=1.0,
                    information_content=0.9
                )
            
            self._complexity_score.update()
    
    def assign_role(self, role_name: str, agent: Agent) -> None:
        """
        Assign a role to an agent.
        
        Args:
            role_name: Name of the role
            agent: Agent to assign to the role
        """
        self.roles[role_name] = agent
        
        # Update complexity score
        if self._enable_scoring:
            self._add_edge_score(
                f"role_connection:{role_name}",
                path_distance=1.0,
                information_content=0.9
            )
            self._complexity_score.update()
    
    async def run(self, input_text: str) -> str:
        """
        Run the agent team on the given input text asynchronously.
        
        Args:
            input_text: Input text to process
            
        Returns:
            Team's response
        """
        # Add user message to conversation history
        self.add_message("user", input_text)
        
        # In a real implementation, this would coordinate team members with roles
        # For now, we'll just return a placeholder response
        response = f"This is a response from the {self.team_name} team with {len(self.roles)} roles (async)"
        
        # Add assistant message to conversation history
        self.add_message("assistant", response)
        
        return response
    
    def run_sync(self, input_text: str) -> str:
        """
        Run the agent team on the given input text synchronously.
        
        Args:
            input_text: Input text to process
            
        Returns:
            Team's response
        """
        # Add user message to conversation history
        self.add_message("user", input_text)
        
        # In a real implementation, this would coordinate team members with roles
        # For now, we'll just return a placeholder response
        response = f"This is a response from the {self.team_name} team with {len(self.roles)} roles (sync)"
        
        # Add assistant message to conversation history
        self.add_message("assistant", response)
        
        return response
