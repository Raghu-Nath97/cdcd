---
name: langchain-agent-workflows
description: 'Build LangChain agents with create_agent, init_chat_model, batch processing, and structured output. Use when building agents with create_agent, initializing models with init_chat_model, configuring batch processing with model.batch, or setting up structured output with ToolStrategy.'
---

# LangChain Agent Workflows

## When to use
- Building or refactoring `create_agent` pipelines
- Initializing models with `init_chat_model()`
- Converting sequential `model.invoke()` loops to `model.batch()`
- Setting up structured output with `ToolStrategy` or `ProviderStrategy`
- Adding middleware (HITL approval, logging, retry)

## Procedure
1. Initialize models with `init_chat_model()` using provider-prefixed IDs (`"openai:gpt-4o"`, `"anthropic:claude-sonnet-4-5"`).
2. Collect tool functions and create the agent with a focused system prompt.
3. For parallel workloads, replace sequential loops with `model.batch(items, config={"max_concurrency": 10})`.
4. For structured output, set an explicit `ToolStrategy` or `ProviderStrategy`.
5. Keep orchestration thin — push business logic into `@tool` functions or graph nodes.

## Basic Agent Setup

```python
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

model = init_chat_model("openai:gpt-4o")
agent = create_agent(
    model=model,
    tools=[search_tool, calculator_tool],
    system_prompt="You are a helpful assistant."
)

result = agent.invoke({"messages": [{"role": "user", "content": "Find product X"}]})
```

## Batch Processing

```python
# Wrong: sequential — slow
results = [model.invoke(item) for item in items]

# Fix: use batch with concurrency
results = model.batch(
    [{"query": "alpha"}, {"query": "beta"}],
    config={"max_concurrency": 10}
)
```

## Model Initialization

```python
# Provider is inferred from the prefix
model = init_chat_model("openai:gpt-4o")
model = init_chat_model("anthropic:claude-sonnet-4-5")
model = init_chat_model("azure_openai:gpt-4o", azure_deployment="my-deploy")
```

## Common Mistakes

### Wrong: hardcoding provider-specific class

```python
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o")  # Tightly coupled to OpenAI

# Fix: use init_chat_model for provider-agnostic setup
from langchain.chat_models import init_chat_model
model = init_chat_model("openai:gpt-4o")
```

### Wrong: fat orchestration logic in agent assembly

```python
# Don't put business logic in the agent creation layer
agent = create_agent(
    model=model,
    tools=[search_tool],
    system_prompt="You are an assistant that always checks inventory first, "
                  "then calculates shipping, then formats the response as..."
    # Too much logic here — move it into tools or graph nodes
)
```

## Verification
- Agent uses `init_chat_model()`, not provider-specific classes.
- `model.batch()` replaces sequential loops where parallelism is safe.
- Structured output uses explicit strategy (`ToolStrategy` / `ProviderStrategy`).
- System prompt is concise; domain logic lives in tools.

## References
- [Agent Patterns](.devagent/ai_docs/langchain/agent-patterns.md) — agent architectures, structured output agents
- [Model Integration](.devagent/ai_docs/langchain/model-integration.md) — init_chat_model, provider config
- [Structured Output](.devagent/ai_docs/langchain/structured-output.md) — ToolStrategy, ProviderStrategy
- [Streaming Patterns](.devagent/ai_docs/langchain/streaming-patterns.md) — real-time streaming agents

## Related Skills
- `langchain-tooling-basics` — defining the tools that agents use
- `reviewing-python-code` — Python coding standards
