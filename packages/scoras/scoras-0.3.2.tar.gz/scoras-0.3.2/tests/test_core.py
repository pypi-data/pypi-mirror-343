import unittest
import asyncio
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from scoras.core import Graph, Node, Edge

class TestScoringMixin(unittest.TestCase):
    """Test the ScoringMixin class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scoring = ScoringMixin()
    
    def test_initialization(self):
        """Test initialization of ScoringMixin."""
        self.assertTrue(self.scoring._enable_scoring)
        self.assertIsInstance(self.scoring._complexity_score, ComplexityScore)
        
        # Test with scoring disabled
        scoring_disabled = ScoringMixin(enable_scoring=False)
        self.assertFalse(scoring_disabled._enable_scoring)
    
    def test_add_node_score(self):
        """Test adding a node score."""
        self.scoring._add_node_score("test_node", inputs=2, outputs=3)
        self.assertGreater(self.scoring._complexity_score.total_score, 0)
        self.assertIn("node_test_node", self.scoring._complexity_score.components)
    
    def test_add_edge_score(self):
        """Test adding an edge score."""
        self.scoring._add_edge_score("test_edge", path_distance=0.5, information_content=0.7)
        self.assertGreater(self.scoring._complexity_score.total_score, 0)
        self.assertIn("edge_test_edge", self.scoring._complexity_score.components)
    
    def test_add_condition_score(self):
        """Test adding a condition score."""
        self.scoring._add_condition_score("test_condition", branches=4)
        self.assertGreater(self.scoring._complexity_score.total_score, 0)
        self.assertIn("condition_test_condition", self.scoring._complexity_score.components)
    
    def test_add_tool_score(self):
        """Test adding a tool score."""
        self.scoring._add_tool_score("test_tool", parameters=3, execution_time=0.8, resource_usage=0.5)
        self.assertGreater(self.scoring._complexity_score.total_score, 0)
        self.assertIn("tool_test_tool", self.scoring._complexity_score.components)
    
    def test_get_complexity_score(self):
        """Test getting the complexity score."""
        # Add some scores
        self.scoring._add_node_score("test_node", inputs=2, outputs=3)
        self.scoring._add_edge_score("test_edge", path_distance=0.5, information_content=0.7)
        
        # Get the score
        score = self.scoring.get_complexity_score()
        
        # Check the result
        self.assertIsInstance(score, dict)
        self.assertIn("total_score", score)
        self.assertIn("complexity_rating", score)
        self.assertIn("components", score)
        
        # Check that the components are included
        self.assertIn("node_test_node", score["components"])
        self.assertIn("edge_test_edge", score["components"])
    
    def test_disabled_scoring(self):
        """Test behavior when scoring is disabled."""
        scoring_disabled = ScoringMixin(enable_scoring=False)
        
        # Add some scores (should be ignored)
        scoring_disabled._add_node_score("test_node", inputs=2, outputs=3)
        
        # Get the score
        score = scoring_disabled.get_complexity_score()
        
        # Check that the score is empty
        self.assertEqual(score["total_score"], 0)
        self.assertEqual(score["complexity_rating"], "Simple")
        self.assertEqual(score["components"], {})

class TestComplexityScore(unittest.TestCase):
    """Test the ComplexityScore class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.score = ComplexityScore()
    
    def test_initialization(self):
        """Test initialization of ComplexityScore."""
        self.assertEqual(self.score.total_score, 0)
        self.assertEqual(self.score.complexity_rating, "Simple")
        self.assertEqual(self.score.components, {})
    
    def test_update_rating(self):
        """Test updating the complexity rating."""
        # Test different score ranges
        self.score.total_score = 3
        self.score.update()
        self.assertEqual(self.score.complexity_rating, "Simple")
        
        self.score.total_score = 10
        self.score.update()
        self.assertEqual(self.score.complexity_rating, "Moderate")
        
        self.score.total_score = 20
        self.score.update()
        self.assertEqual(self.score.complexity_rating, "Complex")
        
        self.score.total_score = 40
        self.score.update()
        self.assertEqual(self.score.complexity_rating, "Very Complex")
        
        self.score.total_score = 60
        self.score.update()
        self.assertEqual(self.score.complexity_rating, "Extremely Complex")
    
    def test_to_dict(self):
        """Test converting to dictionary."""
        # Add some components
        self.score.components = {
            "node_test": 1.5,
            "edge_test": 2.0
        }
        self.score.total_score = 3.5
        self.score.update()
        
        # Convert to dict
        result = self.score.to_dict()
        
        # Check the result
        self.assertIsInstance(result, dict)
        self.assertEqual(result["total_score"], 3.5)
        self.assertEqual(result["complexity_rating"], "Simple")
        self.assertEqual(result["components"]["node_test"], 1.5)
        self.assertEqual(result["components"]["edge_test"], 2.0)

class TestNode(unittest.TestCase):
    """Test the Node class."""
    
    def test_initialization(self):
        """Test initialization of Node."""
        node = Node(id="test", inputs=2, outputs=3)
        self.assertEqual(node.id, "test")
        self.assertEqual(node.inputs, 2)
        self.assertEqual(node.outputs, 3)
    
    def test_calculate_complexity(self):
        """Test calculating node complexity."""
        # Simple node
        node1 = Node(id="test1", inputs=1, outputs=1)
        self.assertAlmostEqual(node1.calculate_complexity(), 0.0, places=2)
        
        # More complex node
        node2 = Node(id="test2", inputs=3, outputs=4)
        self.assertGreater(node2.calculate_complexity(), 0)
        
        # Node with scaling factor
        node3 = Node(id="test3", inputs=2, outputs=2, scaling_factor=2.0)
        self.assertAlmostEqual(node3.calculate_complexity(), 2.0, places=2)

class TestEdge(unittest.TestCase):
    """Test the Edge class."""
    
    def test_initialization(self):
        """Test initialization of Edge."""
        edge = Edge(id="test", path_distance=0.5, information_content=0.7)
        self.assertEqual(edge.id, "test")
        self.assertEqual(edge.path_distance, 0.5)
        self.assertEqual(edge.information_content, 0.7)
    
    def test_calculate_complexity(self):
        """Test calculating edge complexity."""
        # Simple edge
        edge1 = Edge(id="test1", path_distance=0.1, information_content=0.1)
        self.assertGreater(edge1.calculate_complexity(), 0)
        
        # More complex edge
        edge2 = Edge(id="test2", path_distance=0.9, information_content=0.9)
        self.assertGreater(edge2.calculate_complexity(), edge1.calculate_complexity())
        
        # Edge with scaling factor
        edge3 = Edge(id="test3", path_distance=0.5, information_content=0.5, scaling_factor=2.0)
        self.assertGreater(edge3.calculate_complexity(), edge1.calculate_complexity())

class TestGraph(unittest.TestCase):
    """Test the Graph class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.graph = Graph()
    
    def test_add_node(self):
        """Test adding a node to the graph."""
        self.graph.add_node("node1", inputs=2, outputs=3)
        self.assertEqual(len(self.graph.nodes), 1)
        self.assertIn("node1", self.graph.nodes)
    
    def test_add_edge(self):
        """Test adding an edge to the graph."""
        self.graph.add_edge("edge1", "node1", "node2", path_distance=0.5, information_content=0.7)
        self.assertEqual(len(self.graph.edges), 1)
        self.assertIn("edge1", self.graph.edges)
    
    def test_calculate_complexity(self):
        """Test calculating graph complexity."""
        # Add nodes and edges
        self.graph.add_node("node1", inputs=2, outputs=3)
        self.graph.add_node("node2", inputs=1, outputs=2)
        self.graph.add_edge("edge1", "node1", "node2", path_distance=0.5, information_content=0.7)
        
        # Calculate complexity
        complexity = self.graph.calculate_complexity()
        
        # Check the result
        self.assertGreater(complexity, 0)
        
        # Add more nodes and edges
        self.graph.add_node("node3", inputs=3, outputs=1)
        self.graph.add_edge("edge2", "node2", "node3", path_distance=0.8, information_content=0.6)
        
        # Calculate complexity again
        new_complexity = self.graph.calculate_complexity()
        
        # Check that complexity increased
        self.assertGreater(new_complexity, complexity)

class TestWorkflowExecutor(unittest.TestCase):
    """Test the WorkflowExecutor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.graph = Graph()
        self.graph.add_node("start", inputs=0, outputs=1)
        self.graph.add_node("process", inputs=1, outputs=1)
        self.graph.add_node("end", inputs=1, outputs=0)
        self.graph.add_edge("edge1", "start", "process", path_distance=0.5, information_content=0.7)
        self.graph.add_edge("edge2", "process", "end", path_distance=0.6, information_content=0.8)
        
        self.executor = WorkflowExecutor(self.graph)
    
    def test_initialization(self):
        """Test initialization of WorkflowExecutor."""
        self.assertEqual(self.executor.graph, self.graph)
        self.assertEqual(self.executor.current_node, None)
    
    def test_start_workflow(self):
        """Test starting a workflow."""
        self.executor.start_workflow("start")
        self.assertEqual(self.executor.current_node, "start")
    
    def test_transition(self):
        """Test transitioning between nodes."""
        self.executor.start_workflow("start")
        self.executor.transition("process")
        self.assertEqual(self.executor.current_node, "process")
        
        # Test invalid transition
        with self.assertRaises(ValueError):
            self.executor.transition("invalid")
    
    def test_get_complexity_score(self):
        """Test getting the complexity score of the workflow."""
        # Start and execute the workflow
        self.executor.start_workflow("start")
        self.executor.transition("process")
        self.executor.transition("end")
        
        # Get the complexity score
        score = self.executor.get_complexity_score()
        
        # Check the result
        self.assertIsInstance(score, dict)
        self.assertIn("total_score", score)
        self.assertIn("complexity_rating", score)
        self.assertGreater(score["total_score"], 0)

if __name__ == "__main__":
    unittest.main()
