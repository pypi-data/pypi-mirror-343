"""
Scoras: Intelligent Agent Framework with Complexity Scoring

This module provides RAG (Retrieval-Augmented Generation) functionality for the Scoras framework.
"""

from typing import Any, Dict, List, Optional, Union, Callable, TypeVar
import asyncio
from pydantic import BaseModel, Field
import math

from .core import ScoringMixin, RAG, Agent

class Document(BaseModel):
    """Model representing a document for retrieval."""
    
    content: str = Field(..., description="Content of the document")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata associated with the document")
    embedding: Optional[List[float]] = Field(None, description="Vector embedding of the document")
    
    def __str__(self) -> str:
        """String representation of the document."""
        return self.content[:100] + "..." if len(self.content) > 100 else self.content

class Retriever(ScoringMixin):
    """
    Base class for document retrievers.
    
    Retrievers are responsible for finding relevant documents based on a query.
    """
    
    def __init__(
        self,
        documents: List[Document],
        enable_scoring: bool = True
    ):
        """
        Initialize a Retriever.
        
        Args:
            documents: List of documents to retrieve from
            enable_scoring: Whether to track complexity scoring
        """
        super().__init__(enable_scoring=enable_scoring)
        self.documents = documents
        
        # Add complexity score for the retriever
        self._add_node_score("retriever", inputs=1, outputs=len(documents))

    async def retrieve(self, query: str, top_k: int = 3) -> List[Document]:
        """
        Retrieve relevant documents based on a query.
        
        Args:
            query: Query string
            top_k: Number of documents to retrieve
            
        Returns:
            List of retrieved documents
        """
        raise NotImplementedError("Subclasses must implement retrieve method")
    
    def retrieve_sync(self, query: str, top_k: int = 3) -> List[Document]:
        """
        Retrieve relevant documents based on a query synchronously.
        
        Args:
            query: Query string
            top_k: Number of documents to retrieve
            
        Returns:
            List of retrieved documents
        """
        # Create an event loop if there isn't one
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Run the async method in the event loop
        return loop.run_until_complete(self.retrieve(query, top_k))

class SimpleRetriever(Retriever):
    """
    A simple retriever that uses keyword matching.
    
    This retriever finds documents that contain the query keywords.
    """
    
    async def retrieve(self, query: str, top_k: int = 3) -> List[Document]:
        """
        Retrieve relevant documents based on keyword matching.
        
        Args:
            query: Query string
            top_k: Number of documents to retrieve
            
        Returns:
            List of retrieved documents
        """
        # Simple keyword matching
        query_terms = query.lower().split()
        
        # Score each document based on term frequency
        scored_docs = []
        for doc in self.documents:
            content = doc.content.lower()
            score = sum(content.count(term) for term in query_terms)
            scored_docs.append((doc, score))
        
        # Sort by score and take top_k
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        # Add complexity score based on query complexity
        query_complexity = min(1.0, len(query_terms) / 10)
        self._add_edge_score(
            f"retrieve_{query[:20]}",
            path_distance=1.0,
            information_content=0.5 + query_complexity
        )
        
        return [doc for doc, _ in scored_docs[:top_k]]

class SimpleRAG(RAG):
    """
    A simple RAG system that combines document retrieval with language model generation.
    
    This RAG system uses a simple retriever and an agent to generate responses.
    """
    
    def __init__(
        self,
        agent: Agent,
        documents: List[Document],
        enable_scoring: bool = True
    ):
        """
        Initialize a SimpleRAG system.
        
        Args:
            agent: Agent for generation
            documents: List of documents to retrieve from
            enable_scoring: Whether to track complexity scoring
        """
        # Create a simple retriever
        retriever = SimpleRetriever(documents, enable_scoring=enable_scoring)
        
        # Initialize the base RAG system
        super().__init__(retriever, agent, enable_scoring=enable_scoring)
    
    async def run(self, query: str, top_k: int = 3) -> str:
        """
        Process a query using the SimpleRAG system.
        
        Args:
            query: Query string
            top_k: Number of documents to retrieve
            
        Returns:
            Generated response
        """
        # Retrieve relevant documents
        docs = await self.retriever.retrieve(query, top_k)
        
        # Format documents for the agent
        context = "\n\n".join([f"Document {i+1}: {doc.content}" for i, doc in enumerate(docs)])
        
        # Create the prompt with the retrieved context
        prompt = f"Context information:\n{context}\n\nQuestion: {query}\n\nAnswer:"
        
        # Generate a response using the agent
        response = await self.agent.run(prompt)
        
        return response

class ContextualRAG(RAG):
    """
    A RAG system that adapts to the query context.
    
    This RAG system analyzes the query to determine the best retrieval strategy.
    """
    
    def __init__(
        self,
        agent: Agent,
        documents: List[Document],
        embedding_function: Optional[Callable[[str], List[float]]] = None,
        enable_scoring: bool = True
    ):
        """
        Initialize a ContextualRAG system.
        
        Args:
            agent: Agent for generation
            documents: List of documents to retrieve from
            embedding_function: Optional function to convert text to embeddings
            enable_scoring: Whether to track complexity scoring
        """
        from .rag import ContextualRetriever
        
        # Create a contextual retriever
        retriever = ContextualRetriever(documents, embedding_function, enable_scoring=enable_scoring)
        
        # Initialize the base RAG system
        super().__init__(retriever, agent, enable_scoring=enable_scoring)
        
        # Add additional complexity for contextual RAG
        self._add_node_score("contextual_rag", inputs=2, outputs=1)
    
    async def run(self, query: str, top_k: int = 3) -> str:
        """
        Process a query using the ContextualRAG system.
        
        Args:
            query: Query string
            top_k: Number of documents to retrieve
            
        Returns:
            Generated response
        """
        # Retrieve relevant documents using the contextual retriever
        docs = await self.retriever.retrieve(query, top_k)
        
        # Format documents for the agent
        context = "\n\n".join([f"Document {i+1}: {doc.content}" for i, doc in enumerate(docs)])
        
        # Create the prompt with the retrieved context
        prompt = f"Context information:\n{context}\n\nQuestion: {query}\n\nAnswer:"
        
        # Generate a response using the agent
        response = await self.agent.run(prompt)
        
        return response
