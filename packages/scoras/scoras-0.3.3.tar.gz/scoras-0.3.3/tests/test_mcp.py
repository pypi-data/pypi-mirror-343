import unittest
import asyncio
from unittest.mock import patch, MagicMock

from scoras.mcp import MCPServer, MCPClient, MCPMessage, MCPResponse, MCPSkill, create_mcp_server, create_mcp_client
from scoras.agents import Agent

class TestMCPMessage(unittest.TestCase):
    """Test the MCPMessage class."""
    
    def test_initialization(self):
        """Test initialization of MCPMessage."""
        message = MCPMessage(
            role="user",
            parts=[{"type": "text", "text": "Hello, world!"}]
        )
        self.assertEqual(message.role, "user")
        self.assertEqual(len(message.parts), 1)
        self.assertEqual(message.parts[0]["type"], "text")
        self.assertEqual(message.parts[0]["text"], "Hello, world!")
    
    def test_from_text(self):
        """Test creating a message from text."""
        message = MCPMessage.from_text("user", "Hello, world!")
        self.assertEqual(message.role, "user")
        self.assertEqual(len(message.parts), 1)
        self.assertEqual(message.parts[0]["type"], "text")
        self.assertEqual(message.parts[0]["text"], "Hello, world!")
    
    def test_to_dict(self):
        """Test converting to dictionary."""
        message = MCPMessage(
            role="user",
            parts=[{"type": "text", "text": "Hello, world!"}]
        )
        result = message.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["role"], "user")
        self.assertEqual(len(result["parts"]), 1)
        self.assertEqual(result["parts"][0]["type"], "text")
        self.assertEqual(result["parts"][0]["text"], "Hello, world!")

class TestMCPResponse(unittest.TestCase):
    """Test the MCPResponse class."""
    
    def test_initialization(self):
        """Test initialization of MCPResponse."""
        response = MCPResponse(
            jsonrpc="2.0",
            result={"message": "Success"},
            id="request1"
        )
        self.assertEqual(response.jsonrpc, "2.0")
        self.assertEqual(response.result, {"message": "Success"})
        self.assertEqual(response.id, "request1")
        self.assertIsNone(response.error)
    
    def test_error_response(self):
        """Test creating an error response."""
        response = MCPResponse.error(
            id="request1",
            code=-32600,
            message="Invalid Request"
        )
        self.assertEqual(response.jsonrpc, "2.0")
        self.assertIsNone(response.result)
        self.assertEqual(response.id, "request1")
        self.assertEqual(response.error["code"], -32600)
        self.assertEqual(response.error["message"], "Invalid Request")
    
    def test_to_dict(self):
        """Test converting to dictionary."""
        # Success response
        response = MCPResponse(
            jsonrpc="2.0",
            result={"message": "Success"},
            id="request1"
        )
        result = response.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["jsonrpc"], "2.0")
        self.assertEqual(result["result"], {"message": "Success"})
        self.assertEqual(result["id"], "request1")
        self.assertNotIn("error", result)
        
        # Error response
        response = MCPResponse.error(
            id="request1",
            code=-32600,
            message="Invalid Request"
        )
        result = response.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["jsonrpc"], "2.0")
        self.assertNotIn("result", result)
        self.assertEqual(result["id"], "request1")
        self.assertEqual(result["error"]["code"], -32600)
        self.assertEqual(result["error"]["message"], "Invalid Request")

class TestMCPSkill(unittest.TestCase):
    """Test the MCPSkill class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a simple skill
        self.skill = MCPSkill(
            name="math",
            description="Performs mathematical operations",
            function=lambda params: eval(params["expression"])
        )
    
    def test_initialization(self):
        """Test initialization of MCPSkill."""
        self.assertEqual(self.skill.name, "math")
        self.assertEqual(self.skill.description, "Performs mathematical operations")
        self.assertTrue(callable(self.skill.function))
        self.assertTrue(self.skill._enable_scoring)
    
    async def test_execute(self):
        """Test executing the skill."""
        # Execute the skill
        result = await self.skill.execute({"expression": "5 + 3"})
        
        # Check the result
        self.assertEqual(result, 8)
    
    async def test_execute_with_error(self):
        """Test executing the skill with an error."""
        # Execute the skill with invalid parameters
        with self.assertRaises(Exception):
            await self.skill.execute({"invalid": "params"})
    
    def test_get_complexity_score(self):
        """Test getting the complexity score."""
        # Execute the skill to generate complexity
        asyncio.run(self.skill.execute({"expression": "5 + 3"}))
        
        # Get the score
        score = self.skill.get_complexity_score()
        
        # Check the result
        self.assertIsInstance(score, dict)
        self.assertIn("total_score", score)
        self.assertIn("complexity_rating", score)
        self.assertGreater(score["total_score"], 0)

class TestMCPServer(unittest.TestCase):
    """Test the MCPServer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create an agent
        self.agent = Agent(model="openai:gpt-4o")
        
        # Create some skills
        self.math_skill = MCPSkill(
            name="math",
            description="Performs mathematical operations",
            function=lambda params: eval(params["expression"])
        )
        
        # Create a server
        self.server = MCPServer(
            name="Test Server",
            description="A test MCP server",
            agent=self.agent,
            skills=[self.math_skill]
        )
    
    def test_initialization(self):
        """Test initialization of MCPServer."""
        self.assertEqual(self.server.name, "Test Server")
        self.assertEqual(self.server.description, "A test MCP server")
        self.assertEqual(self.server.agent, self.agent)
        self.assertEqual(len(self.server.skills), 1)
        self.assertEqual(self.server.skills[0], self.math_skill)
        self.assertTrue(self.server._enable_scoring)
    
    @patch('scoras.agents.Agent.run')
    async def test_handle_request_task_send(self, mock_run):
        """Test handling a task/send request."""
        # Set up the mock
        mock_run.return_value = "The result is 8."
        
        # Create a request
        request = {
            "jsonrpc": "2.0",
            "method": "tasks/send",
            "params": {
                "task": {
                    "id": "task1",
                    "messages": [
                        {"role": "user", "parts": [{"type": "text", "text": "Calculate 5+3"}]}
                    ]
                }
            },
            "id": "request1"
        }
        
        # Handle the request
        response = await self.server.handle_request(request)
        
        # Check the response
        self.assertIsInstance(response, dict)
        self.assertEqual(response["jsonrpc"], "2.0")
        self.assertEqual(response["id"], "request1")
        self.assertIn("result", response)
        self.assertIn("task", response["result"])
        self.assertEqual(response["result"]["task"]["id"], "task1")
        self.assertIn("messages", response["result"]["task"])
    
    @patch('scoras.mcp.MCPSkill.execute')
    async def test_handle_request_skills_invoke(self, mock_execute):
        """Test handling a skills/invoke request."""
        # Set up the mock
        mock_execute.return_value = 8
        
        # Create a request
        request = {
            "jsonrpc": "2.0",
            "method": "skills/invoke",
            "params": {
                "skill": "math",
                "params": {"expression": "5 + 3"}
            },
            "id": "request1"
        }
        
        # Handle the request
        response = await self.server.handle_request(request)
        
        # Check the response
        self.assertIsInstance(response, dict)
        self.assertEqual(response["jsonrpc"], "2.0")
        self.assertEqual(response["id"], "request1")
        self.assertIn("result", response)
        self.assertEqual(response["result"], 8)
    
    async def test_handle_request_invalid_method(self):
        """Test handling a request with an invalid method."""
        # Create a request
        request = {
            "jsonrpc": "2.0",
            "method": "invalid_method",
            "params": {},
            "id": "request1"
        }
        
        # Handle the request
        response = await self.server.handle_request(request)
        
        # Check the response
        self.assertIsInstance(response, dict)
        self.assertEqual(response["jsonrpc"], "2.0")
        self.assertEqual(response["id"], "request1")
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32601)
        self.assertEqual(response["error"]["message"], "Method not found")
    
    def test_get_complexity_score(self):
        """Test getting the complexity score."""
        # Get the score
        score = self.server.get_complexity_score()
        
        # Check the result
        self.assertIsInstance(score, dict)
        self.assertIn("total_score", score)
        self.assertIn("complexity_rating", score)
        self.assertGreater(score["total_score"], 0)
        
        # Compare with agent score
        agent_score = self.agent.get_complexity_score()
        
        # Server should have higher complexity than agent
        self.assertGreater(score["total_score"], agent_score["total_score"])

class TestMCPClient(unittest.TestCase):
    """Test the MCPClient class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a client
        self.client = MCPClient(
            server_url="http://example.com/mcp"
        )
    
    def test_initialization(self):
        """Test initialization of MCPClient."""
        self.assertEqual(self.client.server_url, "http://example.com/mcp")
        self.assertTrue(self.client._enable_scoring)
    
    @patch('httpx.AsyncClient.post')
    async def test_send_request(self, mock_post):
        """Test sending a request."""
        # Set up the mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "jsonrpc": "2.0",
            "result": {"message": "Success"},
            "id": "request1"
        }
        mock_post.return_value = mock_response
        
        # Send a request
        response = await self.client.send_request(
            method="test_method",
            params={"param1": "value1"}
        )
        
        # Check the response
        self.assertIsInstance(response, dict)
        self.assertEqual(response["jsonrpc"], "2.0")
        self.assertEqual(response["result"], {"message": "Success"})
        self.assertEqual(response["id"], "request1")
    
    @patch('httpx.AsyncClient.post')
    async def test_send_task(self, mock_post):
        """Test sending a task."""
        # Set up the mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "jsonrpc": "2.0",
            "result": {
                "task": {
                    "id": "task1",
                    "messages": [
                        {"role": "assistant", "parts": [{"type": "text", "text": "The result is 8."}]}
                    ]
                }
            },
            "id": "request1"
        }
        mock_post.return_value = mock_response
        
        # Send a task
        response = await self.client.send_task(
            task_id="task1",
            messages=[MCPMessage.from_text("user", "Calculate 5+3")]
        )
        
        # Check the response
        self.assertIsInstance(response, dict)
        self.assertEqual(response["jsonrpc"], "2.0")
        self.assertIn("result", response)
        self.assertIn("task", response["result"])
        self.assertEqual(response["result"]["task"]["id"], "task1")
        self.assertIn("messages", response["result"]["task"])
    
    @patch('httpx.AsyncClient.post')
    async def test_invoke_skill(self, mock_post):
        """Test invoking a skill."""
        # Set up the mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "jsonrpc": "2.0",
            "result": 8,
            "id": "request1"
        }
        mock_post.return_value = mock_response
        
        # Invoke a skill
        response = await self.client.invoke_skill(
            skill_name="math",
            params={"expression": "5 + 3"}
        )
        
        # Check the response
        self.assertIsInstance(response, dict)
        self.assertEqual(response["jsonrpc"], "2.0")
        self.assertEqual(response["result"], 8)
        self.assertEqual(response["id"], "request1")
    
    def test_get_complexity_score(self):
        """Test getting the complexity score."""
        # Get the score
        score = self.client.get_complexity_score()
        
        # Check the result
        self.assertIsInstance(score, dict)
        self.assertIn("total_score", score)
        self.assertIn("complexity_rating", score)
        self.assertGreater(score["total_score"], 0)

class TestCreateMCPServer(unittest.TestCase):
    """Test the create_mcp_server function."""
    
    def test_create_server(self):
        """Test creating an MCP server."""
        # Create an agent
        agent = Agent(model="openai:gpt-4o")
        
        # Create a skill
        math_skill = MCPSkill(
            name="math",
            description="Performs mathematical operations",
            function=lambda params: eval(params["expression"])
        )
        
        # Create a server
        server = create_mcp_server(
            name="Test Server",
            description="A test MCP server",
            agent=agent,
            skills=[math_skill]
        )
        
        # Check the server
        self.assertIsInstance(server, MCPServer)
        self.assertEqual(server.name, "Test Server")
        self.assertEqual(server.description, "A test MCP server")
        self.assertEqual(server.agent, agent)
        self.assertEqual(len(server.skills), 1)
        self.assertEqual(server.skills[0], math_skill)

class TestCreateMCPClient(unittest.TestCase):
    """Test the create_mcp_client function."""
    
    def test_create_client(self):
        """Test creating an MCP client."""
        # Create a client
        client = create_mcp_client(
            server_url="http://example.com/mcp"
        )
        
        # Check the client
        self.assertIsInstance(client, MCPClient)
        self.assertEqual(client.server_url, "http://example.com/mcp")

if __name__ == "__main__":
    unittest.main()
