import unittest
import asyncio
from unittest.mock import patch, MagicMock

from scoras.tools import Tool, ToolResult, ToolChain, ToolRouter, ToolBuilder
from scoras.agents import Agent

class TestTool(unittest.TestCase):
    """Test the Tool class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a simple tool
        self.tool = Tool(
            name="calculator",
            description="Performs basic arithmetic operations",
            parameters=["operation", "a", "b"],
            function=lambda operation, a, b: eval(f"{a} {operation} {b}")
        )
    
    def test_initialization(self):
        """Test initialization of Tool."""
        self.assertEqual(self.tool.name, "calculator")
        self.assertEqual(self.tool.description, "Performs basic arithmetic operations")
        self.assertEqual(self.tool.parameters, ["operation", "a", "b"])
        self.assertTrue(callable(self.tool.function))
        self.assertTrue(self.tool._enable_scoring)
    
    async def test_execute(self):
        """Test executing the tool."""
        # Execute the tool
        result = await self.tool.execute(operation="+", a=5, b=3)
        
        # Check the result
        self.assertIsInstance(result, ToolResult)
        self.assertEqual(result.value, 8)
        self.assertEqual(result.tool_name, "calculator")
        self.assertEqual(result.parameters, {"operation": "+", "a": 5, "b": 3})
        self.assertTrue(result.success)
        self.assertIsNone(result.error)
    
    async def test_execute_with_error(self):
        """Test executing the tool with an error."""
        # Create a tool that raises an exception
        error_tool = Tool(
            name="error_tool",
            description="Always raises an error",
            parameters=[],
            function=lambda: 1/0  # Will raise ZeroDivisionError
        )
        
        # Execute the tool
        result = await error_tool.execute()
        
        # Check the result
        self.assertIsInstance(result, ToolResult)
        self.assertIsNone(result.value)
        self.assertEqual(result.tool_name, "error_tool")
        self.assertEqual(result.parameters, {})
        self.assertFalse(result.success)
        self.assertIsInstance(result.error, ZeroDivisionError)
    
    def test_execute_sync(self):
        """Test executing the tool synchronously."""
        # Execute the tool
        result = self.tool.execute_sync(operation="*", a=4, b=7)
        
        # Check the result
        self.assertIsInstance(result, ToolResult)
        self.assertEqual(result.value, 28)
        self.assertEqual(result.tool_name, "calculator")
        self.assertEqual(result.parameters, {"operation": "*", "a": 4, "b": 7})
        self.assertTrue(result.success)
    
    def test_get_complexity_score(self):
        """Test getting the complexity score."""
        # Execute the tool to generate complexity
        self.tool.execute_sync(operation="+", a=5, b=3)
        
        # Get the score
        score = self.tool.get_complexity_score()
        
        # Check the result
        self.assertIsInstance(score, dict)
        self.assertIn("total_score", score)
        self.assertIn("complexity_rating", score)
        self.assertGreater(score["total_score"], 0)

class TestToolResult(unittest.TestCase):
    """Test the ToolResult class."""
    
    def test_initialization(self):
        """Test initialization of ToolResult."""
        # Successful result
        result = ToolResult(
            value=42,
            tool_name="test_tool",
            parameters={"param1": "value1"},
            success=True
        )
        self.assertEqual(result.value, 42)
        self.assertEqual(result.tool_name, "test_tool")
        self.assertEqual(result.parameters, {"param1": "value1"})
        self.assertTrue(result.success)
        self.assertIsNone(result.error)
        
        # Failed result
        error = ValueError("Test error")
        result = ToolResult(
            value=None,
            tool_name="test_tool",
            parameters={"param1": "value1"},
            success=False,
            error=error
        )
        self.assertIsNone(result.value)
        self.assertEqual(result.tool_name, "test_tool")
        self.assertEqual(result.parameters, {"param1": "value1"})
        self.assertFalse(result.success)
        self.assertEqual(result.error, error)
    
    def test_str_representation(self):
        """Test string representation of ToolResult."""
        # Successful result
        result = ToolResult(
            value=42,
            tool_name="test_tool",
            parameters={"param1": "value1"},
            success=True
        )
        self.assertIn("Success", str(result))
        self.assertIn("test_tool", str(result))
        self.assertIn("42", str(result))
        
        # Failed result
        error = ValueError("Test error")
        result = ToolResult(
            value=None,
            tool_name="test_tool",
            parameters={"param1": "value1"},
            success=False,
            error=error
        )
        self.assertIn("Failed", str(result))
        self.assertIn("test_tool", str(result))
        self.assertIn("ValueError", str(result))
        self.assertIn("Test error", str(result))

class TestToolChain(unittest.TestCase):
    """Test the ToolChain class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create some tools
        self.tool1 = Tool(
            name="add",
            description="Adds two numbers",
            parameters=["a", "b"],
            function=lambda a, b: a + b
        )
        
        self.tool2 = Tool(
            name="multiply",
            description="Multiplies two numbers",
            parameters=["a", "b"],
            function=lambda a, b: a * b
        )
        
        # Create a tool chain
        self.chain = ToolChain(
            name="math_chain",
            description="Performs a sequence of math operations",
            tools=[self.tool1, self.tool2]
        )
    
    def test_initialization(self):
        """Test initialization of ToolChain."""
        self.assertEqual(self.chain.name, "math_chain")
        self.assertEqual(self.chain.description, "Performs a sequence of math operations")
        self.assertEqual(len(self.chain.tools), 2)
        self.assertEqual(self.chain.tools[0], self.tool1)
        self.assertEqual(self.chain.tools[1], self.tool2)
        self.assertTrue(self.chain._enable_scoring)
    
    async def test_execute(self):
        """Test executing the tool chain."""
        # Execute the chain
        results = await self.chain.execute(
            add={"a": 5, "b": 3},
            multiply={"a": 8, "b": 2}
        )
        
        # Check the results
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 2)
        self.assertIn("add", results)
        self.assertIn("multiply", results)
        
        # Check individual results
        self.assertEqual(results["add"].value, 8)
        self.assertEqual(results["multiply"].value, 16)
    
    async def test_execute_sequential(self):
        """Test executing the tool chain sequentially with result passing."""
        # Execute the chain sequentially
        results = await self.chain.execute_sequential(
            initial_input={"a": 5, "b": 3},
            result_mapping={
                "add": lambda result: {"a": result.value, "b": 2}
            }
        )
        
        # Check the results
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 2)
        self.assertIn("add", results)
        self.assertIn("multiply", results)
        
        # Check individual results
        self.assertEqual(results["add"].value, 8)
        self.assertEqual(results["multiply"].value, 16)  # 8 * 2
    
    def test_execute_sync(self):
        """Test executing the tool chain synchronously."""
        # Execute the chain
        results = self.chain.execute_sync(
            add={"a": 5, "b": 3},
            multiply={"a": 8, "b": 2}
        )
        
        # Check the results
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 2)
        self.assertIn("add", results)
        self.assertIn("multiply", results)
        
        # Check individual results
        self.assertEqual(results["add"].value, 8)
        self.assertEqual(results["multiply"].value, 16)
    
    def test_get_complexity_score(self):
        """Test getting the complexity score."""
        # Execute the chain to generate complexity
        self.chain.execute_sync(
            add={"a": 5, "b": 3},
            multiply={"a": 8, "b": 2}
        )
        
        # Get the score
        score = self.chain.get_complexity_score()
        
        # Check the result
        self.assertIsInstance(score, dict)
        self.assertIn("total_score", score)
        self.assertIn("complexity_rating", score)
        self.assertGreater(score["total_score"], 0)
        
        # Compare with individual tools
        tool1_score = self.tool1.get_complexity_score()
        tool2_score = self.tool2.get_complexity_score()
        
        # Chain should have higher complexity than individual tools
        self.assertGreater(score["total_score"], tool1_score["total_score"])
        self.assertGreater(score["total_score"], tool2_score["total_score"])

class TestToolRouter(unittest.TestCase):
    """Test the ToolRouter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create some tools
        self.calculator = Tool(
            name="calculator",
            description="Performs basic arithmetic operations",
            parameters=["operation", "a", "b"],
            function=lambda operation, a, b: eval(f"{a} {operation} {b}")
        )
        
        self.translator = Tool(
            name="translator",
            description="Translates text to another language",
            parameters=["text", "target_language"],
            function=lambda text, target_language: f"Translated to {target_language}: {text}"
        )
        
        # Create a tool router
        self.router = ToolRouter(
            name="tool_router",
            description="Routes requests to appropriate tools",
            tools={
                "calculator": self.calculator,
                "translator": self.translator
            },
            routing_function=lambda query: "calculator" if any(op in query for op in ["+", "-", "*", "/"]) else "translator"
        )
    
    def test_initialization(self):
        """Test initialization of ToolRouter."""
        self.assertEqual(self.router.name, "tool_router")
        self.assertEqual(self.router.description, "Routes requests to appropriate tools")
        self.assertEqual(len(self.router.tools), 2)
        self.assertEqual(self.router.tools["calculator"], self.calculator)
        self.assertEqual(self.router.tools["translator"], self.translator)
        self.assertTrue(callable(self.router.routing_function))
        self.assertTrue(self.router._enable_scoring)
    
    async def test_route(self):
        """Test routing to the appropriate tool."""
        # Route a calculator query
        tool_name = await self.router.route("What is 5 + 3?")
        self.assertEqual(tool_name, "calculator")
        
        # Route a translator query
        tool_name = await self.router.route("Translate 'hello' to Spanish")
        self.assertEqual(tool_name, "translator")
    
    async def test_execute(self):
        """Test executing the router."""
        # Execute with a calculator query
        result = await self.router.execute(
            query="What is 5 + 3?",
            parameters={
                "calculator": {"operation": "+", "a": 5, "b": 3},
                "translator": {"text": "hello", "target_language": "Spanish"}
            }
        )
        
        # Check the result
        self.assertIsInstance(result, ToolResult)
        self.assertEqual(result.value, 8)
        self.assertEqual(result.tool_name, "calculator")
        
        # Execute with a translator query
        result = await self.router.execute(
            query="Translate 'hello' to Spanish",
            parameters={
                "calculator": {"operation": "+", "a": 5, "b": 3},
                "translator": {"text": "hello", "target_language": "Spanish"}
            }
        )
        
        # Check the result
        self.assertIsInstance(result, ToolResult)
        self.assertEqual(result.value, "Translated to Spanish: hello")
        self.assertEqual(result.tool_name, "translator")
    
    def test_execute_sync(self):
        """Test executing the router synchronously."""
        # Execute with a calculator query
        result = self.router.execute_sync(
            query="What is 5 + 3?",
            parameters={
                "calculator": {"operation": "+", "a": 5, "b": 3},
                "translator": {"text": "hello", "target_language": "Spanish"}
            }
        )
        
        # Check the result
        self.assertIsInstance(result, ToolResult)
        self.assertEqual(result.value, 8)
        self.assertEqual(result.tool_name, "calculator")
    
    def test_get_complexity_score(self):
        """Test getting the complexity score."""
        # Execute the router to generate complexity
        self.router.execute_sync(
            query="What is 5 + 3?",
            parameters={
                "calculator": {"operation": "+", "a": 5, "b": 3},
                "translator": {"text": "hello", "target_language": "Spanish"}
            }
        )
        
        # Get the score
        score = self.router.get_complexity_score()
        
        # Check the result
        self.assertIsInstance(score, dict)
        self.assertIn("total_score", score)
        self.assertIn("complexity_rating", score)
        self.assertGreater(score["total_score"], 0)
        
        # Compare with individual tools
        calculator_score = self.calculator.get_complexity_score()
        translator_score = self.translator.get_complexity_score()
        
        # Router should have higher complexity than individual tools
        self.assertGreater(score["total_score"], calculator_score["total_score"])
        self.assertGreater(score["total_score"], translator_score["total_score"])

class TestToolBuilder(unittest.TestCase):
    """Test the ToolBuilder class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a tool builder
        self.builder = ToolBuilder()
    
    def test_create_tool(self):
        """Test creating a tool."""
        # Create a simple tool
        tool = self.builder.create_tool(
            name="calculator",
            description="Performs basic arithmetic operations",
            parameters=["operation", "a", "b"],
            function=lambda operation, a, b: eval(f"{a} {operation} {b}")
        )
        
        # Check the tool
        self.assertIsInstance(tool, Tool)
        self.assertEqual(tool.name, "calculator")
        self.assertEqual(tool.description, "Performs basic arithmetic operations")
        self.assertEqual(tool.parameters, ["operation", "a", "b"])
        self.assertTrue(callable(tool.function))
    
    def test_create_chain(self):
        """Test creating a tool chain."""
        # Create some tools
        tool1 = self.builder.create_tool(
            name="add",
            description="Adds two numbers",
            parameters=["a", "b"],
            function=lambda a, b: a + b
        )
        
        tool2 = self.builder.create_tool(
            name="multiply",
            description="Multiplies two numbers",
            parameters=["a", "b"],
            function=lambda a, b: a * b
        )
        
        # Create a chain
        chain = self.builder.create_chain(
            name="math_chain",
            description="Performs a sequence of ma
(Content truncated due to size limit. Use line ranges to read in chunks)