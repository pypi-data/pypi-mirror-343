import unittest
import asyncio
from unittest.mock import patch, MagicMock

from scoras.a2a import A2AMessage, A2AConversation, A2AAgent, A2ANetwork, A2AHub
from scoras.a2a import create_a2a_agent, create_a2a_network
from scoras.agents import Agent, Message

class TestA2AMessage(unittest.TestCase):
    """Test the A2AMessage class."""
    
    def test_initialization(self):
        """Test initialization of A2AMessage."""
        message = A2AMessage(
            sender="agent1",
            receiver="agent2",
            content="Hello, agent2!"
        )
        self.assertEqual(message.sender, "agent1")
        self.assertEqual(message.receiver, "agent2")
        self.assertEqual(message.content, "Hello, agent2!")
        self.assertEqual(message.metadata, {})
        self.assertIsNotNone(message.id)
        self.assertIsNone(message.timestamp)
    
    def test_to_dict(self):
        """Test converting to dictionary."""
        message = A2AMessage(
            id="msg123",
            sender="agent1",
            receiver="agent2",
            content="Hello, agent2!",
            metadata={"priority": "high"},
            timestamp="2025-04-13T22:00:00Z"
        )
        result = message.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], "msg123")
        self.assertEqual(result["sender"], "agent1")
        self.assertEqual(result["receiver"], "agent2")
        self.assertEqual(result["content"], "Hello, agent2!")
        self.assertEqual(result["metadata"]["priority"], "high")
        self.assertEqual(result["timestamp"], "2025-04-13T22:00:00Z")

class TestA2AConversation(unittest.TestCase):
    """Test the A2AConversation class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.message1 = A2AMessage(
            id="msg1",
            sender="agent1",
            receiver="agent2",
            content="Hello, agent2!"
        )
        self.message2 = A2AMessage(
            id="msg2",
            sender="agent2",
            receiver="agent1",
            content="Hello, agent1!"
        )
        self.conversation = A2AConversation(
            id="conv123",
            participants=["agent1", "agent2"],
            messages=[self.message1, self.message2],
            metadata={"topic": "greetings"}
        )
    
    def test_initialization(self):
        """Test initialization of A2AConversation."""
        self.assertEqual(self.conversation.id, "conv123")
        self.assertEqual(self.conversation.participants, ["agent1", "agent2"])
        self.assertEqual(len(self.conversation.messages), 2)
        self.assertEqual(self.conversation.messages[0], self.message1)
        self.assertEqual(self.conversation.messages[1], self.message2)
        self.assertEqual(self.conversation.metadata["topic"], "greetings")
    
    def test_to_dict(self):
        """Test converting to dictionary."""
        result = self.conversation.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], "conv123")
        self.assertEqual(result["participants"], ["agent1", "agent2"])
        self.assertEqual(len(result["messages"]), 2)
        self.assertEqual(result["messages"][0]["id"], "msg1")
        self.assertEqual(result["messages"][1]["id"], "msg2")
        self.assertEqual(result["metadata"]["topic"], "greetings")

class TestA2AAgent(unittest.TestCase):
    """Test the A2AAgent class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create an agent
        self.base_agent = Agent(model="openai:gpt-4o")
        
        # Create an A2A agent
        self.a2a_agent = A2AAgent(
            agent_id="agent1",
            agent=self.base_agent
        )
    
    def test_initialization(self):
        """Test initialization of A2AAgent."""
        self.assertEqual(self.a2a_agent.agent_id, "agent1")
        self.assertEqual(self.a2a_agent.agent, self.base_agent)
        self.assertEqual(self.a2a_agent.conversations, {})
        self.assertTrue(self.a2a_agent._enable_scoring)
    
    @patch('scoras.agents.Agent.run')
    async def test_send_receive_message(self, mock_run):
        """Test sending and receiving messages."""
        # Set up the mock
        mock_run.return_value = "Hello back!"
        
        # Send a message
        sent_message = await self.a2a_agent.send_message(
            receiver_id="agent2",
            content="Hello, agent2!"
        )
        
        # Check the sent message
        self.assertIsInstance(sent_message, A2AMessage)
        self.assertEqual(sent_message.sender, "agent1")
        self.assertEqual(sent_message.receiver, "agent2")
        self.assertEqual(sent_message.content, "Hello, agent2!")
        
        # Check that the conversation was created
        self.assertEqual(len(self.a2a_agent.conversations), 1)
        conversation_id = list(self.a2a_agent.conversations.keys())[0]
        conversation = self.a2a_agent.conversations[conversation_id]
        self.assertIsInstance(conversation, A2AConversation)
        self.assertEqual(len(conversation.messages), 1)
        self.assertEqual(conversation.messages[0], sent_message)
        
        # Receive a message
        received_message = A2AMessage(
            sender="agent2",
            receiver="agent1",
            content="Hello, agent1!"
        )
        response = await self.a2a_agent.receive_message(received_message)
        
        # Check the response
        self.assertIsInstance(response, A2AMessage)
        self.assertEqual(response.sender, "agent1")
        self.assertEqual(response.receiver, "agent2")
        self.assertEqual(response.content, "Hello back!")
    
    def test_send_message_sync(self):
        """Test sending a message synchronously."""
        with patch('scoras.a2a.A2AAgent.send_message', return_value=asyncio.Future()) as mock_send:
            # Create a message
            message = A2AMessage(
                sender="agent1",
                receiver="agent2",
                content="Hello, agent2!"
            )
            
            # Set the result of the future
            mock_send.return_value.set_result(message)
            
            # Send the message synchronously
            result = self.a2a_agent.send_message_sync(
                receiver_id="agent2",
                content="Hello, agent2!"
            )
            
            # Check the result
            self.assertEqual(result, message)
    
    def test_get_complexity_score(self):
        """Test getting the complexity score."""
        # Send a message to generate complexity
        self.a2a_agent.send_message_sync(
            receiver_id="agent2",
            content="Hello, agent2!"
        )
        
        # Get the score
        score = self.a2a_agent.get_complexity_score()
        
        # Check the result
        self.assertIsInstance(score, dict)
        self.assertIn("total_score", score)
        self.assertIn("complexity_rating", score)
        self.assertGreater(score["total_score"], 0)
        
        # Compare with base agent
        base_score = self.base_agent.get_complexity_score()
        
        # A2A agent should have higher complexity
        self.assertGreater(score["total_score"], base_score["total_score"])

class TestA2ANetwork(unittest.TestCase):
    """Test the A2ANetwork class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create base agents
        self.base_agent1 = Agent(model="openai:gpt-4o")
        self.base_agent2 = Agent(model="anthropic:claude-3-opus")
        
        # Create A2A agents
        self.a2a_agent1 = A2AAgent(
            agent_id="agent1",
            agent=self.base_agent1
        )
        self.a2a_agent2 = A2AAgent(
            agent_id="agent2",
            agent=self.base_agent2
        )
        
        # Create an A2A network
        self.network = A2ANetwork(
            name="test_network",
            agents={
                "agent1": self.a2a_agent1,
                "agent2": self.a2a_agent2
            }
        )
    
    def test_initialization(self):
        """Test initialization of A2ANetwork."""
        self.assertEqual(self.network.name, "test_network")
        self.assertEqual(len(self.network.agents), 2)
        self.assertEqual(self.network.agents["agent1"], self.a2a_agent1)
        self.assertEqual(self.network.agents["agent2"], self.a2a_agent2)
        self.assertEqual(self.network.conversations, {})
        self.assertTrue(self.network._enable_scoring)
    
    @patch('scoras.a2a.A2AAgent.send_message')
    async def test_send_message(self, mock_send):
        """Test sending a message through the network."""
        # Set up the mock
        message = A2AMessage(
            sender="agent1",
            receiver="agent2",
            content="Hello, agent2!"
        )
        mock_send.return_value = message
        
        # Send a message
        result = await self.network.send_message(
            sender_id="agent1",
            receiver_id="agent2",
            content="Hello, agent2!"
        )
        
        # Check the result
        self.assertEqual(result, message)
        mock_send.assert_called_once()
    
    @patch('scoras.a2a.A2AAgent.receive_message')
    async def test_deliver_message(self, mock_receive):
        """Test delivering a message through the network."""
        # Set up the mock
        message = A2AMessage(
            sender="agent1",
            receiver="agent2",
            content="Hello, agent2!"
        )
        response = A2AMessage(
            sender="agent2",
            receiver="agent1",
            content="Hello, agent1!"
        )
        mock_receive.return_value = response
        
        # Deliver a message
        result = await self.network.deliver_message(message)
        
        # Check the result
        self.assertEqual(result, response)
        mock_receive.assert_called_once_with(message)
    
    @patch('scoras.a2a.A2ANetwork.send_message')
    @patch('scoras.a2a.A2ANetwork.deliver_message')
    async def test_simulate_conversation(self, mock_deliver, mock_send):
        """Test simulating a conversation."""
        # Set up the mocks
        initial_message = A2AMessage(
            sender="agent1",
            receiver="agent2",
            content="Hello, agent2!"
        )
        response1 = A2AMessage(
            sender="agent2",
            receiver="agent1",
            content="Hello, agent1!"
        )
        response2 = A2AMessage(
            sender="agent1",
            receiver="agent2",
            content="How are you?"
        )
        response3 = A2AMessage(
            sender="agent2",
            receiver="agent1",
            content="I'm fine, thanks!"
        )
        
        mock_send.return_value = initial_message
        mock_deliver.side_effect = [response1, response2, response3]
        
        # Create a conversation
        conversation = A2AConversation(
            id="conv123",
            participants=["agent1", "agent2"],
            messages=[initial_message, response1, response2, response3]
        )
        self.network.conversations["conv123"] = conversation
        
        # Simulate a conversation
        result = await self.network.simulate_conversation(
            sender_id="agent1",
            receiver_id="agent2",
            initial_message="Hello, agent2!",
            turns=3
        )
        
        # Check the result
        self.assertEqual(result, conversation)
        self.assertEqual(mock_send.call_count, 1)
        self.assertEqual(mock_deliver.call_count, 3)
    
    def test_get_complexity_score(self):
        """Test getting the complexity score."""
        # Get the score
        score = self.network.get_complexity_score()
        
        # Check the result
        self.assertIsInstance(score, dict)
        self.assertIn("total_score", score)
        self.assertIn("complexity_rating", score)
        self.assertGreater(score["total_score"], 0)
        
        # Compare with individual agents
        agent1_score = self.a2a_agent1.get_complexity_score()
        agent2_score = self.a2a_agent2.get_complexity_score()
        
        # Network should have higher complexity than individual agents
        self.assertGreater(score["total_score"], agent1_score["total_score"])
        self.assertGreater(score["total_score"], agent2_score["total_score"])

class TestA2AHub(unittest.TestCase):
    """Test the A2AHub class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create base agents
        self.base_agent1 = Agent(model="openai:gpt-4o")
        self.base_agent2 = Agent(model="anthropic:claude-3-opus")
        
        # Create A2A agents
        self.a2a_agent1 = A2AAgent(
            agent_id="agent1",
            agent=self.base_agent1
        )
        self.a2a_agent2 = A2AAgent(
            agent_id="agent2",
            agent=self.base_agent2
        )
        
        # Create an A2A hub
        self.hub = A2AHub(name="test_hub")
    
    def test_initialization(self):
        """Test initialization of A2AHub."""
        self.assertEqual(self.hub.name, "test_hub")
        self.assertEqual(self.hub.agents, {})
        self.assertEqual(self.hub.conversations, {})
        self.assertEqual(self.hub.message_queue, [])
        self.assertTrue(self.hub._enable_scoring)
    
    async def test_register_agent(self):
        """Test registering an agent with the hub."""
        # Register an agent
        await self.hub.register_agent(self.a2a_agent1)
        
        # Check that the agent was registered
        self.assertEqual(len(self.hub.agents), 1)
        self.assertEqual(self.hub.agents["agent1"], self.a2a_agent1)
        
        # Register another agent
        await self.hub.register_agent(self.a2a_agent2)
        
        # Check that the agent was registered
        self.assertEqual(len(self.hub.agents), 2)
        self.assertEqual(self.hub.agents["agent2"], self.a2a_agent2)
    
    async def test_unregister_agent(self):
        """Test unregistering an agent from the hub."""
        # Register agents
        await self.hub.register_agent(self.a2a_agent1)
        await self.hub.register_agent(self.a2a_agent2)
        
        # Unregister an agent
        await self.hub.unregister_agent("agent1")
        
        # Check that the agent was unregistered
        self.assertEqual(len(self.hub.agents), 1)
        self.assertNotIn("agent1", self.hub.agents)
        self.assertIn("agent2", self.hub.agents)
    
    @patch('scoras.a2a.A2AAgent.receive_message')
    async def test_send_message(self, mock_receive):
        """Test sending a message through the hub."""
        # Set up the mock
        mock_receive.return_value = None
        
        # Register agents
        await self.hub.register_agent(self.a2a_agent1)
        await self.hub.register_agent(self.a2a_agent2)
        
        # Create a message
        message = A2AMessage(
            sender="agent1",
            receiver="agent2",
            content="Hello, agent2!"
        )
        
        # Send the message
        await self.hub.send_message(message)
        
        # Check that the message was processed
        self.assertEqual(len(self.hub.message_queue), 1)
        self.assertEqual(self.hub.message_queue[0], message)
        mock_receive.assert_called_once_with(message)
    
    def test_register_agent_sync(self):
        """Test registering an agent synchronously."""
        with patch('scoras.a2a.A2AHub.register_agent', return_value=asyncio.Future()) as mock_register:
            # Set the result of the future
            mock_register.return_value.set_result(None)
            
            # Register an agent synchronously
            self.hub.register_agent_sync(self.a2a_agent1)
            
            # Check that the method was called
            mock_register.assert_called_once_with(self.a2a_agent1)
    
    def test
(Content truncated due to size limit. Use line ranges to read in chunks)