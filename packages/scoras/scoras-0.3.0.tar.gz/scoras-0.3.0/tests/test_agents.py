import unittest
import asyncio
from unittest.mock import patch, MagicMock

from scoras.agents import Agent, Message, ModelConfig, ExpertAgent, CreativeAgent, MultiAgentSystem, AgentTeam

class TestAgent(unittest.TestCase):
    """Test the Agent class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = Agent(model="openai:gpt-4o")
    
    def test_initialization(self):
        """Test initialization of Agent."""
        self.assertIsInstance(self.agent.model_config, ModelConfig)
        self.assertEqual(self.agent.model_config.provider, "openai")
        self.assertEqual(self.agent.model_config.model_name, "gpt-4o")
        self.assertEqual(len(self.agent.messages), 1)  # System message
        self.assertEqual(self.agent.messages[0].role, "system")
    
    def test_model_config_from_string(self):
        """Test creating ModelConfig from string."""
        config = ModelConfig.from_string("anthropic:claude-3-opus")
        self.assertEqual(config.provider, "anthropic")
        self.assertEqual(config.model_name, "claude-3-opus")
        
        # Test with invalid format
        with self.assertRaises(ValueError):
            ModelConfig.from_string("invalid_format")
    
    @patch('scoras.agents.Agent._process_with_model')
    async def test_run(self, mock_process):
        """Test running the agent."""
        # Set up the mock
        mock_process.return_value = "This is a test response"
        
        # Run the agent
        response = await self.agent.run("Test message")
        
        # Check the result
        self.assertEqual(response, "This is a test response")
        self.assertEqual(len(self.agent.messages), 3)  # System + user + assistant
        self.assertEqual(self.agent.messages[1].role, "user")
        self.assertEqual(self.agent.messages[1].content, "Test message")
        self.assertEqual(self.agent.messages[2].role, "assistant")
        self.assertEqual(self.agent.messages[2].content, "This is a test response")
    
    def test_run_sync(self):
        """Test running the agent synchronously."""
        with patch('scoras.agents.Agent._process_with_model', return_value=asyncio.Future()) as mock_process:
            # Set the result of the future
            mock_process.return_value.set_result("This is a test response")
            
            # Run the agent synchronously
            response = self.agent.run_sync("Test message")
            
            # Check the result
            self.assertEqual(response, "This is a test response")
    
    def test_get_complexity_score(self):
        """Test getting the complexity score."""
        # Get the score
        score = self.agent.get_complexity_score()
        
        # Check the result
        self.assertIsInstance(score, dict)
        self.assertIn("total_score", score)
        self.assertIn("complexity_rating", score)
        self.assertGreater(score["total_score"], 0)

class TestExpertAgent(unittest.TestCase):
    """Test the ExpertAgent class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = ExpertAgent(
            model="openai:gpt-4o",
            domain="mathematics",
            expertise_level="advanced"
        )
    
    def test_initialization(self):
        """Test initialization of ExpertAgent."""
        self.assertEqual(self.agent.domain, "mathematics")
        self.assertEqual(self.agent.expertise_level, "advanced")
        self.assertIn("expert in mathematics", self.agent.system_prompt)
    
    def test_get_complexity_score(self):
        """Test getting the complexity score."""
        # Get the score
        score = self.agent.get_complexity_score()
        
        # Check the result
        self.assertIsInstance(score, dict)
        self.assertIn("total_score", score)
        self.assertIn("complexity_rating", score)
        self.assertGreater(score["total_score"], 0)
        
        # Compare with basic agent
        basic_agent = Agent(model="openai:gpt-4o")
        basic_score = basic_agent.get_complexity_score()
        
        # Expert agent should have higher complexity
        self.assertGreater(score["total_score"], basic_score["total_score"])

class TestCreativeAgent(unittest.TestCase):
    """Test the CreativeAgent class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = CreativeAgent(
            model="openai:gpt-4o",
            creative_domain="writing",
            creativity_level=0.8
        )
    
    def test_initialization(self):
        """Test initialization of CreativeAgent."""
        self.assertEqual(self.agent.creative_domain, "writing")
        self.assertEqual(self.agent.creativity_level, 0.8)
        self.assertIn("creative assistant", self.agent.system_prompt)
        self.assertGreaterEqual(self.agent.model_config.temperature, 0.7)
    
    def test_get_complexity_score(self):
        """Test getting the complexity score."""
        # Get the score
        score = self.agent.get_complexity_score()
        
        # Check the result
        self.assertIsInstance(score, dict)
        self.assertIn("total_score", score)
        self.assertIn("complexity_rating", score)
        self.assertGreater(score["total_score"], 0)
        
        # Compare with basic agent
        basic_agent = Agent(model="openai:gpt-4o")
        basic_score = basic_agent.get_complexity_score()
        
        # Creative agent should have higher complexity
        self.assertGreater(score["total_score"], basic_score["total_score"])

class TestMultiAgentSystem(unittest.TestCase):
    """Test the MultiAgentSystem class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent1 = Agent(model="openai:gpt-4o")
        self.agent2 = Agent(model="anthropic:claude-3-opus")
        self.system = MultiAgentSystem(agents=[self.agent1, self.agent2])
    
    def test_initialization(self):
        """Test initialization of MultiAgentSystem."""
        self.assertEqual(len(self.system.agents), 2)
        self.assertIsInstance(self.system.coordinator, Agent)
    
    @patch('scoras.agents.Agent.run')
    async def test_run(self, mock_run):
        """Test running the multi-agent system."""
        # Set up the mock
        mock_run.side_effect = [
            "Analysis: Both agents should handle this.",
            "Response from agent 1",
            "Response from agent 2",
            "Final synthesized response"
        ]
        
        # Run the system
        response = await self.system.run("Test message")
        
        # Check the result
        self.assertEqual(response, "Final synthesized response")
        self.assertEqual(mock_run.call_count, 4)  # Coordinator analysis + 2 agents + synthesis
    
    def test_get_complexity_score(self):
        """Test getting the complexity score."""
        # Get the score
        score = self.system.get_complexity_score()
        
        # Check the result
        self.assertIsInstance(score, dict)
        self.assertIn("total_score", score)
        self.assertIn("complexity_rating", score)
        self.assertGreater(score["total_score"], 0)
        
        # Compare with single agent
        single_agent = Agent(model="openai:gpt-4o")
        single_score = single_agent.get_complexity_score()
        
        # Multi-agent system should have higher complexity
        self.assertGreater(score["total_score"], single_score["total_score"])

class TestAgentTeam(unittest.TestCase):
    """Test the AgentTeam class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent1 = Agent(model="openai:gpt-4o")
        self.agent2 = Agent(model="anthropic:claude-3-opus")
        self.team = AgentTeam(
            name="Research Team",
            roles={
                "researcher": self.agent1,
                "writer": self.agent2
            }
        )
    
    def test_initialization(self):
        """Test initialization of AgentTeam."""
        self.assertEqual(self.team.name, "Research Team")
        self.assertEqual(len(self.team.roles), 2)
        self.assertIn("researcher", self.team.roles)
        self.assertIn("writer", self.team.roles)
        self.assertEqual(len(self.team.workflow), 2)
    
    @patch('scoras.agents.Agent.run')
    async def test_run(self, mock_run):
        """Test running the agent team."""
        # Set up the mock
        mock_run.side_effect = [
            "Analysis: Use researcher then writer.",
            "Research findings",
            "Final written report"
        ]
        
        # Run the team
        response = await self.team.run("Research quantum computing")
        
        # Check the result
        self.assertEqual(response, "Final written report")
        self.assertEqual(mock_run.call_count, 3)  # Coordinator + researcher + writer
    
    def test_get_complexity_score(self):
        """Test getting the complexity score."""
        # Get the score
        score = self.team.get_complexity_score()
        
        # Check the result
        self.assertIsInstance(score, dict)
        self.assertIn("total_score", score)
        self.assertIn("complexity_rating", score)
        self.assertGreater(score["total_score"], 0)
        
        # Compare with basic multi-agent system
        basic_system = MultiAgentSystem(agents=[self.agent1, self.agent2])
        basic_score = basic_system.get_complexity_score()
        
        # Agent team should have similar or higher complexity due to workflow
        self.assertGreaterEqual(score["total_score"], basic_score["total_score"])

if __name__ == "__main__":
    unittest.main()
