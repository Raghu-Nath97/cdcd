# LangChain Memory and State Management

Guide to managing conversation history, state, and long-term memory in LangChain agents.

## Table of Contents
1. [Short-Term Memory](#short-term-memory)
2. [Long-Term Memory](#long-term-memory)
3. [Custom State](#custom-state)
4. [State Updates](#state-updates)
5. [Production Patterns](#production-patterns)

---

## Short-Term Memory

Short-term memory stores conversation history for the current session.

### Basic Memory with Checkpointer

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# Create memory checkpointer
checkpointer = InMemorySaver()

agent = create_agent(
    model="openai:gpt-4o",
    tools=[],
    checkpointer=checkpointer
)

# First conversation
config = {"configurable": {"thread_id": "user123"}}

agent.invoke(
    {"messages": [{"role": "user", "content": "My name is Alice"}]},
    config=config
)

# Continue conversation (remembers context)
agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    config=config  # Same thread_id
)
# Response: "Your name is Alice"
```

### Persistent Memory (Production)

```python
from langgraph.checkpoint.postgres import PostgresSaver

# Use database for persistence
checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:pass@localhost/db"
)

agent = create_agent(
    model="anthropic:claude-sonnet-4-5",
    tools=[search_tool],
    checkpointer=checkpointer
)
```

### Memory Management

```python
# Clear conversation history
from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES

agent.invoke(
    {"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES)]},
    config=config
)

# Remove specific messages
agent.invoke(
    {"messages": [RemoveMessage(id="message_id_123")]},
    config=config
)
```

---

## Long-Term Memory

Long-term memory persists across sessions using a key-value store.

### Using InMemoryStore

```python
from langgraph.store.memory import InMemoryStore
from langchain.tools import tool, ToolRuntime

store = InMemoryStore()

@tool
def save_preference(
    key: str,
    value: str,
    runtime: ToolRuntime
) -> str:
    """Save user preference."""
    user_id = runtime.context.get("user_id", "default")
    
    # Store preference
    runtime.store.put(
        namespace=("preferences", user_id),
        key=key,
        value={"setting": value}
    )
    
    return f"Saved {key} = {value}"

@tool
def get_preference(
    key: str,
    runtime: ToolRuntime
) -> str:
    """Retrieve user preference."""
    user_id = runtime.context.get("user_id", "default")
    
    # Get preference
    item = runtime.store.get(
        namespace=("preferences", user_id),
        key=key
    )
    
    if item:
        return f"{key}: {item.value['setting']}"
    return f"No preference for {key}"

agent = create_agent(
    model="openai:gpt-4o",
    tools=[save_preference, get_preference],
    store=store
)
```

### Persistent Store (Production)

```python
from langgraph.store.postgres import PostgresStore

# Use database for long-term memory
store = PostgresStore.from_conn_string(
    "postgresql://user:pass@localhost/db"
)

agent = create_agent(
    model="openai:gpt-4o",
    tools=[memory_tools],
    store=store
)
```

### Searching Memory

```python
@tool
def search_memories(
    query: str,
    runtime: ToolRuntime
) -> str:
    """Search user's memories."""
    user_id = runtime.context.get("user_id")
    
    # Search in namespace
    items = runtime.store.search(
        namespace=("memories", user_id),
        # Can add filters/limits here
    )
    
    results = [f"{item.key}: {item.value}" for item in items]
    return "\n".join(results) if results else "No memories found"
```

---

## Custom State

Extend agent state to store custom data.

### Defining Custom State

```python
from typing import TypedDict
from langchain.agents import AgentState

class CustomAgentState(AgentState):
    """Extended agent state."""
    user_name: str
    user_score: int
    preferences: dict
    session_data: dict
```

### Using Custom State

```python
agent = create_agent(
    model="openai:gpt-4o",
    tools=[score_tool],
    state_schema=CustomAgentState
)

# Initialize with custom state
result = agent.invoke({
    "messages": [{"role": "user", "content": "Hello"}],
    "user_name": "Alice",
    "user_score": 0,
    "preferences": {},
    "session_data": {}
})
```

### Accessing State in Tools

```python
@tool
def get_user_info(runtime: ToolRuntime) -> str:
    """Get current user information."""
    state = runtime.state
    
    name = state.get("user_name", "Guest")
    score = state.get("user_score", 0)
    
    return f"User: {name}, Score: {score}"
```

---

## State Updates

Update state during agent execution.

### Using Command

```python
from langgraph.types import Command

@tool
def add_points(
    points: int,
    runtime: ToolRuntime
) -> Command:
    """Add points to user score."""
    current_score = runtime.state.get("user_score", 0)
    new_score = current_score + points
    
    return Command(
        update={"user_score": new_score},
        message=f"Added {points} points. New score: {new_score}"
    )

@tool
def update_preference(
    key: str,
    value: str,
    runtime: ToolRuntime
) -> Command:
    """Update user preference in state."""
    prefs = runtime.state.get("preferences", {})
    prefs[key] = value
    
    return Command(
        update={"preferences": prefs},
        message=f"Updated {key} = {value}"
    )
```

### Conditional Updates

```python
@tool
def award_achievement(
    achievement: str,
    runtime: ToolRuntime
) -> Command:
    """Award achievement if eligible."""
    score = runtime.state.get("user_score", 0)
    
    if score >= 100:
        return Command(
            update={"achievements": [achievement]},
            message=f"Achievement unlocked: {achievement}!"
        )
    else:
        return f"Need {100 - score} more points for this achievement"
```

---

## Production Patterns

### Multi-User Support

```python
from typing import TypedDict

class UserContext(TypedDict):
    user_id: str
    session_id: str

def get_user_config(user_id: str, session_id: str):
    """Generate config for user session."""
    return {
        "configurable": {
            "thread_id": f"{user_id}_{session_id}"
        }
    }

# Per-user conversations
user1_config = get_user_config("alice", "session1")
user2_config = get_user_config("bob", "session1")

# Separate conversation histories
agent.invoke({"messages": [...]}, config=user1_config)
agent.invoke({"messages": [...]}, config=user2_config)
```

### Session Expiry

```python
from datetime import datetime, timedelta

@tool
def check_session_validity(runtime: ToolRuntime) -> str:
    """Check if session is still valid."""
    session_data = runtime.state.get("session_data", {})
    start_time = session_data.get("start_time")
    
    if not start_time:
        # New session
        from langgraph.types import Command
        return Command(
            update={
                "session_data": {
                    "start_time": datetime.now().isoformat()
                }
            },
            message="Session started"
        )
    
    # Check expiry
    start = datetime.fromisoformat(start_time)
    if datetime.now() - start > timedelta(hours=1):
        return "Session expired. Please start a new session."
    
    return "Session valid"
```

### State Persistence

```python
import json
from pathlib import Path

class FileCheckpointer:
    """Simple file-based checkpointer for development."""
    
    def __init__(self, base_path: str = "./checkpoints"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
    
    def save(self, thread_id: str, state: dict):
        """Save state to file."""
        file_path = self.base_path / f"{thread_id}.json"
        with open(file_path, 'w') as f:
            json.dump(state, f)
    
    def load(self, thread_id: str) -> dict:
        """Load state from file."""
        file_path = self.base_path / f"{thread_id}.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        return {}
```

### Memory Optimization

```python
@tool
def summarize_conversation(runtime: ToolRuntime) -> Command:
    """Summarize and compress old messages."""
    messages = runtime.state["messages"]
    
    if len(messages) > 20:
        # Keep only recent messages + summary
        old_messages = messages[:-10]
        recent_messages = messages[-10:]
        
        # Generate summary (using LLM)
        summary = f"Previous conversation summary: [...]"
        
        from langchain.messages import SystemMessage
        new_messages = [
            SystemMessage(summary),
            *recent_messages
        ]
        
        return Command(
            update={"messages": new_messages},
            message="Conversation summarized to save memory"
        )
    
    return "No summarization needed"
```

---

## Best Practices

1. **Use thread_id**: Unique ID per conversation/user
2. **Persistent storage**: Use database checkpointers in production
3. **Memory limits**: Implement message truncation/summarization
4. **Namespace data**: Use namespaces in stores for organization
5. **Clean up**: Regularly purge old sessions/data
6. **State immutability**: Don't mutate state directly; use Command
7. **Default values**: Always provide defaults when accessing state
8. **Session validation**: Check session validity in long-running apps
9. **Error handling**: Handle missing/corrupted state gracefully
10. **Monitor size**: Track memory usage and storage costs

---

## Production Example

Tracking batch processing state:

```python
class BatchState(AgentState):
    """State for batch processing."""
    total_items: int
    processed_items: int
    failed_items: int
    results: list[dict]

@tool
def process_item(
    item: str,
    runtime: ToolRuntime
) -> Command:
    """Process item and update state."""
    processed = runtime.state.get("processed_items", 0)
    results = runtime.state.get("results", [])
    
    try:
        # Process item
        result = {"item": item, "status": "success"}
        results.append(result)
        
        return Command(
            update={
                "processed_items": processed + 1,
                "results": results
            },
            message=f"Processed: {item}"
        )
    except Exception as e:
        failed = runtime.state.get("failed_items", 0)
        return Command(
            update={
                "processed_items": processed + 1,
                "failed_items": failed + 1
            },
            message=f"Failed: {item}"
        )
```

---

## Integration with NileGPT

Example: Tracking batch processing state

```python
class BatchState(AgentState):
    """State for batch processing."""
    total_items: int
    processed_items: int
    failed_items: int
    results: list[dict]

@tool
def process_item(
    item: str,
    runtime: ToolRuntime
) -> Command:
    """Process item and update state."""
    processed = runtime.state.get("processed_items", 0)
    results = runtime.state.get("results", [])
    
    try:
        # Process item
        result = {"item": item, "status": "success"}
        results.append(result)
        
        return Command(
            update={
                "processed_items": processed + 1,
                "results": results
            },
            message=f"Processed: {item}"
        )
    except Exception as e:
        failed = runtime.state.get("failed_items", 0)
        return Command(
            update={
                "processed_items": processed + 1,
                "failed_items": failed + 1
            },
            message=f"Failed: {item}"
        )
```
