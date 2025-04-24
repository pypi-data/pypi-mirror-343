"""
Core functionality for the Scoras library.
"""
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel

class ScoringMixin:
    """Base class that provides complexity scoring functionality."""
    
    def __init__(self):
        self._complexity_score = 0
        self._enable_scoring = True
    
    def add_complexity(self, points: float, reason: str = ""):
        """Add complexity points to the total score."""
        if self._enable_scoring:
            self._complexity_score += points
            return True
        return False
    
    def get_complexity_score(self) -> Dict[str, Any]:
        """Get the current complexity score and rating."""
        score = self._complexity_score
        
        # Determine complexity rating based on score
        if score < 5:
            rating = "Simple"
        elif score < 10:
            rating = "Standard"
        elif score < 20:
            rating = "Complex"
        elif score < 50:
            rating = "Very Complex"
        else:
            rating = "Extremely Complex"
        
        return {
            "total_score": score,
            "complexity_rating": rating,
            "components": {
                "base": score
            }
        }

class Node(ScoringMixin):
    """Represents a node in a graph."""
    
    def __init__(self, id: str, metadata: Optional[Dict[str, Any]] = None):
        super().__init__()
        self.id = id
        self.metadata = metadata or {}
        self.add_complexity(1.0, "Node creation")
    
    def __repr__(self):
        return f"Node(id='{self.id}')"

class Edge(ScoringMixin):
    """Represents an edge between two nodes in a graph."""
    
    def __init__(self, source: str, target: str, weight: float = 1.0, metadata: Optional[Dict[str, Any]] = None):
        super().__init__()
        self.source = source
        self.target = target
        self.weight = weight
        self.metadata = metadata or {}
        self.add_complexity(1.0, "Edge creation")
    
    def __repr__(self):
        return f"Edge(source='{self.source}', target='{self.target}', weight={self.weight})"

class Graph(ScoringMixin):
    """Represents a graph with nodes and edges."""
    
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.add_complexity(1.0, "Graph creation")
    
    def add_node(self, node: Node) -> Node:
        """Add a node to the graph."""
        self.nodes[node.id] = node
        self.add_complexity(0.5, f"Added node {node.id}")
        return node
    
    def add_edge(self, edge: Edge) -> Edge:
        """Add an edge to the graph."""
        if edge.source not in self.nodes:
            raise ValueError(f"Source node '{edge.source}' not found in graph")
        if edge.target not in self.nodes:
            raise ValueError(f"Target node '{edge.target}' not found in graph")
        
        self.edges.append(edge)
        self.add_complexity(1.0, f"Added edge from {edge.source} to {edge.target}")
        return edge
    
    def get_complexity_score(self) -> Dict[str, Any]:
        """Get the complexity score of the graph, including all nodes and edges."""
        base_score = super().get_complexity_score()
        
        # Add complexity from nodes and edges
        node_score = sum(node.get_complexity_score()["total_score"] for node in self.nodes.values())
        edge_score = sum(edge.get_complexity_score()["total_score"] for edge in self.edges)
        
        total_score = base_score["total_score"] + node_score + edge_score
        
        # Determine complexity rating based on total score
        if total_score < 5:
            rating = "Simple"
        elif total_score < 10:
            rating = "Standard"
        elif total_score < 20:
            rating = "Complex"
        elif total_score < 50:
            rating = "Very Complex"
        else:
            rating = "Extremely Complex"
        
        return {
            "total_score": total_score,
            "complexity_rating": rating,
            "components": {
                "base": base_score["total_score"],
                "nodes": node_score,
                "edges": edge_score
            }
        }
    
    def __repr__(self):
        return f"Graph(name='{self.name}', nodes={len(self.nodes)}, edges={len(self.edges)})"

class Agent(ScoringMixin):
    """Represents an AI agent with complexity scoring."""
    
    def __init__(self, model: str, system_prompt: str = None):
        super().__init__()
        self.model = model
        self.system_prompt = system_prompt or "You are a helpful assistant."
        self.tools = []
        self.add_complexity(2.0, "Agent creation")
    
    def add_tool(self, tool):
        """Add a tool to the agent."""
        self.tools.append(tool)
        self.add_complexity(1.0, f"Added tool: {getattr(tool, 'name', 'unnamed')}")
        return tool
    
    def run_sync(self, query: str) -> str:
        """Synchronous version of run method (simplified for minimal implementation)."""
        self.add_complexity(1.0, "Agent execution")
        return f"Response to: {query}"
    
    async def run(self, query: str) -> str:
        """Run the agent with a query (simplified for minimal implementation)."""
        self.add_complexity(1.0, "Agent execution")
        return f"Response to: {query}"
    
    def get_complexity_score(self) -> Dict[str, Any]:
        """Get the complexity score of the agent, including all tools."""
        base_score = super().get_complexity_score()
        
        # Add complexity from tools if they have scoring
        tool_score = 0
        for tool in self.tools:
            if hasattr(tool, 'get_complexity_score'):
                tool_score += tool.get_complexity_score()["total_score"]
            else:
                tool_score += 1.0  # Default score for tools without scoring
        
        total_score = base_score["total_score"] + tool_score
        
        # Determine complexity rating based on total score
        if total_score < 5:
            rating = "Simple"
        elif total_score < 10:
            rating = "Standard"
        elif total_score < 20:
            rating = "Complex"
        elif total_score < 50:
            rating = "Very Complex"
        else:
            rating = "Extremely Complex"
        
        return {
            "total_score": total_score,
            "complexity_rating": rating,
            "components": {
                "base": base_score["total_score"],
                "tools": tool_score
            }
        }
    
    def __repr__(self):
        return f"Agent(model='{self.model}', tools={len(self.tools)})"
