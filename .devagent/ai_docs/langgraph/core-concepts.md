# LangGraph Core Concepts

## Overview

LangGraph is a low-level orchestration framework for building stateful, long-running agent workflows. It models workflows as graphs with nodes (Python functions) and edges (control flow).

## Graph Components

### StateGraph

The main graph class parameterized by a state schema:

```python
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

class State(TypedDict):
    messages: list
    user_input: str
    result: str

builder = StateGraph(State)
```

### State Schema

Define state using TypedDict, dataclass, or Pydantic BaseModel:

```python
from typing import Annotated
from typing_extensions import TypedDict
from operator import add

class State(TypedDict):
    # Default reducer: override
    foo: int
    # Custom reducer: append
    bar: Annotated[list[str], add]
```

**Key Points:**

- State schema defines channels (keys) and their types
- Each channel can have a reducer function
- Default reducer overwrites the value
- Custom reducers (like `add`) combine values

### Reducers

Reducers control how node updates are applied to state:

```python
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class State(TypedDict):
    # Default reducer: replace value
    counter: int
    # Add reducer: append to list
    items: Annotated[list[str], add]
    # Message reducer: smart message handling
    messages: Annotated[list[AnyMessage], add_messages]
```

The `add_messages` reducer:

- Appends new messages
- Updates existing messages by ID
- Handles message serialization/deserialization

### MessagesState

Prebuilt state for chat applications:

```python
from langgraph.graph import MessagesState

# Predefined with messages channel
class MyState(MessagesState):
    user_id: str
    context: dict
```

Equivalent to:

```python
class MyState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user_id: str
    context: dict
```

## Nodes

Nodes are Python functions that process state:

```python
def my_node(state: State) -> dict:
    """Process state and return updates."""
    return {"result": process(state["user_input"])}
```

**Node Signatures:**

- `state`: Required - the graph state
- `config`: Optional - RunnableConfig with thread_id, tags, etc.
- `runtime`: Optional - Runtime context
- `store`: Optional - Memory store access

**Full Node Example:**

```python
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from langgraph.store.base import BaseStore

def my_node(
    state: State,
    config: RunnableConfig,
    *,
    runtime: Runtime,
    store: BaseStore
) -> dict:
    thread_id = config["configurable"]["thread_id"]
    user_context = runtime.context.user_id
    memories = store.search((user_context, "memories"))
    
    return {"result": "processed"}
```

**Special Nodes:**

- `START`: Virtual node for entry point
- `END`: Virtual node for termination

## Edges

Edges define control flow between nodes.

### Normal Edges

Direct transitions between nodes:

```python
from langgraph.graph import START, END

builder.add_edge(START, "node_a")
builder.add_edge("node_a", "node_b")
builder.add_edge("node_b", END)
```

### Conditional Edges

Dynamic routing based on state:

```python
def routing_function(state: State) -> str:
    return "node_b" if state["condition"] else "node_c"

builder.add_conditional_edges("node_a", routing_function)

# With explicit mapping
builder.add_conditional_edges(
    "node_a",
    routing_function,
    {True: "node_b", False: "node_c"}
)
```

### Entry Points

Define where graph execution starts:

```python
# Fixed entry point
builder.add_edge(START, "first_node")

# Conditional entry point
def entry_routing(state: State) -> str:
    return "node_a" if state["use_a"] else "node_b"

builder.add_conditional_edges(START, entry_routing)
```

## Command

Combine state updates and routing in a single node:

```python
from typing import Literal
from langgraph.types import Command

def my_node(state: State) -> Command[Literal["next_node", "END"]]:
    # Process and route
    result = process(state)
    
    if result.success:
        return Command(
            update={"result": result.value},
            goto="next_node"
        )
    return Command(goto="END")
```

**When to Use Command:**

- Need to both update state AND route
- Implementing agent handoffs
- Conditional routing with state changes

**Type Annotations Required:**

```python
# Must specify possible next nodes
Command[Literal["node_a", "node_b", "END"]]
```

## Send API

Enable dynamic parallelization (map-reduce patterns):

```python
from langgraph.types import Send

def fan_out(state: State) -> list[Send]:
    # Create parallel executions
    return [
        Send("process_item", {"item": item})
        for item in state["items"]
    ]

builder.add_conditional_edges("fan_out", fan_out)
```

**Use Cases:**

- Map-reduce workflows
- Process unknown number of items in parallel
- Dynamic workflow generation

## Graph Compilation

Compile the graph before execution:

```python
# Basic compilation
graph = builder.compile()

# With checkpointer for persistence
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# With interrupts for human-in-the-loop
graph = builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["critical_node"],
    interrupt_after=["review_node"]
)
```

## Execution

### Invoke

Synchronous execution:

```python
result = graph.invoke(
    {"user_input": "Hello"},
    config={"configurable": {"thread_id": "1"}}
)
```

### Stream

Stream intermediate results:

```python
for chunk in graph.stream(
    {"user_input": "Hello"},
    config={"configurable": {"thread_id": "1"}},
    stream_mode="updates"  # or "values", "messages", "events"
):
    print(chunk)
```

**Stream Modes:**

- `values`: Full state after each step
- `updates`: Only state updates from each node
- `messages`: Only message updates
- `events`: All internal events

### Async Execution

```python
result = await graph.ainvoke(inputs, config=config)

async for chunk in graph.astream(inputs, config=config):
    print(chunk)
```

## Runtime Context

Pass runtime dependencies to nodes:

```python
from dataclasses import dataclass

@dataclass
class Context:
    llm_provider: str
    database_url: str

builder = StateGraph(State, context_schema=Context)
graph = builder.compile()

# Pass context at runtime
result = graph.invoke(
    inputs,
    context={"llm_provider": "openai", "database_url": "..."}
)
```

Access in nodes:

```python
def my_node(state: State, runtime: Runtime[Context]) -> dict:
    provider = runtime.context.llm_provider
    return {"result": "..."}
```

## Recursion Limit

Control maximum graph execution steps:

```python
result = graph.invoke(
    inputs,
    config={"recursion_limit": 50}  # Default is 25
)
```

## Visualization

Generate graph visualizations:

```python
# Mermaid diagram
from IPython.display import Image, display
display(Image(graph.get_graph().draw_mermaid_png()))

# ASCII representation
print(graph.get_graph().draw_ascii())
```

## Multiple Schemas

Use different schemas for input, output, and internal state:

```python
class InputState(TypedDict):
    user_input: str

class OutputState(TypedDict):
    result: str

class InternalState(TypedDict):
    user_input: str
    result: str
    intermediate: list

builder = StateGraph(
    InternalState,
    input_schema=InputState,
    output_schema=OutputState
)
```

## Node Caching

Cache expensive node computations:

```python
from langgraph.types import CachePolicy
from langgraph.cache.memory import InMemoryCache

builder.add_node(
    "expensive_node",
    expensive_function,
    cache_policy=CachePolicy(ttl=300)  # 5 minutes
)

graph = builder.compile(cache=InMemoryCache())
```

## Best Practices

1. **Always use type hints** for state schemas
2. **Choose appropriate reducers** for each state channel
3. **Use MessagesState** for chat applications
4. **Return updates, don't mutate state** in nodes
5. **Compile before execution** - it's required!
6. **Use Command** to combine routing and updates
7. **Visualize complex graphs** to understand flow
8. **Add proper error handling** in nodes
9. **Test nodes independently** before graph integration
10. **Use descriptive node names** for maintainability
