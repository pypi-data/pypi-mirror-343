"""
Scoras package initialization.
"""

__version__ = "0.3.1"  # Updated version
__author__ = "Anderson L. Amaral"

# Import core functionality
from .core import ScoringMixin, Graph, Node, Edge, Agent

# Provide convenience imports
__all__ = ['ScoringMixin', 'Graph', 'Node', 'Edge', 'Agent']
from scoras.core import Graph, Node, Edge, Message, Tool, RAG, ScoreTracker, ScorasConfig, WorkflowGraph, ScoringMixin
from scoras.agents import Agent, ExpertAgent, CreativeAgent, MultiAgentSystem, AgentTeam
from scoras.rag import SimpleRAG, ContextualRAG, Document, Retriever
from scoras.tools import tool, ToolChain, ToolRouter, ToolBuilder, ToolResult
from scoras.mcp import MCPServer, MCPClient, MCPSkill, create_mcp_server, create_mcp_client
from scoras.a2a import A2AAgent, A2ANetwork, A2AHub, create_a2a_agent, create_a2a_network
