---
name: langgraph-fundamentals
description: 'Build LangGraph StateGraph workflows: define state schemas with TypedDict and Annotated reducers, implement nodes, add edges and conditional routing, use Command for routing with state updates. Use when creating a new StateGraph, defining state schemas, writing node functions, or adding edges.'
---

# LangGraph Fundamentals

## When to use
- Creating a new `StateGraph` workflow
- Defining state schemas with `TypedDict` and `Annotated` reducers
- Writing node functions that return partial state updates
- Adding edges, conditional edges, or `Command`-based routing
- Using `Send` for dynamic parallelization

## Procedure
1. Define a state schema using `TypedDict`. Use `Annotated` with a reducer for any field that accumulates values (lists, messages).
2. Write node functions that accept the state and return a `dict` of partial updates — never mutate state directly.
3. Build the graph with `StateGraph(State)`, add nodes and edges.
4. Compile the graph before invoking: `graph = builder.compile()`.
5. For routing that also updates state, return a `Command` from the node instead of using a separate routing function.

## State Schema Patterns

### Basic state with reducers

```python
from typing import Annotated
from typing_extensions import TypedDict
from operator import add
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]  # Smart message merge
    documents: Annotated[list[str], add]                 # Append-only list
    current_step: str                                    # Default: overwrite
```

### Chat applications — extend MessagesState

```python
from langgraph.graph import MessagesState

class ChatState(MessagesState):  # Predefines messages with add_messages reducer
    user_id: str
    context: dict[str, str]
```

### Input/output schemas for external boundaries

```python
class InputState(TypedDict):
    user_input: str

class OutputState(TypedDict):
    result: str

class InternalState(InputState, OutputState):
    intermediate_data: list[dict]

builder = StateGraph(InternalState, input=InputState, output=OutputState)
```

## Node Patterns

### Basic node — return partial updates

```python
def my_node(state: State) -> dict:
    return {"result": process(state["messages"])}
```

### Node with config access

```python
from langchain_core.runnables import RunnableConfig

def my_node(state: State, config: RunnableConfig) -> dict:
    thread_id = config["configurable"]["thread_id"]
    return {"result": f"processed for {thread_id}"}
```

## Edge & Routing Patterns

### Conditional routing

```python
def route_by_intent(state: State) -> str:
    if "question" in state["messages"][-1].content:
        return "answer"
    return "clarify"

builder.add_conditional_edges("classify", route_by_intent, ["answer", "clarify"])
```

### Command — routing + state update in one step

```python
from langgraph.types import Command

def router_node(state: State) -> Command:
    next_node = determine_next(state)
    return Command(update={"current_step": next_node}, goto=next_node)
```

### Dynamic parallelization with Send

```python
from langgraph.types import Send

def fan_out(state: State) -> list[Send]:
    return [Send("process_item", {"item": item}) for item in state["items"]]

builder.add_conditional_edges("start", fan_out, ["process_item"])
```

## Common Mistakes

### Wrong: mutating state directly

```python
def bad_node(state: State) -> dict:
    state["value"] = "new"  # Don't mutate!
    return state

# Fix: return only the updates
def good_node(state: State) -> dict:
    return {"value": "new"}
```

### Wrong: forgetting reducer on list fields

```python
class BadState(TypedDict):
    messages: list  # Second write overwrites first!

# Fix: use Annotated with a reducer
class GoodState(TypedDict):
    messages: Annotated[list, add_messages]
```

### Wrong: invoking builder instead of compiled graph

```python
builder.invoke(state)  # Error!

# Fix: compile first
graph = builder.compile()
graph.invoke(state)
```

## Verification
- State schema uses `TypedDict` with `Annotated` reducers for accumulating fields.
- Nodes return `dict` — no direct state mutation.
- Graph is compiled before invocation.
- `Command` is used instead of heavy routing functions.

## References
- [Core Concepts](.devagent/ai_docs/langgraph/core-concepts.md) — StateGraph, nodes, edges, reducers, Command, Send
- [Agent Architectures](.devagent/ai_docs/langgraph/agent-architectures.md) — supervisor, swarm, multi-agent
- [Examples Library](.devagent/ai_docs/langgraph/examples.md) — end-to-end workflow samples

## Related Skills
- `langgraph-persistence` — adding checkpointers and memory stores
- `langgraph-human-in-the-loop` — adding interrupts and approval gates
- `reviewing-python-code` — Python coding standards in agent code
