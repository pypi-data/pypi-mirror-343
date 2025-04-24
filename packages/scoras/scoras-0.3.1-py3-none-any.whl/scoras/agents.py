"""
Agents module for the Scoras library.

This module contains implementations for creating and managing various types of agents,
with integrated scoring to measure workflow complexity.

Author: Anderson L. Amaral
"""

from typing import Any, Callable, Dict, List, Optional, Type, Union, TypeVar
import json
import asyncio
from pydantic import BaseModel, Field

from .core import Agent, Message, Tool, ScorasConfig, ScoreTracker

# Implementations of specific model providers
class OpenAIProvider:
    """Provider for OpenAI models."""
    
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.settings = kwargs
        self._setup_client()
    
    def _setup_client(self):
        """Set up the OpenAI client."""
        try:
            import openai
            self.client = openai.AsyncClient(**self.settings)
        except ImportError:
            raise ImportError(
                "The 'openai' package is not installed. "
                "Install it with 'pip install openai'."
            )
    
    async def generate(self, messages: List[Message], **kwargs) -> str:
        """Generate a response from the model."""
        try:
            message_dicts = [msg.to_dict() for msg in messages]
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=message_dicts,
                **{**self.settings, **kwargs}
            )
            return response.choices[0].message.content
        except Exception as e:
            if ScorasConfig.debug:
                print(f"Error generating response with OpenAI: {e}")
            raise
    
    async def generate_with_tools(self, messages: List[Message], tools: List[Tool], **kwargs) -> Dict[str, Any]:
        """Generate a response from the model with tool calling capabilities."""
        try:
            message_dicts = [msg.to_dict() for msg in messages]
            tool_dicts = [tool.to_json_schema() for tool in tools]
            
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=message_dicts,
                tools=tool_dicts,
                **{**self.settings, **kwargs}
            )
            
            message = response.choices[0].message
            
            if message.tool_calls:
                return {
                    "content": message.content or "",
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments
                            }
                        }
                        for tool_call in message.tool_calls
                    ]
                }
            else:
                return message.content
        except Exception as e:
            if ScorasConfig.debug:
                print(f"Error generating response with tools with OpenAI: {e}")
            raise

class AnthropicProvider:
    """Provider for Anthropic models."""
    
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.settings = kwargs
        self._setup_client()
    
    def _setup_client(self):
        """Set up the Anthropic client."""
        try:
            import anthropic
            self.client = anthropic.AsyncAnthropic(**self.settings)
        except ImportError:
            raise ImportError(
                "The 'anthropic' package is not installed. "
                "Install it with 'pip install anthropic'."
            )
    
    async def generate(self, messages: List[Message], **kwargs) -> str:
        """Generate a response from the model."""
        try:
            # Convert messages to Anthropic format
            anthropic_messages = []
            system_content = None
            
            for msg in messages:
                if msg.role == "user":
                    anthropic_messages.append({"role": "user", "content": msg.content})
                elif msg.role == "assistant":
                    anthropic_messages.append({"role": "assistant", "content": msg.content})
                elif msg.role == "system":
                    # Anthropic handles system messages differently
                    system_content = msg.content
            
            response = await self.client.messages.create(
                model=self.model_name,
                messages=anthropic_messages,
                system=system_content,
                **{**self.settings, **kwargs}
            )
            return response.content[0].text
        except Exception as e:
            if ScorasConfig.debug:
                print(f"Error generating response with Anthropic: {e}")
            raise
    
    async def generate_with_tools(self, messages: List[Message], tools: List[Tool], **kwargs) -> Dict[str, Any]:
        """Generate a response from the model with tool calling capabilities."""
        try:
            # Convert messages to Anthropic format
            anthropic_messages = []
            system_content = None
            
            for msg in messages:
                if msg.role == "user":
                    anthropic_messages.append({"role": "user", "content": msg.content})
                elif msg.role == "assistant":
                    anthropic_messages.append({"role": "assistant", "content": msg.content})
                elif msg.role == "system":
                    # Anthropic handles system messages differently
                    system_content = msg.content
            
            # Convert tools to Anthropic format
            anthropic_tools = [tool.to_json_schema() for tool in tools]
            
            response = await self.client.messages.create(
                model=self.model_name,
                messages=anthropic_messages,
                system=system_content,
                tools=anthropic_tools,
                **{**self.settings, **kwargs}
            )
            
            # Check for tool calls
            if hasattr(response, 'tool_calls') and response.tool_calls:
                return {
                    "content": response.content[0].text if response.content else "",
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "function": {
                                "name": tool_call.name,
                                "arguments": json.dumps(tool_call.input)
                            }
                        }
                        for tool_call in response.tool_calls
                    ]
                }
            else:
                return response.content[0].text
        except Exception as e:
            if ScorasConfig.debug:
                print(f"Error generating response with tools with Anthropic: {e}")
            raise

class GeminiProvider:
    """Provider for Google's Gemini models."""
    
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.settings = kwargs
        self._setup_client()
    
    def _setup_client(self):
        """Set up the Gemini client."""
        try:
            import google.generativeai as genai
            
            # Configure the API
            if "api_key" in self.settings:
                genai.configure(api_key=self.settings.pop("api_key"))
            
            self.client = genai.GenerativeModel(model_name=self.model_name, **self.settings)
        except ImportError:
            raise ImportError(
                "The 'google-generativeai' package is not installed. "
                "Install it with 'pip install google-generativeai'."
            )
    
    async def generate(self, messages: List[Message], **kwargs) -> str:
        """Generate a response from the model."""
        try:
            # Convert messages to Gemini format
            gemini_messages = []
            
            for msg in messages:
                if msg.role == "user":
                    gemini_messages.append({"role": "user", "parts": [{"text": msg.content}]})
                elif msg.role == "assistant":
                    gemini_messages.append({"role": "model", "parts": [{"text": msg.content}]})
                elif msg.role == "system":
                    # Add system message as a user message at the beginning
                    if not gemini_messages:
                        gemini_messages.append({"role": "user", "parts": [{"text": f"System: {msg.content}"}]})
            
            # Run in an executor to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.generate_content(gemini_messages, **kwargs)
            )
            
            return response.text
        except Exception as e:
            if ScorasConfig.debug:
                print(f"Error generating response with Gemini: {e}")
            raise
    
    async def generate_with_tools(self, messages: List[Message], tools: List[Tool], **kwargs) -> Dict[str, Any]:
        """Generate a response from the model with tool calling capabilities."""
        # Note: This is a simplified implementation as Gemini's function calling API may differ
        try:
            # For now, just use regular generation and parse the response
            response_text = await self.generate(messages, **kwargs)
            
            # Check if the response contains a tool call (simplified parsing)
            if "I'll use the" in response_text and "tool" in response_text:
                # Try to identify which tool to use based on the response
                tool_name = None
                for tool in tools:
                    if tool.name.lower() in response_text.lower():
                        tool_name = tool.name
                        break
                
                if tool_name:
                    # Extract arguments (this is a simplified approach)
                    # In a real implementation, you'd need more sophisticated parsing
                    args_start = response_text.find("{")
                    args_end = response_text.rfind("}") + 1
                    
                    if args_start != -1 and args_end != -1:
                        try:
                            args_str = response_text[args_start:args_end]
                            args = json.loads(args_str)
                            
                            return {
                                "content": response_text,
                                "tool_calls": [
                                    {
                                        "id": "gemini_tool_call_1",
                                        "function": {
                                            "name": tool_name,
                                            "arguments": json.dumps(args)
                                        }
                                    }
                                ]
                            }
                        except json.JSONDecodeError:
                            pass
            
            # If no tool call detected or parsing failed, return the text response
            return response_text
        except Exception as e:
            if ScorasConfig.debug:
                print(f"Error generating response with tools with Gemini: {e}")
            raise

# Function to create an agent with the appropriate provider
def create_agent(
    model: str = None,
    system_prompt: str = None,
    tools: List[Tool] = None,
    result_type: Type[BaseModel] = None,
    enable_scoring: bool = True,
    **kwargs
) -> Agent:
    """
    Create an agent with the appropriate provider based on the model string.
    
    Args:
        model: Model identifier (e.g., "openai:gpt-4o", "anthropic:claude-3-opus", "gemini:gemini-pro")
        system_prompt: System prompt for the agent
        tools: List of tools available to the agent
        result_type: Expected result type (Pydantic model)
        enable_scoring: Whether to enable complexity scoring
        **kwargs: Additional settings for the model
        
    Returns:
        A configured agent
    """
    agent = Agent(
        model=model,
        system_prompt=system_prompt,
        tools=tools,
        result_type=result_type,
        enable_scoring=enable_scoring,
        **kwargs
    )
    
    # Configure the appropriate provider
    if model:
        if model.startswith("openai:"):
            model_name = model.split(":", 1)[1]
            agent.provider = OpenAIProvider(model_name, **kwargs)
        elif model.startswith("anthropic:"):
            model_name = model.split(":", 1)[1]
            agent.provider = AnthropicProvider(model_name, **kwargs)
        elif model.startswith("gemini:"):
            model_name = model.split(":", 1)[1]
            agent.provider = GeminiProvider(model_name, **kwargs)
    
    return agent

# Specialized agent classes
class ExpertAgent(Agent):
    """Agent specialized for expert knowledge in a specific domain."""
    
    def __init__(
        self,
        model: str = None,
        domain: str = "general",
        expertise_level: str = "advanced",
        tools: List[Tool] = None,
        enable_scoring: bool = True,
        **kwargs
    ):
        # Create a system prompt based on domain and expertise
        system_prompt = f"You are an {expertise_level} expert in {domain}. "
        
        if domain == "science":
            system_prompt += "Provide accurate, evidence-based scientific information. Cite sources when possible."
        elif domain == "programming":
            system_prompt += "Provide clear, efficient code solutions and explain your implementation choices."
        elif domain == "finance":
            system_prompt += "Provide accurate financial analysis and advice based on sound economic principles."
        elif domain == "medicine":
            system_prompt += "Provide medical information for educational purposes only. Always advise consulting healthcare professionals."
        elif domain == "legal":
            system_prompt += "Provide legal information for educational purposes only. Always advise consulting legal professionals."
        else:
            system_prompt += "Provide helpful, accurate information in response to questions."
        
        super().__init__(
            model=model,
            system_prompt=system_prompt,
            tools=tools,
            enable_scoring=enable_scoring,
            **kwargs
        )
        
        self.domain = domain
        self.expertise_level = expertise_level
        
        # Add domain-specific metadata to track expertise
        self.metadata = {
            "agent_type": "expert",
            "domain": domain,
            "expertise_level": expertise_level
        }

class CreativeAgent(Agent):
    """Agent specialized for creative tasks like writing, storytelling, or idea generation."""
    
    def __init__(
        self,
        model: str = None,
        creative_mode: str = "balanced",
        style_guide: Optional[str] = None,
        tools: List[Tool] = None,
        enable_scoring: bool = True,
        **kwargs
    ):
        # Adjust temperature based on creative mode
        if creative_mode == "conservative":
            kwargs["temperature"] = kwargs.get("temperature", 0.5)
        elif creative_mode == "balanced":
            kwargs["temperature"] = kwargs.get("temperature", 0.7)
        elif creative_mode == "experimental":
            kwargs["temperature"] = kwargs.get("temperature", 0.9)
        
        # Create a system prompt based on creative mode and style guide
        system_prompt = "You are a creative assistant specialized in generating engaging and original content. "
        
        if creative_mode == "conservative":
            system_prompt += "Focus on clarity, coherence, and conventional approaches while maintaining creativity."
        elif creative_mode == "balanced":
            system_prompt += "Balance creativity with practicality, generating fresh ideas that remain accessible."
        elif creative_mode == "experimental":
            system_prompt += "Prioritize novelty and unconventional approaches, pushing boundaries with innovative ideas."
        
        if style_guide:
            system_prompt += f"\n\nStyle Guide: {style_guide}"
        
        super().__init__(
            model=model,
            system_prompt=system_prompt,
            tools=tools,
            enable_scoring=enable_scoring,
            **kwargs
        )
        
        self.creative_mode = creative_mode
        self.style_guide = style_guide
        
        # Add creativity-specific metadata
        self.metadata = {
            "agent_type": "creative",
            "creative_mode": creative_mode,
            "has_style_guide": style_guide is not None
        }

class RAGAgent(Agent):
    """Agent specialized for Retrieval Augmented Generation."""
    
    def __init__(
        self,
        model: str = None,
        retriever: Callable[[str], List[str]] = None,
        citation_style: str = "inline",
        tools: List[Tool] = None,
        enable_scoring: bool = True,
        **kwargs
    ):
        system_prompt = (
            "You are a specialized agent for answering questions based on provided information. "
            "Only use the information in the context to answer questions. "
            "If the information isn't in the context, indicate that you can't answer based on the available information."
        )
        
        if citation_style == "inline":
            system_prompt += "\nInclude inline citations when referencing specific information from the context."
        elif citation_style == "academic":
            system_prompt += "\nUse academic-style citations with numbered references when referencing information."
        elif citation_style == "minimal":
            system_prompt += "\nOnly cite sources when absolutely necessary, focusing on providing clear information."
        
        super().__init__(
            model=model,
            system_prompt=system_prompt,
            tools=tools,
            enable_scoring=enable_scoring,
            **kwargs
        )
        
        self.retriever = retriever
        self.citation_style = citation_style
        
        # Add RAG-specific metadata
        self.metadata = {
            "agent_type": "rag",
            "citation_style": citation_style
        }
        
        # Add score for retriever if scoring is enabled
        if self.score_tracker and self.retriever:
            self.score_tracker.add_node("complex")
    
    async def run(self, user_input: str, **kwargs) -> Any:
        """Run the agent with the given user input, retrieving relevant information first."""
        if self.retriever:
            # Retrieve relevant documents
            documents = self.retriever(user_input)
            
            # Format the context
            context = "\n\n".join(documents)
            
            # Format the user input with the context
            enhanced_input = f"Context:\n{context}\n\nQuestion: {user_input}"
            
            # Run the agent with the enhanced input
            return await super().run(enhanced_input, **kwargs)
        else:
            # If no retriever is available, run normally
            return await super().run(user_input, **kwargs)

class MultiAgentSystem:
    """System for coordinating multiple agents with integrated scoring."""
    
    def __init__(self, agents: Dict[str, Agent], enable_scoring: bool = True):
        self.agents = agents
        self.enable_scoring = enable_scoring
        self.score_tracker = ScoreTracker() if enable_scoring else None
        
        # Add score for multi-agent system
        if self.score_tracker:
            self.score_tracker.add_node("complex")
            
            # Add edges between agents (conceptual)
            for i in range(len(agents) - 1):
                self.score_tracker.add_edge()
            
            # Incorporate scores from individual agents
            for agent_id, agent in agents.items():
                if agent.enable_scoring and agent.score_tracker:
                    for component, score in agent.score_tracker.components.items():
                        self.score_tracker.components[component] += score
                        self.score_tracker.total_score += score
                    for component, count in agent.score_tracker.component_counts.items():
                        self.score_tracker.component_counts[component] += count
    
    async def run(self, agent_id: str, user_input: str, **kwargs) -> Any:
        """Run a specific agent with the given user input."""
        if agent_id not in self.agents:
            raise ValueError(f"Agent '{agent_id}' not found")
        
        return await self.agents[agent_id].run(user_input, **kwargs)
    
    def run_sync(self, agent_id: str, user_input: str, **kwargs) -> Any:
        """Synchronous version of run."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        return loop.run_until_complete(self.run(agent_id, user_input, **kwargs))
    
    async def run_sequence(self, user_input: str, agent_sequence: List[str], **kwargs) -> List[Any]:
        """Run a sequence of agents, passing the output of each as input to the next."""
        results = []
        current_input = user_input
        
        for agent_id in agent_sequence:
            if agent_id not in self.agents:
                raise ValueError(f"Agent '{agent_id}' not found")
            
            result = await self.agents[agent_id].run(current_input, **kwargs)
            results.append(result)
            
            # The output of this agent becomes the input for the next
            if isinstance(result, BaseModel):
                current_input = result.model_dump_json()
            else:
                current_input = str(result)
        
        return results
    
    def run_sequence_sync(self, user_input: str, agent_sequence: List[str], **kwargs) -> List[Any]:
        """Synchronous version of run_sequence."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        return loop.run_until_complete(self.run_sequence(user_input, agent_sequence, **kwargs))
    
    async def run_parallel(self, user_input: str, agent_ids: List[str], **kwargs) -> Dict[str, Any]:
        """Run multiple agents in parallel with the same input."""
        tasks = {}
        for agent_id in agent_ids:
            if agent_id not in self.agents:
                raise ValueError(f"Agent '{agent_id}' not found")
            
            tasks[agent_id] = self.run(agent_id, user_input, **kwargs)
        
        # Wait for all tasks to complete
        results = {}
        for agent_id, task in tasks.items():
            results[agent_id] = await task
        
        return results
    
    def run_parallel_sync(self, user_input: str, agent_ids: List[str], **kwargs) -> Dict[str, Any]:
        """Synchronous version of run_parallel."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        return loop.run_until_complete(self.run_parallel(user_input, agent_ids, **kwargs))
    
    def get_complexity_score(self) -> Optional[Dict[str, Any]]:
        """Get the complexity score of the multi-agent system."""
        if not self.score_tracker:
            return None
        
        return self.score_tracker.get_report()

class AgentTeam:
    """A team of agents that collaborate to solve complex tasks with defined roles."""
    
    def __init__(
        self,
        coordinator: Agent,
        specialists: Dict[str, Agent],
        enable_scoring: bool = True,
        **kwargs
    ):
        self.coordinator = coordinator
        self.specialists = specialists
        self.enable_scoring = enable_scoring
        self.score_tracker = ScoreTracker() if enable_scoring else None
        self.conversation_history = []
        
        # Add score for agent team
        if self.score_tracker:
            # Complex node for the team structure
            self.score_tracker.add_node("complex")
            
            # Add edges from coordinator to each specialist
            for _ in specialists:
                self.score_tracker.add_edge(True)  # Conditional edges
            
            # Incorporate scores from individual agents
            if coordinator.enable_scoring and coordinator.score_tracker:
                for component, score in coordinator.score_tracker.components.items():
                    self.score_tracker.components[component] += score
                    self.score_tracker.total_score += score
                for component, count in coordinator.score_tracker.component_counts.items():
                    self.score_tracker.component_counts[component] += count
            
            for specialist_id, specialist in specialists.items():
                if specialist.enable_scoring and specialist.score_tracker:
                    for component, score in specialist.score_tracker.components.items():
                        self.score_tracker.components[component] += score
                        self.score_tracker.total_score += score
                    for component, count in specialist.score_tracker.component_counts.items():
                        self.score_tracker.component_counts[component] += count
    
    async def run(self, user_input: str, max_turns: int = 5, **kwargs) -> str:
        """Run the agent team to collaboratively solve a task."""
        # Add user input to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Prepare the initial context for the coordinator
        context = (
            "You are the coordinator of a team of specialist agents. "
            "Your task is to break down the user's request and delegate to specialists as needed.\n\n"
            f"Available specialists: {', '.join(self.specialists.keys())}\n\n"
            f"User request: {user_input}"
        )
        
        # Start the collaboration process
        for turn in range(max_turns):
            # Coordinator decides what to do
            coordinator_response = await self.coordinator.run(context, **kwargs)
            self.conversation_history.append({"role": "coordinator", "content": coordinator_response})
            
            # Check if coordinator wants to delegate to a specialist
            specialist_to_call = None
            specialist_query = None
            
            for specialist_id in self.specialists.keys():
                if f"Ask {specialist_id}" in coordinator_response or f"Delegate to {specialist_id}" in coordinator_response:
                    specialist_to_call = specialist_id
                    # Extract the query for the specialist
                    query_start = coordinator_response.find(f"Query for {specialist_id}:")
                    if query_start != -1:
                        query_start += len(f"Query for {specialist_id}:")
                        query_end = coordinator_response.find("\n\n", query_start)
                        if query_end == -1:
                            query_end = len(coordinator_response)
                        specialist_query = coordinator_response[query_start:query_end].strip()
                    break
            
            # If no explicit query was found but a specialist was mentioned, use the user's input
            if specialist_to_call and not specialist_query:
                specialist_query = user_input
            
            # If a specialist was identified, call them
            if specialist_to_call and specialist_query:
                specialist = self.specialists[specialist_to_call]
                specialist_response = await specialist.run(specialist_query, **kwargs)
                
                self.conversation_history.append({
                    "role": "specialist",
                    "name": specialist_to_call,
                    "content": specialist_response
                })
                
                # Update context for coordinator with specialist's response
                context += f"\n\n{specialist_to_call}'s response: {specialist_response}"
            
            # Check if the coordinator indicates the task is complete
            if "Final answer:" in coordinator_response or "Task complete" in coordinator_response:
                # Extract the final answer
                final_start = coordinator_response.find("Final answer:")
                if final_start != -1:
                    final_start += len("Final answer:")
                    final_answer = coordinator_response[final_start:].strip()
                    return final_answer
                else:
                    return coordinator_response
        
        # If we've reached the maximum number of turns, return the coordinator's last response
        return f"(Reached maximum turns) {coordinator_response}"
    
    def run_sync(self, user_input: str, max_turns: int = 5, **kwargs) -> str:
        """Synchronous version of run."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        return loop.run_until_complete(self.run(user_input, max_turns, **kwargs))
    
    def get_complexity_score(self) -> Optional[Dict[str, Any]]:
        """Get the complexity score of the agent team."""
        if not self.score_tracker:
            return None
        
        return self.score_tracker.get_report()
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the conversation history of the agent team."""
        return self.conversation_history
