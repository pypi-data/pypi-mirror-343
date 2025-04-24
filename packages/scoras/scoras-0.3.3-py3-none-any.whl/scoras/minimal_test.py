"""
Minimal test script for the Scoras library.

This script tests the basic functionality of the Scoras library
by creating a graph with nodes and edges and calculating complexity scores.
"""

from scoras import Graph, Node, Edge

def main():
    print("Testing Scoras Minimal Package")
    print("==============================")
    
    # Create a graph
    graph = Graph("test_graph")
    print(f"Created graph: {graph.name}")
    
    # Add nodes
    node_a = graph.add_node(Node("A", {"label": "Start"}))
    node_b = graph.add_node(Node("B", {"label": "Process"}))
    node_c = graph.add_node(Node("C", {"label": "End"}))
    
    print(f"Added nodes: {list(graph.nodes.keys())}")
    
    # Add edges
    edge_ab = graph.add_edge(Edge("A", "B", 1.0, {"type": "flow"}))
    edge_bc = graph.add_edge(Edge("B", "C", 1.0, {"type": "flow"}))
    
    print(f"Added edges: {len(graph.edges)}")
    
    # Get complexity scores
    node_score = node_a.get_complexity_score()
    edge_score = edge_ab.get_complexity_score()
    graph_score = graph.get_complexity_score()
    
    print("\nComplexity Scores:")
    print(f"Node complexity: {node_score['total_score']} ({node_score['complexity_rating']})")
    print(f"Edge complexity: {edge_score['total_score']} ({edge_score['complexity_rating']})")
    print(f"Graph complexity: {graph_score['total_score']} ({graph_score['complexity_rating']})")
    print(f"Graph components: {graph_score['components']}")
    
    print("\nScoras minimal package is working correctly!")

if __name__ == "__main__":
    main()
