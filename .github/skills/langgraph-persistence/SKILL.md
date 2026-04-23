---
name: langgraph-persistence
description: 'Add LangGraph persistence: configure checkpointers for conversation memory, set up cross-thread memory stores, debug state persistence issues. Use when adding MemorySaver or PostgresSaver checkpointers, configuring InMemoryStore or PostgresStore, or troubleshooting missing state across invocations.'
---

# LangGraph Persistence

## When to use
- Adding a checkpointer (`MemorySaver`, `PostgresSaver`) for conversation memory
- Configuring cross-thread memory stores (`InMemoryStore`, `PostgresStore`)
- Debugging why state is lost between invocations
- Setting up `thread_id` based state isolation

## Procedure
1. Choose a checkpointer: `MemorySaver` for development, `PostgresSaver` for production.
2. Pass the checkpointer to `builder.compile(checkpointer=checkpointer)`.
3. Always provide a `thread_id` in the config when invoking the graph.
4. For cross-thread memory (e.g. user preferences shared across conversations), add a memory store.
5. Access the store inside nodes via the `store` keyword argument.

## Checkpointer Setup

### Development — MemorySaver

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# Every invoke with the same thread_id resumes from last state
result = graph.invoke(
    {"messages": [HumanMessage("Hello")]},
    config={"configurable": {"thread_id": "user-123"}}
)
```

### Production — PostgresSaver

```python
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver.from_conn_string("postgresql://user:pass@host/db")
graph = builder.compile(checkpointer=checkpointer)
```

## Cross-Thread Memory Store

Stores persist data across threads (conversations), useful for user preferences, long-term facts, or shared context.

```python
from langgraph.store.memory import InMemoryStore
from langgraph.store.base import BaseStore

store = InMemoryStore()
graph = builder.compile(checkpointer=checkpointer, store=store)

# Write to store from outside
store.put(("user", "123"), "preferences", {"theme": "dark"})
```

### Accessing store inside a node

```python
def my_node(state: State, *, store: BaseStore) -> dict:
    memories = store.search(("user", state["user_id"]), query="relevant")
    return {"context": memories}
```

## Common Mistakes

### Wrong: forgetting thread_id

```python
graph.invoke({"messages": [msg]})  # No thread_id — state is not persisted!

# Fix: always pass thread_id
graph.invoke({"messages": [msg]}, config={"configurable": {"thread_id": "123"}})
```

### Wrong: using MemorySaver in production

```python
# MemorySaver is in-memory only — state lost on restart
checkpointer = MemorySaver()  # Fine for dev, not for prod

# Fix: use PostgresSaver or another durable backend
checkpointer = PostgresSaver.from_conn_string(conn_string)
```

## Verification
- Graph is compiled with a checkpointer.
- All `invoke` / `stream` calls include `thread_id` in config.
- Production deployments use a durable checkpointer (not `MemorySaver`).
- Cross-thread data uses a store, not checkpointer state.

## References
- [Persistence Patterns](.devagent/ai_docs/langgraph/persistence.md) — checkpointer API, store API, production setup
- [Core Concepts](.devagent/ai_docs/langgraph/core-concepts.md) — how checkpoints fit into the graph lifecycle

## Related Skills
- `langgraph-fundamentals` — building the graph that persistence wraps
- `langgraph-human-in-the-loop` — HITL requires a checkpointer
