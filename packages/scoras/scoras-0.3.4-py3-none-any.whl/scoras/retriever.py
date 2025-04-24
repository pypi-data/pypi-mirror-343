"""
Implementation of the Retriever class for the Scoras library.
This file provides the Retriever base class for document retrieval in RAG systems.
"""

from typing import List, Dict, Any, Optional, Union
from .core import ScoringMixin
from .rag import Document

class Retriever(ScoringMixin):
    """
    Base class for document retrievers in a RAG system.
    
    A retriever is responsible for finding relevant documents based on a query.
    """
    
    def __init__(self, enable_scoring: bool = True):
        """
        Initialize a retriever.
        
        Args:
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(enable_scoring=enable_scoring)
        
        # Add retriever complexity score
        if self._enable_scoring:
            self._add_node_score("retriever", inputs=1, outputs=1)
            self._complexity_score.components["retrieval"] = 1.0
            self._complexity_score.total_score += 1.0
            self._complexity_score.update()
    
    async def retrieve(self, query: str, top_k: int = 5) -> List[Document]:
        """
        Retrieve relevant documents based on the query asynchronously.
        
        Args:
            query: Query to retrieve documents for
            top_k: Number of documents to retrieve
            
        Returns:
            List of retrieved documents
        """
        # This is a base class, subclasses should implement this method
        raise NotImplementedError("Subclasses must implement retrieve method")
    
    def retrieve_sync(self, query: str, top_k: int = 5) -> List[Document]:
        """
        Retrieve relevant documents based on the query synchronously.
        
        Args:
            query: Query to retrieve documents for
            top_k: Number of documents to retrieve
            
        Returns:
            List of retrieved documents
        """
        # Synchronous version of retrieve
        import asyncio
        return asyncio.run(self.retrieve(query, top_k))
