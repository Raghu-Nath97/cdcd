# LangChain Reference Documentation

This directory contains reference documentation and examples for LangChain development in Python.

## Contents

- **`agent-patterns.md`**: Common agent architecture patterns and examples
- **`tool-examples.md`**: Comprehensive tool creation examples
- **`model-integration.md`**: Model initialization and configuration patterns
- **`middleware-guide.md`**: Middleware patterns for customization
- **`structured-output.md`**: Structured output strategies and examples
- **`streaming-patterns.md`**: Streaming and real-time update patterns
- **`memory-state.md`**: Memory management and state handling
- **`troubleshooting.md`**: Common issues and solutions

## Quick Start

### Basic Agent Example
```python
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get current weather for a location."""
    return f"Weather in {location}: Sunny, 72°F"

agent = create_agent(
    model="openai:gpt-4o",
    tools=[get_weather],
    system_prompt="You are a helpful weather assistant."
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "What's the weather in Paris?"}]
})
```

## Key Concepts

### Messages
All interactions use message objects or dictionaries with roles:
- **SystemMessage**: Initial instructions and context
- **HumanMessage**: User input
- **AIMessage**: Model responses
- **ToolMessage**: Tool execution results

### Tools
Functions that agents can call, defined with:
- Type-hinted parameters (required for schema generation)
- Clear docstrings (guide model when to use the tool)
- Optional Pydantic schemas for complex inputs

### Agents
Orchestrate models and tools in a ReAct loop:
1. Model reasons about the task
2. Decides which tool(s) to call
3. Executes tools
4. Analyzes results
5. Repeats or provides final answer

### Middleware
Intercept and modify agent execution:
- Before/after model calls
- Dynamic prompt generation
- Tool error handling
- Model selection logic

## External Resources

- **Official Docs**: https://docs.langchain.com/
- **API Reference**: https://reference.langchain.com/python/
- **GitHub**: https://github.com/langchain-ai/langchain
- **LangSmith**: https://smith.langchain.com/ (for observability)

## Integration Points

- **LangChain Coding Standards**: See `USAGE_GUIDE.md` in this directory for Python-specific patterns
- **Additional Documentation**: Explore other files in this directory for detailed guides
- **Custom Agent**: Use the `@langchain` agent for expert assistance
- **Custom Prompts**: Use LangChain prompts/commands for workflow assistance

