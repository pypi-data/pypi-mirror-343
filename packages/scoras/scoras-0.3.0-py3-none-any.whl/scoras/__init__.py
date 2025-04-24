"""
Scoras package initialization.
"""

__version__ = "0.3.0"  # Updated version
__author__ = "Anderson L. Amaral"

# Import core functionality
from .core import ScoringMixin, Graph, Node, Edge, Agent

# Provide convenience imports
__all__ = ['ScoringMixin', 'Graph', 'Node', 'Edge', 'Agent']
