# Scoras: Intelligent Agent Framework with Complexity Scoring

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

Scoras is a powerful, intuitive framework for building intelligent agents with built-in complexity scoring. Inspired by PydanticAI and Langgraph but designed to be more accessible and comprehensive, Scoras provides everything you need to create sophisticated AI agents, RAG systems, and multi-agent workflows.

## Key Features

- **Integrated Complexity Scoring**: Automatically measure and understand the complexity of your agent workflows
- **Multi-Model Support**: Work with OpenAI, Anthropic, Google Gemini, and other LLM providers
- **Protocol Support**: Native integration with MCP (Model Context Protocol) and A2A (Agent-to-Agent) protocols
- **Intuitive API**: Simple, expressive interface for creating agents and tools
- **Advanced Graph-Based Workflows**: Create sophisticated agent workflows with conditional branching
- **Enhanced RAG Capabilities**: Build powerful retrieval-augmented generation systems
- **Structured Data Validation**: Leverages Pydantic-style validation for robust data handling
- **Comprehensive Tooling**: Extensive tool framework for agent capabilities

## Installation

```bash
pip install scoras
```

## Quick Start

```python
import scoras as sc

# Create a simple agent
agent = sc.Agent(
    model="openai:gpt-4o",
    system_prompt="You are a helpful assistant."
)

# Run the agent
response = agent.run_sync("What is the capital of France?")
print(response)

# Check the complexity score
score = agent.get_complexity_score()
print(f"Complexity: {score['complexity_rating']} (Score: {score['total_score']})")
```

## Creating Tools

```python
import scoras as sc

# Create a tool using the decorator
@sc.tool(name="calculator", description="Perform calculations", complexity="simple")
async def calculator(operation: str, a: float, b: float) -> float:
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    else:
        raise ValueError(f"Unknown operation: {operation}")

# Create an agent with the tool
agent = sc.Agent(
    model="openai:gpt-4o",
    system_prompt="You are a helpful assistant with calculation abilities.",
    tools=[calculator]
)

# Run the agent with a query that will use the tool
response = agent.run_sync("What is 25 multiplied by 16?")
print(response)

# Check the complexity score
score = agent.get_complexity_score()
print(f"Complexity: {score['complexity_rating']} (Score: {score['total_score']})")
```

## Building RAG Systems

```python
import scoras as sc
from scoras.rag import Document, SimpleRAG

# Create documents
documents = [
    Document(content="The capital of France is Paris, known as the City of Light."),
    Document(content="Paris is famous for the Eiffel Tower, built in 1889."),
    Document(content="France has a population of about 67 million people.")
]

# Create a RAG system
rag = SimpleRAG(
    agent=sc.Agent(model="openai:gpt-4o"),
    documents=documents
)

# Run the RAG system
response = rag.run_sync("What is the capital of France and what is it known for?")
print(response)

# Check the complexity score
score = rag.get_complexity_score()
print(f"Complexity: {score['complexity_rating']} (Score: {score['total_score']})")
```

## Creating Workflows with Graphs

```python
import scoras as sc
from pydantic import BaseModel

# Define the state model
class WorkflowState(BaseModel):
    query: str
    processed_query: str = ""
    search_results: list = []
    final_answer: str = ""

# Define node functions
async def preprocess(state):
    return {"processed_query": state.query.strip().lower()}

async def search(state):
    # Simulate search
    results = [f"Result for {state.processed_query}", "Another result"]
    return {"search_results": results}

async def generate_answer(state):
    answer = f"Based on {len(state.search_results)} results, the answer is..."
    return {"final_answer": answer}

# Create a workflow graph
graph = sc.WorkflowGraph(state_type=WorkflowState)

# Add nodes
graph.add_node("start", lambda s: s, "simple")
graph.add_node("preprocess", preprocess, "standard")
graph.add_node("search", search, "standard")
graph.add_node("generate", generate_answer, "complex")
graph.add_node("end", lambda s: s, "simple")

# Add edges
graph.add_edge("start", "preprocess")
graph.add_edge("preprocess", "search")
graph.add_edge("search", "generate")
graph.add_edge("generate", "end")

# Compile the graph
workflow = graph.compile()

# Run the workflow
result = workflow.run_sync(WorkflowState(query="What is quantum computing?"))
print(result.final_answer)

# Check the complexity score
score = graph.get_complexity_score()
print(f"Complexity: {score['complexity_rating']} (Score: {score['total_score']})")
```

## Protocol Support

### Model Context Protocol (MCP)

Scoras provides native support for the Model Context Protocol (MCP), allowing your agents to interact with MCP servers and act as MCP servers themselves.

```python
import scoras as sc
from scoras.mcp import create_mcp_server, MCPClient, run_mcp_server

# Create tools
@sc.tool(name="calculator", description="Perform calculations")
async def calculator(operation: str, a: float, b: float) -> float:
    # Implementation...
    return result

# Create an MCP server
server = create_mcp_server(
    name="ScorasServer",
    description="Scoras MCP server with tools",
    tools=[calculator],
    capabilities=["tools"]
)

# In one process, run the server
await run_mcp_server(server, host="0.0.0.0", port=8000)

# In another process, connect to the server
client = MCPClient(server_url="http://localhost:8000")

# Execute a tool on the server
result = await client.execute_tool(
    tool_name="calculator",
    parameters={
        "operation": "multiply",
        "a": 5,
        "b": 7
    }
)
print(result)  # {"result": 35}
```

### Agent-to-Agent (A2A) Protocol

Scoras also supports Google's A2A protocol, enabling communication between agents across different frameworks and vendors.

```python
import scoras as sc
from scoras.a2a import create_agent_skill, create_a2a_server, A2AClient, run_a2a_server

# Create an agent
agent = sc.Agent(
    model="openai:gpt-4o",
    system_prompt="You are a helpful assistant."
)

# Define skills
math_skill = create_agent_skill(
    id="math",
    name="Mathematics",
    description="Perform mathematical calculations",
    complexity="standard"
)

# Create an A2A server
server = create_a2a_server(
    name="ScorasAgent",
    description="A versatile agent powered by Scoras",
    agent=agent,
    skills=[math_skill]
)

# In one process, run the server
await run_a2a_server(server, host="0.0.0.0", port=8001)

# In another process, connect to the server
client = A2AClient(agent_url="http://localhost:8001")

# Send a task to the agent
task = await client.send_task(
    message="Calculate the area of a circle with radius 5 cm."
)
print(task)
```

## Understanding Complexity Scores

Scoras provides a unique complexity scoring system that helps you understand and manage the complexity of your agent workflows:

- **Nodes**: Basic processing units (1-1.5 points each)
- **Edges**: Connections between nodes (1.5-4 points each)
- **Tools**: Agent capabilities (1.4-3 points each)
- **Conditions**: Decision points (2.5 points each)

Complexity ratings:
- **Simple**: Score < 10
- **Moderate**: Score 10-25
- **Complex**: Score 25-50
- **Very Complex**: Score 50-100
- **Extremely Complex**: Score > 100

```python
# Get detailed complexity report
score_report = agent.get_complexity_score()
print(json.dumps(score_report, indent=2))

# Example output:
# {
#   "total_score": 15.5,
#   "complexity_rating": "Moderate",
#   "component_scores": {
#     "nodes": 3.0,
#     "edges": 4.5,
#     "tools": 8.0,
#     "conditions": 0.0
#   },
#   "component_counts": {
#     "nodes": 3,
#     "edges": 3,
#     "tools": 4,
#     "conditions": 0
#   },
#   "breakdown": {
#     "nodes": "3 nodes (3.0 points)",
#     "edges": "3 edges (4.5 points)",
#     "tools": "4 tools (8.0 points)",
#     "conditions": "0 conditions (0.0 points)"
#   }
# }
```

## Advanced Features

### Specialized Agents

```python
from scoras.agents import ExpertAgent, CreativeAgent, RAGAgent

# Create an expert agent for a specific domain
expert = ExpertAgent(
    model="anthropic:claude-3-opus",
    domain="medicine",
    expertise_level="advanced"
)

# Create a creative agent for content generation
creative = CreativeAgent(
    model="openai:gpt-4o",
    creativity_level="high"
)

# Create a RAG agent with built-in retrieval
rag_agent = RAGAgent(
    model="gemini:gemini-pro",
    documents=[Document(content="..."), Document(content="...")],
    retrieval_type="semantic"
)
```

### Multi-Agent Systems

```python
from scoras.agents import MultiAgentSystem

# Create individual agents
researcher = sc.Agent(model="openai:gpt-4o", system_prompt="You are a research specialist.")
writer = sc.Agent(model="anthropic:claude-3-opus", system_prompt="You are a writing expert.")
fact_checker = sc.Agent(model="gemini:gemini-pro", system_prompt="You verify facts.")

# Create a multi-agent system
system = MultiAgentSystem(
    agents={
        "researcher": researcher,
        "writer": writer,
        "fact_checker": fact_checker
    },
    coordinator_prompt="Coordinate the research, writing, and fact-checking process."
)

# Run the system
result = system.run_sync("Create a well-researched article about quantum computing.")
```

### Advanced RAG

```python
from scoras.rag import ContextualRAG, SemanticChunker

# Create a chunker
chunker = SemanticChunker(chunk_size=200, overlap=50)

# Process documents
processed_docs = chunker.process([
    Document(content="Long document content..."),
    Document(content="Another long document...")
])

# Create a contextual RAG system
rag = ContextualRAG(
    agent=sc.Agent(model="openai:gpt-4o"),
    documents=processed_docs,
    context_window_size=5
)

# Run with context adaptation
response = rag.run_sync("What are the key points about quantum entanglement?")
```

## Tool Chains

```python
from scoras.tools import ToolChain, ToolRouter

# Create individual tools
calculator_tool = sc.tool(name="calculator")(lambda op, a, b: eval(f"{a} {op} {b}"))
weather_tool = sc.tool(name="weather")(lambda location: {"temp": 72, "conditions": "sunny"})

# Create a tool chain
chain = ToolChain(
    name="math_and_weather",
    tools=[calculator_tool, weather_tool],
    description="Perform calculations and get weather information"
)

# Create a tool router
router = ToolRouter(
    tools=[calculator_tool, weather_tool],
    routing_strategy="content_based"
)

# Add to an agent
agent = sc.Agent(
    model="openai:gpt-4o",
    tools=[chain, router]
)
```

## License

Scoras is created by Anderson L. Amaral and is available under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
