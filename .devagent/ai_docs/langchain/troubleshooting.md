# LangChain Troubleshooting Guide

Common issues and solutions when working with LangChain agents and applications.

## Table of Contents
1. [Tool Calling Issues](#tool-calling-issues)
2. [Import and Module Errors](#import-and-module-errors)
3. [State and Type Errors](#state-and-type-errors)
4. [API and Authentication Errors](#api-and-authentication-errors)
5. [Streaming Issues](#streaming-issues)
6. [Performance Problems](#performance-problems)
7. [Migration Issues (v0.x → v1.0)](#migration-issues-v0x--v10)

---

## Tool Calling Issues

### Problem: Model Doesn't Call Tools

**Symptoms**: Agent responds without using tools, even when they're needed.

**Common Causes**:
1. Vague tool descriptions
2. Missing type hints
3. Tool not properly bound to model
4. Model doesn't support tool calling

**Solutions**:

```python
# ❌ BAD: Vague description
@tool
def search(query: str) -> str:
    """Search."""  # Too vague!
    return "results"

# ✅ GOOD: Clear, detailed description
@tool
def search_products(query: str) -> str:
    """Search the product database for items matching the query.
    
    Use this when users ask about products, inventory, pricing, or availability.
    Supports product names, SKUs, categories, and descriptions.
    
    Args:
        query: Product name, SKU, category, or search terms
    """
    return "results"

# ✅ GOOD: Add type hints
@tool
def calculate(expression: str, precision: int = 2) -> str:
    """Calculate mathematical expressions."""
    return str(eval(expression))

# ✅ GOOD: Explicit system prompt
agent = create_agent(
    model="openai:gpt-4o",
    tools=[search_products],
    system_prompt="You are a product assistant. When users ask about products, ALWAYS use the search_products tool to find accurate information."
)
```

### Problem: Tool Called with Wrong Arguments

**Symptoms**: Tool receives incorrect or missing arguments.

**Solutions**:

```python
# ✅ Use Pydantic schema for complex inputs
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    """Input schema with validation."""
    query: str = Field(description="Search terms")
    category: str = Field(description="Product category", default="all")
    max_results: int = Field(description="Max results", ge=1, le=100, default=10)

@tool(args_schema=SearchInput)
def search_products(query: str, category: str = "all", max_results: int = 10) -> str:
    """Search products with validated inputs."""
    return f"Searching {category} for '{query}' (max {max_results})"

# ✅ Add field examples
class EmailInput(BaseModel):
    recipient: str = Field(description="Email address", examples=["user@example.com"])
    subject: str = Field(description="Subject line", examples=["Meeting Reminder"])
```

---

## Import and Module Errors

### Problem: ModuleNotFoundError or ImportError

**Symptoms**: `ModuleNotFoundError: No module named 'langchain.X'`

**Common Causes**:
1. Wrong import path (changed in v1.0)
2. Missing optional dependencies
3. Package version mismatch

**Solutions**:

```python
# ✅ CORRECT v1.0+ imports
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langchain.agents.middleware import wrap_tool_call, dynamic_prompt
from langchain.agents.structured_output import ToolStrategy, ProviderStrategy

# ❌ OLD patterns (don't use)
# from langchain.agents.react import ReActAgent
# from langgraph.prebuilt.tool_node import InjectedState

# ✅ Install missing dependencies
# pip install langchain-openai      # For OpenAI
# pip install langchain-anthropic   # For Anthropic
# pip install langchain-google-genai # For Google
# pip install langgraph             # For agents
```

### Problem: Import Path Changed

**Error**: `ImportError: cannot import name 'X' from 'langchain.Y'`

**Solution**: Check v1.0 migration guide for correct paths:

```python
# v0.x → v1.0 import changes
# OLD: from langchain.schema import HumanMessage
# NEW: from langchain.messages import HumanMessage

# OLD: from langchain.llms import OpenAI
# NEW: from langchain_openai import ChatOpenAI
```

---

## State and Type Errors

### Problem: TypeError with State Schema

**Symptoms**: `TypeError: state must be TypedDict, got BaseModel`

**Cause**: v1.0 requires `TypedDict` for state, not Pydantic models.

**Solutions**:

```python
# ❌ OLD (doesn't work in v1.0)
from pydantic import BaseModel

class OldState(BaseModel):
    user_id: str
    score: int

# ✅ NEW (v1.0+)
from typing import TypedDict
from langchain.agents import AgentState

class NewState(AgentState):
    user_id: str
    score: int

agent = create_agent(
    model="openai:gpt-4o",
    tools=[],
    state_schema=NewState
)
```

### Problem: Pydantic Validation Errors

**Symptoms**: `ValidationError: field required`

**Solutions**:

```python
# ✅ Provide default values
class MyState(AgentState):
    user_id: str
    score: int = 0  # Default value
    preferences: dict = {}  # Default empty dict

# ✅ Use optional fields
class MyState(AgentState):
    user_id: str
    email: str | None = None  # Optional field

# ✅ Initialize with all required fields
result = agent.invoke({
    "messages": [...],
    "user_id": "user123",  # Required field
    "score": 0
})
```

---

## API and Authentication Errors

### Problem: 401 Unauthorized

**Symptoms**: `AuthenticationError: Invalid API key`

**Solutions**:

```python
# ✅ Check environment variables
import os
print(os.environ.get("OPENAI_API_KEY"))  # Is it set?
print(os.environ.get("ANTHROPIC_API_KEY"))

# ✅ Set environment variable
os.environ["OPENAI_API_KEY"] = "your-key-here"

# ✅ Or pass directly (less secure)
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o", api_key="your-key")
```

### Problem: 429 Rate Limit Exceeded

**Symptoms**: `RateLimitError: Too many requests`

**Solutions**:

```python
# ✅ Solution 1: Add rate limiter
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_openai import ChatOpenAI

rate_limiter = InMemoryRateLimiter(
    requests_per_second=10/60,  # 10 per minute
    check_every_n_seconds=0.1
)

model = ChatOpenAI(model="gpt-4o", rate_limiter=rate_limiter)

# ✅ Solution 2: Batch with concurrency control
results = model.batch(
    inputs,
    config={"max_concurrency": 3}  # Limit parallel requests
)

# ✅ Solution 3: Add delays in tools
import time

@tool
def api_call(endpoint: str) -> str:
    """Call external API with rate limiting."""
    time.sleep(1)  # Add delay
    return "results"
```

### Problem: Timeout Errors

**Symptoms**: `TimeoutError: Request timed out`

**Solutions**:

```python
# ✅ Increase timeout
model = init_chat_model(
    "openai:gpt-4o",
    timeout=120  # 2 minutes
)

# ✅ Add retry logic
model = ChatOpenAI(
    model="gpt-4o",
    timeout=60,
    max_retries=5  # Retry up to 5 times
)
```

---

## Streaming Issues

### Problem: Chunks Not Appearing

**Symptoms**: No output during streaming, or incomplete messages.

**Solutions**:

```python
# ✅ Check stream mode
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "test"}]},
    stream_mode="values"  # Try "messages" or "updates" too
):
    print(chunk)

# ✅ Aggregate chunks correctly
from langchain_core.messages import AIMessageChunk

full_message = None
for chunk in model.stream("Hello"):
    if full_message is None:
        full_message = chunk
    else:
        full_message = full_message + chunk
    print(chunk.text, end="", flush=True)

# ✅ Use flush=True for real-time output
for chunk in model.stream("Write a story"):
    print(chunk.text, end="", flush=True)  # flush=True is important
```

### Problem: Streaming Blocked

**Symptoms**: Streaming starts but then hangs.

**Solutions**:

```python
# ✅ Check if all components support streaming
# Some middleware or tools may block streaming

# ✅ Use async streaming for better control
async def stream_async():
    async for chunk in model.astream("Hello"):
        print(chunk.text, end="", flush=True)

import asyncio
asyncio.run(stream_async())
```

---

## Performance Problems

### Problem: Slow Response Times

**Symptoms**: Agent takes too long to respond.

**Solutions**:

```python
# ✅ Solution 1: Use faster models for simple tasks
fast_model = init_chat_model("openai:gpt-4o-mini", temperature=0.3)

# ✅ Solution 2: Reduce max_tokens
model = init_chat_model("openai:gpt-4o", max_tokens=500)

# ✅ Solution 3: Simplify system prompts
# Shorter prompts = faster processing

# ✅ Solution 4: Use batch processing
results = model.batch(inputs, config={"max_concurrency": 10})
```

### Problem: High Token Usage / Cost

**Symptoms**: Unexpectedly high API costs.

**Solutions**:

```python
# ✅ Monitor token usage
response = model.invoke("Hello")
if response.usage_metadata:
    print(f"Tokens: {response.usage_metadata['total_tokens']}")

# ✅ Use cheaper models when appropriate
budget_model = init_chat_model("openai:gpt-4o-mini")

# ✅ Implement prompt caching
# OpenAI and Anthropic automatically cache repeated prefixes

# ✅ Limit response length
model = init_chat_model("openai:gpt-4o", max_tokens=500)

# ✅ Summarize long conversations
# Compress old messages to reduce input tokens
```

---

## Migration Issues (v0.x → v1.0)

### Problem: Agent Creation Changed

```python
# ❌ OLD (v0.x)
from langchain.agents import initialize_agent, AgentType

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# ✅ NEW (v1.0+)
from langchain.agents import create_agent

agent = create_agent(
    model="openai:gpt-4o",
    tools=tools,
    system_prompt="You are helpful."
)
```

### Problem: State Schema Changed

```python
# ❌ OLD (v0.x)
from pydantic import BaseModel

class OldState(BaseModel):
    user_id: str

# ✅ NEW (v1.0+)
from typing import TypedDict
from langchain.agents import AgentState

class NewState(AgentState):
    user_id: str
```

### Problem: Tool Runtime Changed

```python
# ❌ OLD (v0.x)
from langgraph.prebuilt.tool_node import InjectedState

@tool
def old_tool(state: InjectedState) -> str:
    return state["messages"]

# ✅ NEW (v1.0+)
from langchain.tools import tool, ToolRuntime

@tool
def new_tool(runtime: ToolRuntime) -> str:
    return str(runtime.state["messages"])
```

### Problem: Structured Output Changed

```python
# ❌ OLD (v0.x)
agent = create_agent(
    model="openai:gpt-4o",
    response_format=MySchema
)

# ✅ NEW (v1.0+)
from langchain.agents.structured_output import ToolStrategy

agent = create_agent(
    model="openai:gpt-4o",
    response_format=ToolStrategy(MySchema)
)
```

---

## Debugging Techniques

### Enable Verbose Logging

```python
import logging

# Set LangChain to DEBUG
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("langchain").setLevel(logging.DEBUG)

# Or use environment variable
import os
os.environ["LANGCHAIN_VERBOSE"] = "true"
```

### Test Components Independently

```python
# Test tool separately
from tools import my_tool

result = my_tool.invoke({"param": "value"})
print(result)  # Does it work?

# Test model separately
model = init_chat_model("openai:gpt-4o")
response = model.invoke("Hello")
print(response)  # Does it respond?

# Test tool binding
model_with_tools = model.bind_tools([my_tool])
response = model_with_tools.invoke("Use the tool")
print(response.tool_calls)  # Does it call tools?
```

### Use LangSmith for Tracing

```python
import os

# Enable LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-key"
os.environ["LANGCHAIN_PROJECT"] = "debugging"

# Run agent - traces appear at https://smith.langchain.com/
result = agent.invoke({"messages": [...]})
```

---

## Getting Help

1. **Check official docs**: https://docs.langchain.com/
2. **Search GitHub issues**: https://github.com/langchain-ai/langchain/issues
3. **LangChain Discord**: Active community support
4. **Stack Overflow**: Tag `langchain`
5. **API Reference**: https://reference.langchain.com/python/

---

## Quick Diagnostic Checklist

Before asking for help, verify:

- [ ] LangChain version is v1.0+ (`pip show langchain`)
- [ ] All required packages installed (`langchain-openai`, etc.)
- [ ] Environment variables set correctly (`OPENAI_API_KEY`, etc.)
- [ ] Tool descriptions are clear and detailed
- [ ] Type hints present on all tool parameters
- [ ] State schema uses `TypedDict`, not Pydantic
- [ ] Model supports features you're using (tool calling, etc.)
- [ ] Tools tested independently
- [ ] Error messages read carefully
- [ ] LangSmith tracing enabled for complex issues

---

## Common Error Messages

| Error | Likely Cause | Solution |
|-------|-------------|----------|
| `ModuleNotFoundError: No module named 'langchain_X'` | Missing provider package | `pip install langchain-X` |
| `TypeError: state must be TypedDict` | Using Pydantic for state | Use `TypedDict` instead |
| `AuthenticationError` | Invalid/missing API key | Set environment variable |
| `RateLimitError` | Too many requests | Add rate limiter |
| `TimeoutError` | Request took too long | Increase timeout |
| `ValidationError` | Pydantic validation failed | Check schema and data |
| `Tool not found` | Tool not in agent's tools list | Add tool to `tools=[]` |
| `ImportError: cannot import` | Wrong import path | Check v1.0 migration guide |

---

See also:
- **Agent patterns**: `agent-patterns.md`
- **Tool examples**: `tool-examples.md`
- **Model integration**: `model-integration.md`
- **Middleware guide**: `middleware-guide.md`
````