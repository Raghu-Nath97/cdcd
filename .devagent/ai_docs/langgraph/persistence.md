# LangGraph Persistence Patterns

## Overview

LangGraph's persistence layer enables stateful workflows through checkpointers. Checkpoints save graph state at each super-step, enabling memory, human-in-the-loop, time travel, and fault-tolerance.

## Checkpointers

### Types of Checkpointers

**InMemorySaver** - For development and testing:

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)
```

**SqliteSaver** - For local persistence:

```python
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

conn = sqlite3.connect("checkpoints.db")
checkpointer = SqliteSaver(conn)
graph = builder.compile(checkpointer=checkpointer)
```

**PostgresSaver** - For production:

```python
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:pass@localhost/db"
)
checkpointer.setup()  # Create tables
graph = builder.compile(checkpointer=checkpointer)
```

### Async Checkpointers

For async graph execution:

```python
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

# Use with ainvoke, astream, etc.
checkpointer = AsyncSqliteSaver(...)
result = await graph.ainvoke(inputs, config)
```

## Threads

Threads are unique identifiers for conversation/execution sessions.

### Basic Thread Usage

```python
# Create a thread
config = {"configurable": {"thread_id": "conversation-123"}}

# First interaction
result = graph.invoke({"messages": [user_msg]}, config=config)

# Continue the conversation
result = graph.invoke({"messages": [follow_up_msg]}, config=config)
```

### Multiple Threads

```python
# Different conversations with same user
thread_1 = {"configurable": {"thread_id": "chat-1"}}
thread_2 = {"configurable": {"thread_id": "chat-2"}}

graph.invoke({"messages": [msg1]}, config=thread_1)
graph.invoke({"messages": [msg2]}, config=thread_2)
```

## Checkpoints

Checkpoints are snapshots of graph state at specific points.

### StateSnapshot Structure

```python
StateSnapshot(
    values={'messages': [...], 'context': {...}},
    next=('next_node',),  # Next nodes to execute
    config={'configurable': {'thread_id': '1', 'checkpoint_id': '...'}},
    metadata={'source': 'loop', 'writes': {...}, 'step': 2},
    created_at='2024-08-29T19:19:38.821749+00:00',
    parent_config={...},  # Previous checkpoint
    tasks=(...)  # Pending tasks
)
```

### Get Current State

```python
# Get latest state
config = {"configurable": {"thread_id": "1"}}
state = graph.get_state(config)

print(state.values)  # Current state
print(state.next)    # Next nodes to run
```

### Get State History

```python
# Get all checkpoints in chronological order (newest first)
history = list(graph.get_state_history(config))

for checkpoint in history:
    print(f"Step {checkpoint.metadata['step']}")
    print(f"State: {checkpoint.values}")
    print(f"Next: {checkpoint.next}")
```

### Replay from Checkpoint

Replay execution from a specific checkpoint:

```python
# Resume from specific checkpoint
config = {
    "configurable": {
        "thread_id": "1",
        "checkpoint_id": "0c62ca34-ac19-445d-bbb0-5b4984975b2a"
    }
}

# Steps before checkpoint_id are replayed (not re-executed)
# Steps after checkpoint_id are executed (creating a fork)
result = graph.invoke(None, config=config)
```

### Update State

Manually modify graph state:

```python
# Update current state
graph.update_state(
    config,
    {"messages": [new_message], "context": {"updated": True}}
)

# Update state at specific checkpoint (creates fork)
config_with_checkpoint = {
    "configurable": {
        "thread_id": "1",
        "checkpoint_id": "abc123..."
    }
}
graph.update_state(config_with_checkpoint, updates)

# Update as if from specific node
graph.update_state(config, updates, as_node="node_name")
```

**Important:** Updates use reducers! If a channel has a reducer (like `add`), the update is combined with existing value, not replaced.

## Memory Store

Store data across threads (e.g., user preferences, long-term memory).

### Basic Store Usage

```python
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()
graph = builder.compile(checkpointer=checkpointer, store=store)
```

### Storing and Retrieving Data

```python
import uuid
from langgraph.store.base import BaseStore
from langchain_core.runnables import RunnableConfig

def node_with_memory(
    state: State,
    config: RunnableConfig,
    *,
    store: BaseStore
) -> dict:
    user_id = config["configurable"]["user_id"]
    namespace = (user_id, "memories")
    
    # Store a memory
    memory_id = str(uuid.uuid4())
    store.put(namespace, memory_id, {
        "preference": "dark mode",
        "timestamp": "2024-01-01"
    })
    
    # Retrieve all memories for user
    memories = store.search(namespace)
    
    # Access memory values
    for memory in memories:
        print(memory.value)  # {"preference": "dark mode", ...}
        print(memory.key)    # memory_id
        print(memory.namespace)  # (user_id, "memories")
    
    return state
```

### Semantic Search

Enable semantic search with embeddings:

```python
from langchain.embeddings import init_embeddings

store = InMemoryStore(
    index={
        "embed": init_embeddings("openai:text-embedding-3-small"),
        "dims": 1536,
        "fields": ["preference", "$"]  # Fields to embed
    }
)

# Semantic search
memories = store.search(
    namespace=(user_id, "memories"),
    query="What does the user prefer?",
    limit=3
)
```

### Store with Selective Embedding

```python
# Store with specific fields to embed
store.put(
    namespace,
    memory_id,
    {"preference": "Italian food", "metadata": "User feedback"},
    index=["preference"]  # Only embed this field
)

# Store without embedding
store.put(
    namespace,
    memory_id,
    {"system_info": "Internal data"},
    index=False
)
```

### Using Store in Graph

```python
# Invoke with user context
config = {
    "configurable": {
        "thread_id": "conversation-1",
        "user_id": "user-123"
    }
}

result = graph.invoke(inputs, config=config)

# Store persists across different threads for same user
config_new_thread = {
    "configurable": {
        "thread_id": "conversation-2",  # Different thread
        "user_id": "user-123"            # Same user
    }
}
# Can still access same memories
```

## Serialization

### Custom Serializers

By default, checkpointers use `JsonPlusSerializer`. For unsupported types:

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

# Enable pickle fallback for complex types (e.g., Pandas DataFrames)
checkpointer = InMemorySaver(
    serde=JsonPlusSerializer(pickle_fallback=True)
)
```

### Encryption

Encrypt persisted state:

```python
import os
from langgraph.checkpoint.serde.encrypted import EncryptedSerializer
from langgraph.checkpoint.sqlite import SqliteSaver

# Set encryption key
os.environ["LANGGRAPH_AES_KEY"] = "your-32-byte-key"

# Create encrypted checkpointer
serde = EncryptedSerializer.from_pycryptodome_aes()
checkpointer = SqliteSaver(conn, serde=serde)
```

## Use Cases

### Conversation Memory

```python
from langgraph.graph import MessagesState

class ChatState(MessagesState):
    user_id: str

builder = StateGraph(ChatState)
# ... add nodes

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# Persistent conversation
config = {"configurable": {"thread_id": "chat-123"}}

# First message
graph.invoke({"messages": [{"role": "user", "content": "Hi"}]}, config)

# Follow-up (has context from first message)
graph.invoke({"messages": [{"role": "user", "content": "What did I say?"}]}, config)
```

### User Preferences Across Sessions

```python
store = InMemoryStore()
graph = builder.compile(checkpointer=checkpointer, store=store)

def preferences_node(state, config, *, store):
    user_id = config["configurable"]["user_id"]
    namespace = (user_id, "preferences")
    
    # First session: Store preference
    store.put(namespace, "theme", {"value": "dark"})
    
    # Any session: Retrieve preference
    prefs = store.search(namespace)
    theme = prefs[0].value["value"] if prefs else "light"
    
    return {"theme": theme}
```

### Time Travel and Debugging

```python
# Get full execution history
history = list(graph.get_state_history(config))

# Inspect state at each step
for i, checkpoint in enumerate(history):
    print(f"Step {i}: {checkpoint.values}")
    
# Fork from specific point
fork_config = {
    "configurable": {
        "thread_id": "original",
        "checkpoint_id": history[5].config["configurable"]["checkpoint_id"]
    }
}
# Resume execution with different inputs
result = graph.invoke(new_inputs, config=fork_config)
```

### Fault Tolerance

```python
def may_fail_node(state):
    if random.random() < 0.5:
        raise Exception("Node failed!")
    return {"result": "success"}

builder.add_node("risky", may_fail_node)
graph = builder.compile(checkpointer=checkpointer)

try:
    result = graph.invoke(inputs, config=config)
except Exception as e:
    # Graph state is saved at last successful checkpoint
    # Can resume from where it left off
    state = graph.get_state(config)
    print(f"Failed at step {state.metadata['step']}")
    
    # Retry or modify state and resume
    graph.update_state(config, {"retry": True})
    result = graph.invoke(None, config=config)
```

## Best Practices

1. **Always use checkpointers** for stateful workflows
2. **Use meaningful thread_ids** (e.g., user-id + session-id)
3. **Use store for cross-thread data** (user preferences, knowledge)
4. **Enable semantic search** for better memory retrieval
5. **Use encryption** for sensitive data in production
6. **Clean up old checkpoints** to manage storage
7. **Test with InMemorySaver** before production checkpointers
8. **Use async checkpointers** with async graph execution
9. **Leverage state history** for debugging and auditing
10. **Consider reducers** when updating state manually

## Configuration in Production

For LangGraph Platform, configure in `langgraph.json`:

```json
{
  "store": {
    "index": {
      "embed": "openai:text-embeddings-3-small",
      "dims": 1536,
      "fields": ["$"]
    }
  }
}
```

This enables automatic semantic search without manual configuration.
