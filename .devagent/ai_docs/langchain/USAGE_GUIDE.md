# LangChain GitHub Copilot Customizations

Custom GitHub Copilot configurations for LangChain (Python) development.

## 📦 What's Included

### Custom Agent
**File**: `.github/agents/langchain.agent.md`

Activate this expert agent for LangChain development:
- Deep knowledge of agents, tools, models, and middleware
- Production patterns and best practices
- Streaming, structured output, and memory management
- Integration with LangSmith for observability

**Usage**: Mention `@langchain` in GitHub Copilot Chat to activate this expert mode.

---

### Custom Instructions
**File**: `.github/instructions/langchain.instructions.md`

Automatically applies to all Python files (`**/*.py`):
- Import organization patterns
- Tool definition standards (with type hints and docstrings)
- Model initialization patterns
- Agent creation best practices
- Message handling guidelines
- Error handling patterns
- Middleware patterns
- Testing best practices
- Common anti-patterns to avoid

**Usage**: Automatically applied when editing Python files. Ensures code follows LangChain v1.0+ standards.

---

### Reference Documentation
**Directory**: `.devagent/ai_docs/langchain/`

Comprehensive examples and patterns:

1. **`README.md`** - Quick start and overview
2. **`agent-patterns.md`** - Agent architecture patterns:
   - Basic agents
   - Agents with structured output
   - Agents with custom state
   - Multi-tool agents
   - Context-aware agents
   - Production patterns (error handling, observability, rate limiting)

3. **`tool-examples.md`** - Tool creation guide:
   - Basic tools
   - Tools with complex Pydantic schemas
   - Tools with runtime context (state, user context, memory)
   - Async tools
   - Error handling in tools
   - Tool testing

**Usage**: AI references these automatically for context. You can also link to them in prompts or documentation.

---

### Custom Prompts
**Directory**: `.github/prompts/`

Pre-built workflows for common tasks:

1. **`create-langchain-agent.prompt.md`**
   - **Purpose**: Create a new LangChain agent from scratch
   - **Includes**: Tool definitions, agent config, middleware, tests
   - **Best for**: Starting a new agent project
   
   **Usage**: Use GitHub Copilot's prompt library or reference directly

2. **`debug-langchain-agent.prompt.md`**
   - **Purpose**: Systematically debug LangChain issues
   - **Covers**: Tool calling, imports, state errors, API issues, streaming
   - **Includes**: Diagnostic techniques and common solutions
   
   **Usage**: When you encounter errors or unexpected behavior

---

## 🚀 Getting Started

### 1. Activate the LangChain Expert Agent

In GitHub Copilot Chat:
```
@langchain How do I create an agent with custom tools?
```

### 2. Use Custom Prompts

Access via GitHub Copilot's prompt library or reference directly:
```
#file:.github/prompts/create-langchain-agent.prompt.md

I need an agent that can search a database and send emails
```

### 3. Let Custom Instructions Guide You

Just start coding! When you write Python code, the instructions automatically ensure:
- ✅ Type hints on all tool parameters
- ✅ Clear, detailed docstrings
- ✅ Proper import patterns (v1.0+)
- ✅ Best practice patterns
- ✅ Error handling

### 4. Reference Documentation On-Demand

```
Show me an example of a context-aware tool from #file:.devagent/ai_docs/langchain/tool-examples.md
```

---

## 📚 Key Concepts Covered

### Agent Development
- Creating agents with `create_agent()`
- Tool binding and execution
- ReAct (Reasoning + Acting) pattern
- System prompts and model configuration
- Structured output with `ToolStrategy` and `ProviderStrategy`

### Tool Creation
- Using `@tool` decorator
- Pydantic schemas for complex inputs
- Runtime context access via `ToolRuntime`
- State, user context, and long-term memory
- Async tools for I/O-bound operations
- Error handling and validation

### Models & LLMs
- Model initialization with `init_chat_model()`
- Provider-agnostic syntax (e.g., `"openai:gpt-4o"`)
- Invocation methods: `invoke()`, `stream()`, `batch()`
- Tool calling and multimodal support
- Token usage tracking

### Messages & Prompts
- Message types: SystemMessage, HumanMessage, AIMessage, ToolMessage
- Content blocks for multimodal data
- Conversation history management
- Dynamic prompts with middleware

### Middleware
- Hooks: `@before_model`, `@after_model`, `@wrap_model_call`, `@wrap_tool_call`
- Dynamic model selection
- Error handling and guardrails
- Custom logging and monitoring

### Production Patterns
- LangSmith integration for observability
- Rate limiting
- Streaming with progress updates
- Error resilience
- Testing strategies

---

## 🔧 Integration with Your Project

These LangChain customizations work alongside your existing coding standards.

Example integration:
```python
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.agents import create_agent

# Your LangChain code follows best practices automatically
@tool
def analyze_sentiment(text: str) -> str:
    """Analyze sentiment of text input."""
    # Your implementation
    return "positive"

# Agent creation with proper configuration
agent = create_agent(
    model="openai:gpt-4o",
    tools=[analyze_sentiment],
    system_prompt="You are a sentiment analysis expert."
)
```

---

## 📖 LangChain Version

These customizations are designed for **LangChain v1.0+**

Key v1.0 changes covered:
- ✅ State schemas must be `TypedDict`, not Pydantic
- ✅ Use `ToolRuntime` instead of `InjectedState`/`InjectedStore`
- ✅ Structured output requires `ToolStrategy` or `ProviderStrategy`
- ✅ New import paths and module organization

---

## 🔗 External Resources

- **LangChain Docs**: https://docs.langchain.com/
- **API Reference**: https://reference.langchain.com/python/
- **LangSmith**: https://smith.langchain.com/ (observability platform)
- **GitHub**: https://github.com/langchain-ai/langchain

---

## ✨ Next Steps

1. **Try the expert agent**: `@langchain` in Copilot Chat
2. **Create a new agent**: Use the `create-langchain-agent` prompt
3. **Debug existing code**: Use the `debug-langchain-agent` prompt
4. **Explore patterns**: Browse `.devagent/ai_docs/langchain/`
5. **Write new tools**: Follow patterns in `tool-examples.md`

---

## 🤝 Contributing

Found these customizations helpful? Consider sharing them with the DevAgent community or creating similar configurations for other frameworks you use!

For questions or improvements, refer to the LangChain documentation or use the expert agent for guidance.

Happy coding with LangChain! 🦜🔗
