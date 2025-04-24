"""
Scoras: Intelligent Agent Framework with Complexity Scoring

This module provides the core functionality for the Scoras framework.
"""

from typing import Any, Dict, List, Optional, Union, Callable, TypeVar, Generic
import math
from pydantic import BaseModel, Field

# Type definitions
T = TypeVar('T')
StateType = TypeVar('StateType', bound=BaseModel)

class ComplexityScore(BaseModel):
    """Model representing a complexity score with detailed breakdown."""
    
    total_score: float = Field(0.0, description="Total complexity score")
    node_score: float = Field(0.0, description="Contribution from nodes")
    edge_score: float = Field(0.0, description="Contribution from edges")
    tool_score: float = Field(0.0, description="Contribution from tools")
    condition_score: float = Field(0.0, description="Contribution from conditions")
    components: Dict[str, float] = Field(default_factory=dict, description="Detailed breakdown by component")
    complexity_rating: str = Field("Simple", description="Human-readable complexity rating")
    
    def calculate_rating(self) -> str:
        """Calculate the complexity rating based on the total score."""
        if self.total_score < 10:
            return "Simple"
        elif self.total_score < 25:
            return "Moderate"
        elif self.total_score < 50:
            return "Complex"
        elif self.total_score < 100:
            return "Very Complex"
        else:
            return "Extremely Complex"
    
    def update(self) -> "ComplexityScore":
        """Update the complexity rating based on the current scores."""
        self.complexity_rating = self.calculate_rating()
        return self

class ScoringMixin:
    """Mixin class that provides complexity scoring functionality."""
    
    def __init__(self, enable_scoring: bool = True):
        self._complexity_score = ComplexityScore()
        self._enable_scoring = enable_scoring
        
    def get_complexity_score(self) -> Dict[str, Any]:
        """
        Get the current complexity score.
        
        Returns:
            Dictionary containing complexity score information
        """
        if not self._enable_scoring:
            return {"scoring_disabled": True}
        
        return self._complexity_score.model_dump()
    
    def _add_node_score(self, name: str, inputs: int = 1, outputs: int = 1, max_factor: int = 10) -> None:
        """
        Add a node's contribution to the complexity score.
        
        Args:
            name: Name of the node
            inputs: Number of input connections
            outputs: Number of output connections
            max_factor: Normalization factor
        """
        if not self._enable_scoring:
            return
            
        # Calculate node complexity using the formula: 1 + 0.5 * (inputs * outputs / max_factor)
        node_complexity = 1.0 + 0.5 * min(1.0, (inputs * outputs) / max_factor)
        
        self._complexity_score.node_score += node_complexity
        self._complexity_score.total_score += node_complexity
        self._complexity_score.components[f"node:{name}"] = node_complexity
        self._complexity_score.update()
    
    def _add_edge_score(
        self, 
        name: str, 
        path_distance: float = 1.0, 
        max_distance: float = 10.0,
        information_content: float = 0.5,
        alpha: float = 0.5
    ) -> None:
        """
        Add an edge's contribution to the complexity score.
        
        Args:
            name: Name of the edge
            path_distance: Distance between connected nodes
            max_distance: Maximum possible path distance
            information_content: Measure of data complexity (0-1)
            alpha: Scaling factor for information content
        """
        if not self._enable_scoring:
            return
            
        # Calculate edge complexity using the formula:
        # 1.5 + 2.5 * (path_distance / max_distance) * (1 + alpha * information_content)
        normalized_distance = min(1.0, path_distance / max_distance)
        info_factor = 1.0 + alpha * information_content
        edge_complexity = 1.5 + 2.5 * normalized_distance * info_factor
        
        self._complexity_score.edge_score += edge_complexity
        self._complexity_score.total_score += edge_complexity
        self._complexity_score.components[f"edge:{name}"] = edge_complexity
        self._complexity_score.update()
    
    def _add_tool_score(
        self,
        name: str,
        parameters: int = 1,
        execution_time: float = 1.0,
        resource_usage: float = 0.5,
        max_parameters: int = 10,
        max_execution_time: float = 10.0,
        max_resource_usage: float = 1.0
    ) -> None:
        """
        Add a tool's contribution to the complexity score.
        
        Args:
            name: Name of the tool
            parameters: Number of parameters
            execution_time: Estimated execution time
            resource_usage: Resource utilization (0-1)
            max_parameters: Maximum expected parameters
            max_execution_time: Maximum expected execution time
            max_resource_usage: Maximum expected resource usage
        """
        if not self._enable_scoring:
            return
            
        # Calculate tool complexity using the formula:
        # 1.4 + 1.6 * (parameters * execution_time * resource_usage) / (max_parameters * max_execution_time * max_resource_usage)
        normalized_params = min(1.0, parameters / max_parameters)
        normalized_time = min(1.0, execution_time / max_execution_time)
        normalized_resources = min(1.0, resource_usage / max_resource_usage)
        
        combined_factor = normalized_params * normalized_time * normalized_resources
        tool_complexity = 1.4 + 1.6 * combined_factor
        
        self._complexity_score.tool_score += tool_complexity
        self._complexity_score.total_score += tool_complexity
        self._complexity_score.components[f"tool:{name}"] = tool_complexity
        self._complexity_score.update()
    
    def _add_condition_score(self, name: str, branches: int = 2) -> None:
        """
        Add a condition's contribution to the complexity score.
        
        Args:
            name: Name of the condition
            branches: Number of possible branches
        """
        if not self._enable_scoring:
            return
            
        # Calculate condition complexity using the formula: 2.5 * (1 + log2(branches))
        # Ensure branches is at least 2 to avoid negative log values
        branches = max(2, branches)
        condition_complexity = 2.5 * (1.0 + math.log2(branches))
        
        self._complexity_score.condition_score += condition_complexity
        self._complexity_score.total_score += condition_complexity
        self._complexity_score.components[f"condition:{name}"] = condition_complexity
        self._complexity_score.update()

class Node(ScoringMixin):
    """
    Represents a node in a workflow graph.
    
    A node is a basic processing unit that performs a specific function.
    """
    
    def __init__(
        self,
        name: str,
        function: Optional[Callable] = None,  # Make function optional
        complexity: str = "standard",
        enable_scoring: bool = True
    ):
        """
        Initialize a Node.
        
        Args:
            name: Name of the node
            function: Function to execute when the node is called (optional in 0.3.3 for backward compatibility)
            complexity: Complexity level ("simple", "standard", "complex")
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(enable_scoring=enable_scoring)
        self.name = name
        self.function = function or (lambda x: x)  # Default to identity function if None
        self.complexity = complexity
        self.inputs = []
        self.outputs = []
        
        # Add initial complexity score
        complexity_map = {"simple": 1.0, "standard": 1.2, "complex": 1.5}
        complexity_value = complexity_map.get(complexity.lower(), 1.2)
        self._add_node_score(name, inputs=1, outputs=1, max_factor=10)

class Edge(ScoringMixin):
    """
    Represents an edge in a workflow graph.
    
    An edge connects two nodes and defines the flow of data between them.
    """
    
    def __init__(
        self,
        source: Node,
        target: Node,
        name: Optional[str] = None,
        condition: Optional[Callable[[Any], bool]] = None,
        transform: Optional[Callable[[Any], Any]] = None,
        enable_scoring: bool = True
    ):
        """
        Initialize an Edge.
        
        Args:
            source: Source node
            target: Target node
            name: Optional name for the edge
            condition: Optional condition function that determines if the edge is traversed
            transform: Optional function to transform data flowing through the edge
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(enable_scoring=enable_scoring)
        self.source = source
        self.target = target
        self.name = name or f"{source.name}_to_{target.name}"
        self.condition = condition
        self.transform = transform
        
        # Update node connections
        source.outputs.append(self)
        target.inputs.append(self)
        
        # Add edge complexity score
        path_distance = 1.0  # Default distance
        information_content = 0.5  # Default information content
        
        if condition is not None:
            # Edges with conditions are more complex
            information_content += 0.3
            
        if transform is not None:
            # Edges with transformations are more complex
            information_content += 0.2
            
        self._add_edge_score(
            self.name,
            path_distance=path_distance,
            information_content=information_content
        )
        
        # If there's a condition, add a condition score
        if condition is not None:
            self._add_condition_score(f"{self.name}_condition", branches=2)
    
    async def traverse(self, data: Any) -> Optional[Any]:
        """
        Traverse the edge asynchronously.
        
        Args:
            data: Data to pass through the edge
            
        Returns:
            Transformed data if the edge is traversed, None otherwise
        """
        # Check if the edge should be traversed
        if self.condition is not None and not self.condition(data):
            return None
            
        # Transform the data if needed
        if self.transform is not None:
            data = self.transform(data)
            
        return data
    
    def traverse_sync(self, data: Any) -> Optional[Any]:
        """
        Traverse the edge synchronously.
        
        Args:
            data: Data to pass through the edge
            
        Returns:
            Transformed data if the edge is traversed, None otherwise
        """
        # Check if the edge should be traversed
        if self.condition is not None and not self.condition(data):
            return None
            
        # Transform the data if needed
        if self.transform is not None:
            data = self.transform(data)
            
        return data

class Graph(ScoringMixin, Generic[StateType]):
    """
    Represents a workflow graph.
    
    A graph consists of nodes connected by edges, defining a workflow.
    """
    
    def __init__(
        self,
        name: str = "workflow",
        state_type: Optional[type] = None,
        enable_scoring: bool = True
    ):
        """
        Initialize a Graph.
        
        Args:
            name: Name of the graph
            state_type: Optional type for the graph state
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(enable_scoring=enable_scoring)
        self.name = name
        self.state_type = state_type
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.start_nodes: List[Node] = []
        self.end_nodes: List[Node] = []
    
    def add_node(
        self,
        name: str,
        function: Callable,
        complexity: str = "standard"
    ) -> Node:
        """
        Add a node to the graph.
        
        Args:
            name: Name of the node
            function: Function to execute when the node is called
            complexity: Complexity level ("simple", "standard", "complex")
            
        Returns:
            The created node
        """
        node = Node(name, function, complexity, enable_scoring=self._enable_scoring)
        self.nodes[name] = node
        
        # If this is the first node, make it a start node
        if not self.nodes:
            self.start_nodes.append(node)
            
        return node
    
    def add_edge(
        self,
        source: Union[str, Node],
        target: Union[str, Node],
        name: Optional[str] = None,
        condition: Optional[Callable[[Any], bool]] = None,
        transform: Optional[Callable[[Any], Any]] = None
    ) -> Edge:
        """
        Add an edge to the graph.
        
        Args:
            source: Source node or node name
            target: Target node or node name
            name: Optional name for the edge
            condition: Optional condition function that determines if the edge is traversed
            transform: Optional function to transform data flowing through the edge
            
        Returns:
            The created edge
        """
        # Get the source and target nodes
        source_node = source if isinstance(source, Node) else self.nodes[source]
        target_node = target if isinstance(target, Node) else self.nodes[target]
        
        # Create the edge
        edge = Edge(
            source_node,
            target_node,
            name,
            condition,
            transform,
            enable_scoring=self._enable_scoring
        )
        
        self.edges.append(edge)
        
        # Update end nodes
        if source_node in self.end_nodes:
            self.end_nodes.remove(source_node)
        if target_node not in self.start_nodes and not target_node.inputs:
            self.start_nodes.append(target_node)
        if not target_node.outputs:
            self.end_nodes.append(target_node)
            
        return edge
    
    def compile(self) -> "WorkflowExecutor[StateType]":
        """
        Compile the graph into an executable workflow.
        
        Returns:
            WorkflowExecutor instance
        """
        return WorkflowExecutor(self)

# Add the missing classes

class Message(BaseModel):
    """
    Represents a message in a conversation.
    
    Messages are used for communication between agents and users.
    """
    
    role: str = Field(..., description="Role of the message sender (e.g., 'user', 'assistant', 'system')")
    content: str = Field(..., description="Content of the message")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata for the message")
    
    def __str__(self) -> str:
        """String representation of the message."""
        return f"{self.role}: {self.content[:50]}..." if len(self.content) > 50 else self.content

class Tool(ScoringMixin):
    """
    Represents a tool that can be used by an agent.
    
    Tools provide specific capabilities to agents, allowing them to perform
    actions beyond just generating text.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        function: Callable,
        parameters: Optional[List[Dict[str, Any]]] = None,
        complexity: str = "standard",
        enable_scoring: bool = True
    ):
        """
        Initialize a Tool.
        
        Args:
            name: Name of the tool
            description: Description of what the tool does
            function: Function to call when the tool is used
            parameters: Optional list of parameter specifications
            complexity: Complexity level ("simple", "standard", "complex")
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(enable_scoring=enable_scoring)
        self.name = name
        self.description = description
        self.function = function
        self.parameters = parameters or []
        self.complexity = complexity
        
        # Add complexity score for the tool
        complexity_map = {"simple": 0.5, "standard": 1.0, "complex": 2.0}
        execution_time = complexity_map.get(complexity.lower(), 1.0)
        
        self._add_tool_score(
            name,
            parameters=len(self.parameters),
            execution_time=execution_time,
            resource_usage=0.5
        )
    
    async def execute(self, **kwargs) -> Any:
        """
        Execute the tool with the provided parameters.
        
        Args:
            **kwargs: Parameters for the tool
            
        Returns:
            Result of the tool execution
        """
        import asyncio
        
        # Execute the function
        if asyncio.iscoroutinefunction(self.function):
            return await self.function(**kwargs)
        else:
            return self.function(**kwargs)
    
    def execute_sync(self, **kwargs) -> Any:
        """
        Execute the tool synchronously with the provided parameters.
        
        Args:
            **kwargs: Parameters for the tool
            
        Returns:
            Result of the tool execution
        """
        import asyncio
        
        # Create an event loop if there isn't one
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Run the async method in the event loop
        return loop.run_until_complete(self.execute(**kwargs))

class RAG(ScoringMixin):
    """
    Base class for RAG (Retrieval-Augmented Generation) systems.
    
    RAG systems combine document retrieval with language model generation.
    """
    
    def __init__(
        self,
        retriever: Any,
        agent: Any,
        enable_scoring: bool = True
    ):
        """
        Initialize a RAG system.
        
        Args:
            retriever: Document retriever
            agent: Agent for generation
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(enable_scoring=enable_scoring)
        self.retriever = retriever
        self.agent = agent
        
        # Add complexity score for the RAG system
        self._add_node_score("rag_system", inputs=2, outputs=1)
        self._add_edge_score(
            "retriever_to_agent",
            path_distance=1.0,
            information_content=0.8
        )
    
    async def run(self, query: str, top_k: int = 3) -> str:
        """
        Process a query using the RAG system.
        
        Args:
            query: Query string
            top_k: Number of documents to retrieve
            
        Returns:
            Generated response
        """
        raise NotImplementedError("Subclasses must implement run method")
    
    def run_sync(self, query: str, top_k: int = 3) -> str:
        """
        Process a query synchronously using the RAG system.
        
        Args:
            query: Query string
            top_k: Number of documents to retrieve
            
        Returns:
            Generated response
        """
        import asyncio
        
        # Create an event loop if there isn't one
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Run the async method in the event loop
        return loop.run_until_complete(self.run(query, top_k))

class ScoreTracker:
    """
    Utility class for tracking and analyzing complexity scores.
    
    This class provides methods for tracking, comparing, and visualizing
    complexity scores across different components and workflows.
    """
    
    def __init__(self):
        """Initialize a ScoreTracker."""
        self.scores = {}
    
    def add_score(self, name: str, score: Dict[str, Any]) -> None:
        """
        Add a complexity score to the tracker.
        
        Args:
            name: Name to associate with the score
            score: Complexity score dictionary
        """
        self.scores[name] = score
    
    def get_score(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a complexity score by name.
        
        Args:
            name: Name of the score to retrieve
            
        Returns:
            Complexity score dictionary if found, None otherwise
        """
        return self.scores.get(name)
    
    def compare_scores(self, name1: str, name2: str) -> Dict[str, Any]:
        """
        Compare two complexity scores.
        
        Args:
            name1: Name of the first score
            name2: Name of the second score
            
        Returns:
            Dictionary with comparison results
        """
        score1 = self.get_score(name1)
        score2 = self.get_score(name2)
        
        if not score1 or not score2:
            return {"error": "One or both scores not found"}
        
        return {
            "name1": name1,
            "name2": name2,
            "total_score1": score1.get("total_score", 0),
            "total_score2": score2.get("total_score", 0),
            "difference": score1.get("total_score", 0) - score2.get("total_score", 0),
            "complexity_rating1": score1.get("complexity_rating", "Unknown"),
            "complexity_rating2": score2.get("complexity_rating", "Unknown")
        }
    
    def get_all_scores(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all tracked complexity scores.
        
        Returns:
            Dictionary mapping names to complexity scores
        """
        return self.scores

class ScorasConfig(BaseModel):
    """
    Configuration for the Scoras framework.
    
    This class provides configuration options for various aspects of the framework.
    """
    
    enable_scoring: bool = Field(True, description="Whether to enable complexity scoring")
    default_model: str = Field("openai:gpt-4", description="Default model to use for agents")
    default_temperature: float = Field(0.7, description="Default temperature for model generation")
    default_max_tokens: int = Field(1000, description="Default maximum tokens for model generation")
    default_top_k: int = Field(3, description="Default number of documents to retrieve in RAG systems")
    log_level: str = Field("INFO", description="Logging level")
    
    class Config:
        """Pydantic configuration."""
        validate_assignment = True

class WorkflowGraph(Graph):
    """
    Enhanced graph for defining complex workflows.
    
    This class extends the basic Graph class with additional functionality
    for defining and executing complex workflows.
    """
    
    def __init__(
        self,
        name: str = "workflow",
        state_type: Optional[type] = None,
        enable_scoring: bool = True
    ):
        """
        Initialize a WorkflowGraph.
        
        Args:
            name: Name of the graph
            state_type: Optional type for the graph state
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(name, state_type, enable_scoring)
        self.branches: Dict[str, "WorkflowGraph"] = {}
    
    def add_branch(
        self,
        name: str,
        condition: Callable[[Any], bool]
    ) -> "WorkflowGraph":
        """
        Add a branch to the workflow.
        
        Args:
            name: Name of the branch
            condition: Condition function that determines if the branch is taken
            
        Returns:
            The created branch graph
        """
        branch = WorkflowGraph(f"{self.name}_{name}", self.state_type, self._enable_scoring)
        self.branches[name] = branch
        
        # Add complexity score for the branch
        self._add_condition_score(f"branch_{name}", branches=2)
        
        return branch
    
    def merge_branch(
        self,
        branch_name: str,
        target_node: Union[str, Node]
    ) -> Edge:
        """
        Merge a branch back into the main workflow.
        
        Args:
            branch_name: Name of the branch to merge
            target_node: Target node or node name in the main workflow
            
        Returns:
            The created edge
        """
        if branch_name not in self.branches:
            raise ValueError(f"Branch not found: {branch_name}")
            
        branch = self.branches[branch_name]
        
        if not branch.end_nodes:
            raise ValueError(f"Branch has no end nodes: {branch_name}")
            
        # Get the target node
        target_node_obj = target_node if isinstance(target_node, Node) else self.nodes[target_node]
        
        # Create edges from each end node in the branch to the target node
        edges = []
        for end_node in branch.end_nodes:
            edge = Edge(
                end_node,
                target_node_obj,
                f"{branch_name}_to_{target_node_obj.name}",
                enable_scoring=self._enable_scoring
            )
            self.edges.append(edge)
            edges.append(edge)
            
            # Add complexity score for merging the branch
            self._add_edge_score(
                f"merge_{branch_name}",
                path_distance=2.0,
                information_content=0.7
            )
        
        return edges[0] if edges else None

class WorkflowExecutor(Generic[StateType]):
    """
    Executes a compiled workflow graph.
    """
    
    def __init__(self, graph: Graph[StateType]):
        """
        Initialize a WorkflowExecutor.
        
        Args:
            graph: The workflow graph to execute
        """
        self.graph = graph
    
    async def run(self, initial_state: StateType) -> StateType:
        """
        Run the workflow asynchronously.
        
        Args:
            initial_state: Initial state for the workflow
            
        Returns:
            Final state after workflow execution
        """
        # Validate the initial state
        if self.graph.state_type is not None and not isinstance(initial_state, self.graph.state_type):
            raise TypeError(f"Initial state must be of type {self.graph.state_type.__name__}")
            
        # Start with the initial state
        state = initial_state
        
        # Process each start node
        for node in self.graph.start_nodes:
            # Execute the node
            node_result = await node.execute(state)
            
            # Update the state if the result is of the correct type
            if self.graph.state_type is None or isinstance(node_result, self.graph.state_type):
                state = node_result
            
            # Process outgoing edges
            await self._process_edges(node, state)
            
        return state
    
    async def _process_edges(self, node: Node, state: StateType) -> None:
        """
        Process outgoing edges from a node.
        
        Args:
            node: The node to process edges from
            state: Current state
        """
        for edge in node.outputs:
            # Traverse the edge
            edge_result = await edge.traverse(state)
            
            # If the edge was traversed, process the target node
            if edge_result is not None:
                # Execute the target node
                node_result = await edge.target.execute(edge_result)
                
                # Update the state if the result is of the correct type
                if self.graph.state_type is None or isinstance(node_result, self.graph.state_type):
                    state = node_result
                
                # Process outgoing edges from the target node
                await self._process_edges(edge.target, state)
    
    def run_sync(self, initial_state: StateType) -> StateType:
        """
        Run the workflow synchronously.
        
        Args:
            initial_state: Initial state for the workflow
            
        Returns:
            Final state after workflow execution
        """
        import asyncio
        
        # Create an event loop if there isn't one
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Run the async method in the event loop
        return loop.run_until_complete(self.run(initial_state))

# For backward compatibility
Agent = None  # This will be imported from agents.py
