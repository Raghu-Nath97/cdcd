---
description: "Add persistence and memory to existing LangGraph workflows"
mode: "agent"
tools: ["codebase", "search", "edit"]
model: "Claude Sonnet 4.5"
---

# Add Persistence to LangGraph

You are an expert at adding persistence, memory, and state management to LangGraph workflows.

## Your Task

Help the user add persistence capabilities to their LangGraph application:

### 1. Assess Current State

First understand:

-   Does the graph currently use a checkpointer?
-   What type of persistence is needed (conversation memory, cross-thread data, etc.)?
-   What data needs to persist?
-   Is this for development or production?

### 2. Choose Checkpointer

Select the appropriate checkpointer:

**InMemorySaver** - Development/Testing:

-   Fast and simple
-   Data lost when process ends
-   Good for prototyping

**SqliteSaver** - Local/Testing:

-   Persists to disk
-   Single process
-   Good for development and demos

**PostgresSaver** - Production:

-   Scalable persistence
-   Multi-process support
-   Production-ready

**AsyncSaver** - Async Workflows:

-   Use AsyncSqliteSaver or AsyncPostgresSaver
-   Required for ainvoke, astream

### 3. Implementation Steps

#### Basic Checkpointer Setup

```python
# Before (no persistence)
graph = builder.compile()

# After (with persistence)
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)
```

#### SQLite Persistence

```python
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

# Create connection
conn = sqlite3.connect("graph_checkpoints.db")
checkpointer = SqliteSaver(conn)

graph = builder.compile(checkpointer=checkpointer)

# Don't forget to close connection when done
conn.close()
```

#### PostgreSQL Persistence

```python
from langgraph.checkpoint.postgres import PostgresSaver

# Setup (run once)
checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:password@localhost:5432/mydb"
)
checkpointer.setup()  # Creates tables

# Use in graph
graph = builder.compile(checkpointer=checkpointer)
```

#### Async Persistence

```python
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
import aiosqlite

# Create async connection
conn = await aiosqlite.connect("checkpoints.db")
checkpointer = AsyncSqliteSaver(conn)

graph = builder.compile(checkpointer=checkpointer)

# Use with async methods
result = await graph.ainvoke(inputs, config=config)
```

### 4. Thread Management

Update invocation to use threads:

```python
# Before (stateless)
result = graph.invoke({"input": "hello"})

# After (with thread)
config = {"configurable": {"thread_id": "conversation-1"}}
result = graph.invoke({"input": "hello"}, config=config)

# Continue conversation
result = graph.invoke({"input": "follow-up"}, config=config)
```

### 5. Add Memory Store

For cross-thread persistence:

```python
from langgraph.store.memory import InMemoryStore

# Create store
store = InMemoryStore()

# Compile with both checkpointer and store
graph = builder.compile(
    checkpointer=checkpointer,
    store=store
)

# Use in nodes
def node_with_memory(state, config, *, store):
    user_id = config["configurable"]["user_id"]
    namespace = (user_id, "preferences")

    # Store data
    store.put(namespace, "key1", {"value": "data"})

    # Retrieve data
    memories = store.search(namespace)

    return state
```

### 6. Enable Semantic Search

For better memory retrieval:

```python
from langchain.embeddings import init_embeddings

store = InMemoryStore(
    index={
        "embed": init_embeddings("openai:text-embedding-3-small"),
        "dims": 1536,
        "fields": ["$"]  # Embed all fields
    }
)

graph = builder.compile(checkpointer=checkpointer, store=store)

# Search with natural language
memories = store.search(
    namespace,
    query="What are the user's preferences?",
    limit=5
)
```

### 7. State Management Methods

Teach user how to use state methods:

```python
config = {"configurable": {"thread_id": "abc"}}

# Get current state
state = graph.get_state(config)
print(state.values)  # Current state values
print(state.next)    # Next nodes to execute

# Get state history
for checkpoint in graph.get_state_history(config):
    print(f"Step {checkpoint.metadata['step']}: {checkpoint.values}")

# Update state
graph.update_state(config, {"key": "new_value"})

# Update state at specific checkpoint (creates fork)
graph.update_state(
    {"configurable": {"thread_id": "abc", "checkpoint_id": "xyz"}},
    {"key": "value"}
)
```

### 8. Handle Serialization

For complex types:

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

# Enable pickle fallback for unsupported types
checkpointer = InMemorySaver(
    serde=JsonPlusSerializer(pickle_fallback=True)
)
```

For encryption:

```python
import os
from langgraph.checkpoint.serde.encrypted import EncryptedSerializer
from langgraph.checkpoint.sqlite import SqliteSaver

os.environ["LANGGRAPH_AES_KEY"] = "your-secure-key"

serde = EncryptedSerializer.from_pycryptodome_aes()
checkpointer = SqliteSaver(conn, serde=serde)
```

## Common Issues and Solutions

### Issue: State Not Persisting

```python
# ❌ Problem: No checkpointer
graph = builder.compile()

# ✅ Solution: Add checkpointer
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)
```

### Issue: Threads Not Working

```python
# ❌ Problem: Missing thread_id
result = graph.invoke(inputs)

# ✅ Solution: Include thread_id in config
config = {"configurable": {"thread_id": "unique-id"}}
result = graph.invoke(inputs, config=config)
```

### Issue: Memory Not Shared Across Threads

```python
# ❌ Problem: Using checkpointer for cross-thread data
# Checkpointer is per-thread only

# ✅ Solution: Use store for cross-thread data
store = InMemoryStore()
graph = builder.compile(checkpointer=checkpointer, store=store)

# Access same data from different threads
config1 = {"configurable": {"thread_id": "1", "user_id": "user1"}}
config2 = {"configurable": {"thread_id": "2", "user_id": "user1"}}
# Both can access same user memories via store
```

### Issue: Serialization Errors

```python
# ❌ Problem: Complex types not serializable
class State(TypedDict):
    dataframe: pd.DataFrame  # Not JSON serializable

# ✅ Solution: Use pickle fallback or convert
checkpointer = InMemorySaver(
    serde=JsonPlusSerializer(pickle_fallback=True)
)

# Or convert to serializable format
class State(TypedDict):
    dataframe_dict: dict  # Converted from DataFrame
```

## Best Practices

1. **Choose appropriate checkpointer** for your environment
2. **Always include thread_id** when using checkpointers
3. **Use store for cross-thread data** (user preferences, knowledge base)
4. **Enable semantic search** for better memory retrieval
5. **Handle serialization** of custom types properly
6. **Clean up old checkpoints** in production
7. **Use encryption** for sensitive data
8. **Test with InMemorySaver** before production checkpointers
9. **Implement proper error handling** for persistence failures
10. **Document thread_id patterns** for your application

## Migration Checklist

Help user through migration:

-   [ ] Choose checkpointer type
-   [ ] Install required packages (`langgraph-checkpoint-sqlite`, etc.)
-   [ ] Add checkpointer to compilation
-   [ ] Update invocation calls with thread_id
-   [ ] Test basic persistence
-   [ ] Add memory store if needed
-   [ ] Update node signatures to access store
-   [ ] Test cross-thread memory
-   [ ] Add serialization handling if needed
-   [ ] Enable encryption for production
-   [ ] Add state management to UI/API
-   [ ] Test full workflow
-   [ ] Document persistence patterns

## Reference Materials

Use these resources:

-   Persistence concepts: `.devagent/ai_docs/langgraph/persistence.md`
-   Core concepts: `.devagent/ai_docs/langgraph/core-concepts.md`
-   Best practices: `../instructions/langgraph.instructions.md`
-   Expert guidance: `../agents/langgraph.agent.md`

## Deliverables

Provide:

1. **Updated compilation** with checkpointer
2. **Modified invocation** with thread management
3. **Node updates** if using store
4. **Testing examples** to verify persistence
5. **Documentation** of persistence patterns
6. **Migration notes** for production deployment

Guide the user step-by-step through adding persistence to their LangGraph workflow!
