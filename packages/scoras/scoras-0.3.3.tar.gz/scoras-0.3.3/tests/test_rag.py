import unittest
import asyncio
from unittest.mock import patch, MagicMock

from scoras.rag import Document, Retriever, SimpleRetriever, SemanticRetriever, HybridRetriever
from scoras.rag import ContextualRetriever, RAGSystem, SimpleRAG, ContextualRAG, create_rag_system
from scoras.agents import Agent

class TestDocument(unittest.TestCase):
    """Test the Document class."""
    
    def test_initialization(self):
        """Test initialization of Document."""
        doc = Document(content="This is a test document")
        self.assertEqual(doc.content, "This is a test document")
        self.assertEqual(doc.metadata, {})
        self.assertIsNone(doc.embedding)
        
        # Test with metadata and embedding
        doc = Document(
            content="This is a test document",
            metadata={"source": "test", "date": "2025-04-13"},
            embedding=[0.1, 0.2, 0.3]
        )
        self.assertEqual(doc.metadata["source"], "test")
        self.assertEqual(doc.metadata["date"], "2025-04-13")
        self.assertEqual(doc.embedding, [0.1, 0.2, 0.3])
    
    def test_str_representation(self):
        """Test string representation of Document."""
        # Short document
        doc = Document(content="This is a test document")
        self.assertEqual(str(doc), "This is a test document")
        
        # Long document
        long_content = "This is a very long document that exceeds 100 characters. " * 3
        doc = Document(content=long_content)
        self.assertEqual(str(doc), long_content[:100] + "...")

class TestRetriever(unittest.TestCase):
    """Test the Retriever base class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a concrete subclass for testing
        class TestRetrieverImpl(Retriever):
            async def retrieve(self, query, top_k=3):
                return self.documents[:top_k]
        
        self.documents = [
            Document(content="Document 1"),
            Document(content="Document 2"),
            Document(content="Document 3"),
            Document(content="Document 4"),
            Document(content="Document 5")
        ]
        
        self.retriever = TestRetrieverImpl(self.documents)
    
    def test_initialization(self):
        """Test initialization of Retriever."""
        self.assertEqual(self.retriever.documents, self.documents)
        self.assertTrue(self.retriever._enable_scoring)
    
    def test_retrieve_sync(self):
        """Test retrieving documents synchronously."""
        # Retrieve documents
        results = self.retriever.retrieve_sync("test query", top_k=2)
        
        # Check the results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].content, "Document 1")
        self.assertEqual(results[1].content, "Document 2")
    
    def test_get_complexity_score(self):
        """Test getting the complexity score."""
        # Get the score
        score = self.retriever.get_complexity_score()
        
        # Check the result
        self.assertIsInstance(score, dict)
        self.assertIn("total_score", score)
        self.assertIn("complexity_rating", score)
        self.assertGreater(score["total_score"], 0)

class TestSimpleRetriever(unittest.TestCase):
    """Test the SimpleRetriever class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.documents = [
            Document(content="Paris is the capital of France"),
            Document(content="Berlin is the capital of Germany"),
            Document(content="Rome is the capital of Italy"),
            Document(content="Madrid is the capital of Spain"),
            Document(content="London is the capital of the United Kingdom")
        ]
        
        self.retriever = SimpleRetriever(self.documents)
    
    async def test_retrieve(self):
        """Test retrieving documents."""
        # Retrieve documents
        results = await self.retriever.retrieve("capital of France", top_k=2)
        
        # Check the results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].content, "Paris is the capital of France")  # Most relevant
        
        # Different query
        results = await self.retriever.retrieve("capital of Germany", top_k=2)
        self.assertEqual(results[0].content, "Berlin is the capital of Germany")  # Most relevant
    
    def test_get_complexity_score(self):
        """Test getting the complexity score after retrieval."""
        # Retrieve documents
        asyncio.run(self.retriever.retrieve("capital of France", top_k=2))
        
        # Get the score
        score = self.retriever.get_complexity_score()
        
        # Check the result
        self.assertIsInstance(score, dict)
        self.assertIn("total_score", score)
        self.assertIn("complexity_rating", score)
        self.assertGreater(score["total_score"], 0)

class TestSemanticRetriever(unittest.TestCase):
    """Test the SemanticRetriever class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.documents = [
            Document(content="Paris is the capital of France", embedding=[0.9, 0.1, 0.1]),
            Document(content="Berlin is the capital of Germany", embedding=[0.1, 0.9, 0.1]),
            Document(content="Rome is the capital of Italy", embedding=[0.1, 0.1, 0.9]),
            Document(content="Madrid is the capital of Spain", embedding=[0.5, 0.5, 0.1]),
            Document(content="London is the capital of the United Kingdom", embedding=[0.4, 0.4, 0.4])
        ]
        
        # Mock embedding function
        def mock_embedding_fn(text):
            if "France" in text:
                return [0.9, 0.1, 0.1]
            elif "Germany" in text:
                return [0.1, 0.9, 0.1]
            elif "Italy" in text:
                return [0.1, 0.1, 0.9]
            else:
                return [0.3, 0.3, 0.3]
        
        self.retriever = SemanticRetriever(self.documents, mock_embedding_fn)
    
    async def test_retrieve(self):
        """Test retrieving documents."""
        # Retrieve documents
        results = await self.retriever.retrieve("Tell me about France", top_k=2)
        
        # Check the results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].content, "Paris is the capital of France")  # Most relevant
        
        # Different query
        results = await self.retriever.retrieve("Tell me about Germany", top_k=2)
        self.assertEqual(results[0].content, "Berlin is the capital of Germany")  # Most relevant
    
    def test_cosine_similarity(self):
        """Test cosine similarity calculation."""
        # Test with identical vectors
        sim = self.retriever._cosine_similarity([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
        self.assertAlmostEqual(sim, 1.0, places=5)
        
        # Test with orthogonal vectors
        sim = self.retriever._cosine_similarity([1, 0, 0], [0, 1, 0])
        self.assertAlmostEqual(sim, 0.0, places=5)
        
        # Test with different length vectors
        with self.assertRaises(ValueError):
            self.retriever._cosine_similarity([1, 0], [0, 1, 0])
    
    def test_get_complexity_score(self):
        """Test getting the complexity score after retrieval."""
        # Retrieve documents
        asyncio.run(self.retriever.retrieve("Tell me about France", top_k=2))
        
        # Get the score
        score = self.retriever.get_complexity_score()
        
        # Check the result
        self.assertIsInstance(score, dict)
        self.assertIn("total_score", score)
        self.assertIn("complexity_rating", score)
        self.assertGreater(score["total_score"], 0)
        
        # Compare with simple retriever
        simple_retriever = SimpleRetriever(self.documents)
        asyncio.run(simple_retriever.retrieve("Tell me about France", top_k=2))
        simple_score = simple_retriever.get_complexity_score()
        
        # Semantic retriever should have higher complexity
        self.assertGreater(score["total_score"], simple_score["total_score"])

class TestHybridRetriever(unittest.TestCase):
    """Test the HybridRetriever class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.documents = [
            Document(content="Paris is the capital of France", embedding=[0.9, 0.1, 0.1]),
            Document(content="Berlin is the capital of Germany", embedding=[0.1, 0.9, 0.1]),
            Document(content="Rome is the capital of Italy", embedding=[0.1, 0.1, 0.9]),
            Document(content="Madrid is the capital of Spain", embedding=[0.5, 0.5, 0.1]),
            Document(content="London is the capital of the United Kingdom", embedding=[0.4, 0.4, 0.4])
        ]
        
        # Mock embedding function
        def mock_embedding_fn(text):
            if "France" in text:
                return [0.9, 0.1, 0.1]
            elif "Germany" in text:
                return [0.1, 0.9, 0.1]
            elif "Italy" in text:
                return [0.1, 0.1, 0.9]
            else:
                return [0.3, 0.3, 0.3]
        
        self.retriever = HybridRetriever(
            self.documents,
            mock_embedding_fn,
            keyword_weight=0.4,
            semantic_weight=0.6
        )
    
    async def test_retrieve(self):
        """Test retrieving documents."""
        # Retrieve documents
        results = await self.retriever.retrieve("capital of France", top_k=2)
        
        # Check the results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].content, "Paris is the capital of France")  # Most relevant
        
        # Different query
        results = await self.retriever.retrieve("capital of Germany", top_k=2)
        self.assertEqual(results[0].content, "Berlin is the capital of Germany")  # Most relevant
    
    def test_get_complexity_score(self):
        """Test getting the complexity score after retrieval."""
        # Retrieve documents
        asyncio.run(self.retriever.retrieve("capital of France", top_k=2))
        
        # Get the score
        score = self.retriever.get_complexity_score()
        
        # Check the result
        self.assertIsInstance(score, dict)
        self.assertIn("total_score", score)
        self.assertIn("complexity_rating", score)
        self.assertGreater(score["total_score"], 0)
        
        # Compare with semantic retriever
        semantic_retriever = SemanticRetriever(self.documents, lambda x: [0.3, 0.3, 0.3])
        asyncio.run(semantic_retriever.retrieve("capital of France", top_k=2))
        semantic_score = semantic_retriever.get_complexity_score()
        
        # Hybrid retriever should have higher complexity
        self.assertGreater(score["total_score"], semantic_score["total_score"])

class TestContextualRetriever(unittest.TestCase):
    """Test the ContextualRetriever class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.documents = [
            Document(content="Paris is the capital of France", embedding=[0.9, 0.1, 0.1]),
            Document(content="Berlin is the capital of Germany", embedding=[0.1, 0.9, 0.1]),
            Document(content="Rome is the capital of Italy", embedding=[0.1, 0.1, 0.9]),
            Document(content="Madrid is the capital of Spain", embedding=[0.5, 0.5, 0.1]),
            Document(content="London is the capital of the United Kingdom", embedding=[0.4, 0.4, 0.4])
        ]
        
        # Mock embedding function
        def mock_embedding_fn(text):
            if "France" in text:
                return [0.9, 0.1, 0.1]
            elif "Germany" in text:
                return [0.1, 0.9, 0.1]
            elif "Italy" in text:
                return [0.1, 0.1, 0.9]
            else:
                return [0.3, 0.3, 0.3]
        
        self.retriever = ContextualRetriever(self.documents, mock_embedding_fn)
    
    async def test_retrieve(self):
        """Test retrieving documents."""
        # Short query (should use keyword retrieval)
        results = await self.retriever.retrieve("France", top_k=2)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].content, "Paris is the capital of France")
        
        # Medium query (should use semantic retrieval)
        results = await self.retriever.retrieve("Tell me about the capital of Germany", top_k=2)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].content, "Berlin is the capital of Germany")
        
        # Long query (should use hybrid retrieval)
        results = await self.retriever.retrieve("I'm planning a trip to Europe and want to know about the capital cities of France, Germany, and Italy", top_k=3)
        self.assertEqual(len(results), 3)
    
    def test_analyze_query(self):
        """Test query analysis."""
        # Short query
        strategy = self.retriever._analyze_query("France")
        self.assertEqual(strategy, "keyword")
        
        # Medium query
        strategy = self.retriever._analyze_query("Tell me about the capital of Germany")
        self.assertEqual(strategy, "semantic")
        
        # Long query
        strategy = self.retriever._analyze_query("I'm planning a trip to Europe and want to know about the capital cities of France, Germany, and Italy")
        self.assertEqual(strategy, "hybrid")
    
    def test_get_complexity_score(self):
        """Test getting the complexity score after retrieval."""
        # Retrieve documents with different query types
        asyncio.run(self.retriever.retrieve("France", top_k=2))  # keyword
        asyncio.run(self.retriever.retrieve("Tell me about the capital of Germany", top_k=2))  # semantic
        asyncio.run(self.retriever.retrieve("I'm planning a trip to Europe and want to know about the capital cities of France, Germany, and Italy", top_k=3))  # hybrid
        
        # Get the score
        score = self.retriever.get_complexity_score()
        
        # Check the result
        self.assertIsInstance(score, dict)
        self.assertIn("total_score", score)
        self.assertIn("complexity_rating", score)
        self.assertGreater(score["total_score"], 0)
        
        # Compare with hybrid retriever
        hybrid_retriever = HybridRetriever(self.documents, lambda x: [0.3, 0.3, 0.3])
        asyncio.run(hybrid_retriever.retrieve("capital of France", top_k=2))
        hybrid_score = hybrid_retriever.get_complexity_score()
        
        # Contextual retriever should have higher complexity
        self.assertGreater(score["total_score"], hybrid_score["total_score"])

class TestRAGSystem(unittest.TestCase):
    """Test the RAGSystem class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.documents = [
            Document(content="Paris is the capital of France"),
            Document(content="Berlin is the capital of Germany"),
            Document(content="Rome is the capital of Italy")
        ]
        
        self.retriever = SimpleRetriever(self.documents)
        self.agent = Agent(model="openai:gpt-4o")
        self.rag_system = RAGSystem(self.retriever, self.agent)
    
    def test_initialization(self):
        """Test initialization of RAGSystem."""
        self.assertEqual(self.rag_system.retriever, self.retriever)
        self.assertEqual(self.rag_system.agent, self.agent)
        self.assertTrue(self.rag_system._enable_scoring)
    
    @patch('scoras.rag.Retriever.retrieve')
    @patch('scoras.agents.Agent.run')
    async def test_run(self, mock_agent_run, mock_retriever_retrieve):
        """Test running the RAG system."""
        # Set up the mocks
        mock_retriever_retrieve.return_value = [
            Document(content="Paris is the capital of France")
        ]
        mock_agent_run.return_value = "The capital of France is Paris."
        
        # Run the RAG system
        response = await self.rag_system.run
(Content truncated due to size limit. Use line ranges to read in chunks)