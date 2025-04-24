"""
RAG (Retrieval Augmented Generation) module for the Scoras library.

This module contains implementations for creating and managing RAG systems,
with integrated scoring to measure workflow complexity.

Author: Anderson L. Amaral
"""

from typing import Any, Callable, Dict, List, Optional, Type, Union, TypeVar
import re
import asyncio
from pydantic import BaseModel, Field

from .core import Agent, RAG, ScoreTracker, ScorasConfig

class Document(BaseModel):
    """Class representing a document for retrieval."""
    
    content: str = Field(..., description="The content of the document")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata associated with the document")
    
    def __str__(self) -> str:
        """String representation of the document."""
        return self.content

class ChunkingStrategy(BaseModel):
    """Strategy for chunking documents."""
    
    chunk_size: int = Field(500, description="Size of each chunk in characters")
    chunk_overlap: int = Field(100, description="Overlap between chunks in characters")
    split_by: str = Field("paragraph", description="Method to split the document (paragraph, sentence, token)")
    
    def chunk_document(self, document: Document) -> List[Document]:
        """Chunk a document according to the strategy."""
        content = document.content
        chunks = []
        
        if self.split_by == "paragraph":
            # Split by paragraphs (double newlines)
            paragraphs = re.split(r'\n\s*\n', content)
            current_chunk = ""
            
            for paragraph in paragraphs:
                paragraph = paragraph.strip()
                if not paragraph:
                    continue
                
                # If adding this paragraph would exceed chunk size, save current chunk and start a new one
                if len(current_chunk) + len(paragraph) > self.chunk_size and current_chunk:
                    chunks.append(Document(
                        content=current_chunk,
                        metadata={**document.metadata, "chunk_index": len(chunks)}
                    ))
                    
                    # Start new chunk with overlap
                    words = current_chunk.split()
                    overlap_words = words[-min(len(words), self.chunk_overlap // 5):]  # Approximate words in overlap
                    current_chunk = " ".join(overlap_words) + "\n\n"
                
                current_chunk += paragraph + "\n\n"
            
            # Add the last chunk if it's not empty
            if current_chunk.strip():
                chunks.append(Document(
                    content=current_chunk,
                    metadata={**document.metadata, "chunk_index": len(chunks)}
                ))
                
        elif self.split_by == "sentence":
            # Split by sentences
            sentences = re.split(r'(?<=[.!?])\s+', content)
            current_chunk = ""
            
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue
                
                # If adding this sentence would exceed chunk size, save current chunk and start a new one
                if len(current_chunk) + len(sentence) > self.chunk_size and current_chunk:
                    chunks.append(Document(
                        content=current_chunk,
                        metadata={**document.metadata, "chunk_index": len(chunks)}
                    ))
                    
                    # Start new chunk with overlap
                    words = current_chunk.split()
                    overlap_words = words[-min(len(words), self.chunk_overlap // 5):]  # Approximate words in overlap
                    current_chunk = " ".join(overlap_words) + " "
                
                current_chunk += sentence + " "
            
            # Add the last chunk if it's not empty
            if current_chunk.strip():
                chunks.append(Document(
                    content=current_chunk,
                    metadata={**document.metadata, "chunk_index": len(chunks)}
                ))
                
        else:  # Default to token/word-based chunking
            # Split by words/tokens
            words = content.split()
            words_per_chunk = self.chunk_size // 5  # Approximate characters per word
            overlap_words = self.chunk_overlap // 5  # Approximate words in overlap
            
            for i in range(0, len(words), words_per_chunk - overlap_words):
                chunk_words = words[i:i + words_per_chunk]
                if chunk_words:
                    chunks.append(Document(
                        content=" ".join(chunk_words),
                        metadata={**document.metadata, "chunk_index": len(chunks)}
                    ))
        
        return chunks

class SimpleRetriever:
    """Simple keyword-based retriever."""
    
    def __init__(self, documents: List[Document], top_k: int = 3):
        self.documents = documents
        self.top_k = top_k
    
    def __call__(self, query: str) -> List[str]:
        """Retrieve documents based on keyword matching."""
        # Simple keyword matching
        query_terms = set(query.lower().split())
        scored_docs = []
        
        for doc in self.documents:
            content = doc.content.lower()
            score = sum(1 for term in query_terms if term in content)
            scored_docs.append((score, doc.content))
        
        # Sort by score in descending order
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        
        # Return top k documents
        return [doc for _, doc in scored_docs[:self.top_k]]

class VectorRetriever:
    """Vector-based retriever using embeddings."""
    
    def __init__(
        self, 
        documents: List[Document], 
        embedding_function: Callable[[str], List[float]],
        top_k: int = 3
    ):
        self.documents = documents
        self.embedding_function = embedding_function
        self.top_k = top_k
        self.document_embeddings = []
        
        # Precompute embeddings for all documents
        for doc in documents:
            self.document_embeddings.append(embedding_function(doc.content))
    
    def __call__(self, query: str) -> List[str]:
        """Retrieve documents based on embedding similarity."""
        # Get query embedding
        query_embedding = self.embedding_function(query)
        
        # Calculate similarity with all documents
        similarities = []
        for i, doc_embedding in enumerate(self.document_embeddings):
            similarity = self._cosine_similarity(query_embedding, doc_embedding)
            similarities.append((similarity, self.documents[i].content))
        
        # Sort by similarity in descending order
        similarities.sort(reverse=True, key=lambda x: x[0])
        
        # Return top k documents
        return [doc for _, doc in similarities[:self.top_k]]
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5
        
        if magnitude1 * magnitude2 == 0:
            return 0
            
        return dot_product / (magnitude1 * magnitude2)

class HybridRetriever:
    """Hybrid retriever that combines multiple retrieval methods."""
    
    def __init__(
        self,
        retrievers: List[Callable[[str], List[str]]],
        weights: Optional[List[float]] = None,
        top_k: int = 3
    ):
        self.retrievers = retrievers
        self.weights = weights or [1.0] * len(retrievers)
        self.top_k = top_k
        
        # Normalize weights
        total_weight = sum(self.weights)
        self.weights = [w / total_weight for w in self.weights]
    
    def __call__(self, query: str) -> List[str]:
        """Retrieve documents using multiple retrievers and combine results."""
        all_results = {}
        
        # Get results from each retriever
        for i, retriever in enumerate(self.retrievers):
            weight = self.weights[i]
            results = retriever(query)
            
            # Add to combined results with weight
            for j, result in enumerate(results):
                # Score based on position and weight
                score = weight * (1.0 / (j + 1))
                
                if result in all_results:
                    all_results[result] += score
                else:
                    all_results[result] = score
        
        # Sort by score
        sorted_results = sorted(all_results.items(), key=lambda x: x[1], reverse=True)
        
        # Return top k results
        return [result for result, _ in sorted_results[:self.top_k]]

class SemanticChunker:
    """Chunks documents based on semantic meaning rather than fixed sizes."""
    
    def __init__(
        self,
        embedding_function: Callable[[str], List[float]],
        min_chunk_size: int = 100,
        max_chunk_size: int = 1000,
        similarity_threshold: float = 0.7
    ):
        self.embedding_function = embedding_function
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        self.similarity_threshold = similarity_threshold
    
    def chunk_document(self, document: Document) -> List[Document]:
        """Chunk a document based on semantic similarity."""
        content = document.content
        
        # First split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', content)
        
        chunks = []
        current_chunk = []
        current_embedding = None
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # If this is the first sentence or current chunk is empty
            if not current_chunk:
                current_chunk.append(sentence)
                current_embedding = self.embedding_function(sentence)
                continue
            
            # Check if adding this sentence would exceed max chunk size
            current_chunk_text = " ".join(current_chunk)
            if len(current_chunk_text) + len(sentence) > self.max_chunk_size:
                # Save current chunk and start a new one
                chunks.append(Document(
                    content=current_chunk_text,
                    metadata={**document.metadata, "chunk_index": len(chunks)}
                ))
                current_chunk = [sentence]
                current_embedding = self.embedding_function(sentence)
                continue
            
            # Check semantic similarity
            sentence_embedding = self.embedding_function(sentence)
            similarity = self._cosine_similarity(current_embedding, sentence_embedding)
            
            if similarity >= self.similarity_threshold:
                # Add to current chunk
                current_chunk.append(sentence)
                # Update embedding as average
                current_embedding = [
                    (a + b) / 2 for a, b in zip(current_embedding, sentence_embedding)
                ]
            else:
                # Check if current chunk meets minimum size
                if len(current_chunk_text) >= self.min_chunk_size:
                    # Save current chunk and start a new one
                    chunks.append(Document(
                        content=current_chunk_text,
                        metadata={**document.metadata, "chunk_index": len(chunks)}
                    ))
                    current_chunk = [sentence]
                    current_embedding = sentence_embedding
                else:
                    # Add to current chunk despite low similarity
                    current_chunk.append(sentence)
                    # Update embedding as average
                    current_embedding = [
                        (a + b) / 2 for a, b in zip(current_embedding, sentence_embedding)
                    ]
        
        # Add the last chunk if it's not empty
        if current_chunk:
            current_chunk_text = " ".join(current_chunk)
            chunks.append(Document(
                content=current_chunk_text,
                metadata={**document.metadata, "chunk_index": len(chunks)}
            ))
        
        return chunks
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5
        
        if magnitude1 * magnitude2 == 0:
            return 0
            
        return dot_product / (magnitude1 * magnitude2)

class RAGSystem:
    """Complete RAG system with chunking, embedding, and retrieval."""
    
    def __init__(
        self,
        agent: Agent,
        documents: List[Document],
        chunking_strategy: Optional[ChunkingStrategy] = None,
        embedding_function: Optional[Callable[[str], List[float]]] = None,
        retriever: Optional[Callable[[str], List[str]]] = None,
        prompt_template: Optional[str] = None,
        enable_scoring: bool = True
    ):
        self.agent = agent
        self.original_documents = documents
        self.chunking_strategy = chunking_strategy or ChunkingStrategy()
        self.embedding_function = embedding_function
        self.prompt_template = prompt_template or (
            "Answer the following question based on the provided context:\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Answer:"
        )
        self.enable_scoring = enable_scoring
        self.score_tracker = ScoreTracker() if enable_scoring else None
        
        # Chunk documents
        self.chunked_documents = []
        for doc in documents:
            self.chunked_documents.extend(self.chunking_strategy.chunk_document(doc))
        
        # Set up retriever
        if retriever:
            self.retriever = retriever
        elif embedding_function:
            self.retriever = VectorRetriever(self.chunked_documents, embedding_function)
        else:
            self.retriever = SimpleRetriever(self.chunked_documents)
        
        # Create RAG instance
        self.rag = RAG(
            agent=agent,
            retriever=self.retriever,
            prompt_template=self.prompt_template,
            enable_scoring=enable_scoring
        )
        
        # Add score for RAG system
        if self.score_tracker:
            self.score_tracker.add_node("complex")
            # If agent has scoring enabled, incorporate its score
            if agent.enable_scoring and agent.score_tracker:
                for component, score in agent.score_tracker.components.items():
                    self.score_tracker.components[component] += score
                    self.score_tracker.total_score += score
                for component, count in agent.score_tracker.component_counts.items():
                    self.score_tracker.component_counts[component] += count
    
    async def run(self, query: str, **kwargs) -> Any:
        """Run the RAG system with the given query."""
        return await self.rag.run(query, **kwargs)
    
    def run_sync(self, query: str, **kwargs) -> Any:
        """Synchronous version of run."""
        import asyncio
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        return loop.run_until_complete(self.run(query, **kwargs))
    
    def get_complexity_score(self) -> Optional[Dict[str, Any]]:
        """Get the complexity score of the RAG system."""
        if not self.score_tracker:
            return None
        
        return self.score_tracker.get_report()
    
    def add_documents(self, documents: List[Document]) -> 'RAGSystem':
        """Add documents to the RAG system."""
        # Add to original documents
        self.original_documents.extend(documents)
        
        # Chunk new documents
        chunked_docs = []
        for doc in documents:
            chunked_docs.extend(self.chunking_strategy.chunk_document(doc))
        
        # Add to chunked documents
        self.chunked_documents.extend(chunked_docs)
        
        # Update retriever
        if isinstance(self.retriever, SimpleRetriever):
            self.retriever = SimpleRetriever(self.chunked_documents, self.retriever.top_k)
        elif isinstance(self.retriever, VectorRetriever):
            self.retriever = VectorRetriever(
                self.chunked_documents, 
                self.retriever.embedding_function,
                self.retriever.top_k
            )
        
        return self

class ContextualRAG(RAGSystem):
    """RAG system that adapts retrieval based on query context."""
    
    def __init__(
        self,
        agent: Agent,
        documents: List[Document],
        chunking_strategy: Optional[ChunkingStrategy] = None,
        embedding_function: Optional[Callable[[str], List[float]]] = None,
        prompt_template: Optional[str] = None,
        enable_scoring: bool = True
    ):
        super().__init__(
            agent=agent,
            documents=documents,
            chunking_strategy=chunking_strategy,
            embedding_function=embedding_function,
            prompt_template=prompt_template,
            enable_scoring=enable_scoring
        )
        
        # Create different retrievers for different types of queries
        if embedding_function:
            self.semantic_retriever = VectorRetriever(self.chunked_documents, embedding_function)
        else:
            self.semantic_retriever = SimpleRetriever(self.chunked_documents)
            
        self.keyword_retriever = SimpleRetriever(self.chunked_documents)
        
        # Create hybrid retriever
        self.hybrid_retriever = HybridRetriever(
            retrievers=[self.semantic_retriever, self.keyword_retriever],
            weights=[0.7, 0.3]
        )
    
    async def run(self, query: str, **kwargs) -> Any:
        """Run the contextual RAG system with the given query."""
        # Analyze query to determine best retrieval method
        query_lower = query.lower()
        
        # Choose retriever based on query characteristics
        if any(kw in query_lower for kw in ["who", "what", "when", "where", "why", "how"]):
            # Factual questions benefit from semantic retrieval
            retriever = self.semantic_retriever
        elif any(kw in query_lower for kw in ["find", "search", "locate", "identify"]):
            # Search queries benefit from keyword retrieval
            retriever = self.keyword_retriever
        else:
            # Default to hybrid approach
            retriever = self.hybrid_retriever
        
        # Retrieve documents
        documents = retriever(query)
        
        # Format the context
        context = "\n\n".join(documents)
        
        # Format the prompt
        prompt = self.prompt_template.format(context=context, question=query)
        
        # Run the agent
        return await self.agent.run(prompt, **kwargs)

# Function to create a RAG system
def create_rag_system(
    agent: Agent,
    documents: List[Document],
    chunking_strategy: Optional[ChunkingStrategy] = None,
    embedding_function: Optional[Callable[[str], List[float]]] = None,
    retriever: Optional[Callable[[str], List[str]]] = None,
    prompt_template: Optional[str] = None,
    contextual: bool = False,
    enable_scoring: bool = True
) -> RAGSystem:
    """
    Create a RAG system with the given components.
    
    Args:
        agent: Agent to use for generation
        documents: List of documents to use for retrieval
        chunking_strategy: Strategy for chunking documents
        embedding_function: Function to convert text to embeddings
        retriever: Custom retriever function
        prompt_template: Template for formatting prompts
        contextual: Whether to use contextual retrieval
        enable_scoring: Whether to enable complexity scoring
        
    Returns:
        A configured RAG system
    """
    if contextual:
        return ContextualRAG(
            agent=agent,
            documents=documents,
            chunking_strategy=chunking_strategy,
            embedding_function=embedding_function,
            prompt_template=prompt_template,
            enable_scoring=enable_scoring
        )
    else:
        return RAGSystem(
            agent=agent,
            documents=documents,
            chunking_strategy=chunking_strategy,
            embedding_function=embedding_function,
            retriever=retriever,
            prompt_template=prompt_template,
            enable_scoring=enable_scoring
        )
