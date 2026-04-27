---
name: 'LangChain Standards'
description: 'LangChain coding standards and best practices for Python'
applyTo: '**/*.py'
---

# LangChain Python Coding Standards

These constraints apply when code imports from `langchain`. For procedural guidance, see skills and ai_docs.

## Non-Negotiable Constraints

1. **Always use type hints** on all tool parameters and return types — the model uses them to infer schema
2. **Always provide clear docstrings** on tools — they guide model behavior and tool selection
3. **Use `ToolRuntime`** instead of deprecated `InjectedState`/`InjectedStore` — the modern context API
4. **State schemas must be `TypedDict`**, not Pydantic models — required by LangGraph state machinery
5. **Use `init_chat_model()`** for model initialization — supports provider inference from prefixed IDs

## Additional Resources

- **Skills**: `langchain-tooling-basics`, `langchain-agent-workflows`
- **Detailed examples**: `.devagent/ai_docs/langchain/` (tools, agents, middleware, streaming, structured output, troubleshooting)
- **Expert assistance**: `../agents/langchain.agent.md`

