---
name: langchain-tooling-basics
description: 'Define LangChain tools with @tool decorator, type hints, docstrings, and ToolRuntime. Use when creating @tool functions, adding ToolRuntime for runtime context, migrating from deprecated InjectedState, or reviewing tool definitions for model usability.'
---

# LangChain Tooling Basics

## When to use
- Creating or updating `@tool` functions
- Adding runtime context (user sessions, state) via `ToolRuntime`
- Migrating from deprecated `InjectedState` / `InjectedStore`
- Reviewing tool definitions for model usability

## Procedure
1. Import `tool` and `ToolRuntime` from `langchain.tools`.
2. Define the tool with full type hints and a docstring that explains **what it does**, **what inputs mean**, and **what it returns**.
3. If runtime context is required, accept `runtime: ToolRuntime[ContextType]` and read from `runtime.context`.
4. Return JSON-serializable values (strings, dicts, lists) that match the docstring.
5. Use `TypedDict` for context type schemas, not Pydantic models.

## Basic Tool

```python
from langchain.tools import tool

@tool
def search(query: str, limit: int = 10) -> str:
    """Search the product database for items matching the query.

    Args:
        query: Product name, SKU, or description to search for.
        limit: Maximum number of results (default: 10).
    """
    return f"Found {limit} results for '{query}'"
```

## Tool with Runtime Context

```python
from typing import TypedDict
from langchain.tools import tool, ToolRuntime

class UserContext(TypedDict):
    user_id: str

@tool
def get_orders(status: str, runtime: ToolRuntime[UserContext]) -> str:
    """Return order summaries for the current user filtered by status.

    Args:
        status: Filter by status (pending, completed, cancelled).
    """
    return f"Orders for {runtime.context['user_id']} with status {status}"
```

## Common Mistakes

### Wrong: missing type hints

```python
@tool
def bad_tool(query):  # Model cannot infer parameter type
    """Search database."""
    return "results"

# Fix: add type hints
@tool
def good_tool(query: str) -> str:
    """Search the product database by name or SKU."""
    return "results"
```

### Wrong: vague docstring

```python
@tool
def search(q: str) -> str:
    """Search."""  # Model won't know when to use this tool
    return "results"

# Fix: describe what, when, and what it returns
@tool
def search(query: str) -> str:
    """Search the product catalog by name, category, or SKU. Returns matching product summaries."""
    return "results"
```

### Wrong: using deprecated InjectedState

```python
from langgraph.prebuilt.tool_node import InjectedState  # Deprecated

@tool
def old_tool(state: InjectedState) -> str:
    return state["messages"]

# Fix: use ToolRuntime
from langchain.tools import ToolRuntime

@tool
def new_tool(runtime: ToolRuntime[MyContext]) -> str:
    return runtime.context["messages"]
```

## Verification
- Tool parameters and return types are fully annotated.
- Docstring describes purpose, inputs, and output shape.
- `ToolRuntime` is used for context, not `InjectedState`.
- State schemas use `TypedDict`, not Pydantic.

## References
- [Tool Creation Guide](.devagent/ai_docs/langchain/tool-examples.md) — basic to advanced tool patterns
- [Middleware Guide](.devagent/ai_docs/langchain/middleware-guide.md) — HITL approval, Command resume
- [Troubleshooting](.devagent/ai_docs/langchain/troubleshooting.md) — common tool errors

## Related Skills
- `langchain-agent-workflows` — wiring tools into agents
- `reviewing-python-code` — Python coding standards
