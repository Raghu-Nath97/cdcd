---
name: langgraph-human-in-the-loop
description: 'Add LangGraph human-in-the-loop patterns: configure interrupt_before/interrupt_after for approval gates, implement review steps, resume interrupted graphs with Command. Use when adding human approval before sensitive actions, implementing review gates, or resuming paused workflows.'
---

# LangGraph Human-in-the-Loop

## When to use
- Adding human approval before a sensitive or irreversible action
- Implementing a review gate where a human edits or confirms agent output
- Resuming a paused graph after human input
- Debugging why an interrupt is not firing or resume is failing

## Procedure
1. Ensure the graph has a checkpointer — HITL requires persistence.
2. Add `interrupt_before=["node_name"]` or `interrupt_after=["node_name"]` to `builder.compile()`.
3. Invoke the graph; it will pause at the interrupt point and return partial state.
4. Collect human input externally (UI, CLI, API).
5. Resume with `graph.invoke(Command(resume=value), config={"configurable": {"thread_id": "..."}})`.

## Static Interrupts

### Interrupt before a node

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
graph = builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["sensitive_action"]
)

# First invoke — pauses before sensitive_action
result = graph.invoke(
    {"messages": [HumanMessage("Delete all records")]},
    config={"configurable": {"thread_id": "review-123"}}
)
# result contains state up to the interrupt point
```

### Resume after approval

```python
from langgraph.types import Command

# Human reviewed and approved — resume
graph.invoke(
    Command(resume=True),
    config={"configurable": {"thread_id": "review-123"}}
)
```

### Resume with edited input

```python
# Human edited the proposed action before approving
graph.invoke(
    Command(resume={"approved": True, "modified_query": "Delete inactive records only"}),
    config={"configurable": {"thread_id": "review-123"}}
)
```

## Dynamic Interrupts

Use `interrupt()` inside a node for conditional pauses:

```python
from langgraph.types import interrupt

def sensitive_node(state: State) -> dict:
    if state["risk_score"] > 0.8:
        human_input = interrupt("High risk detected. Approve? (yes/no)")
        if human_input != "yes":
            return {"status": "rejected"}
    return {"status": "approved", "result": execute_action(state)}
```

## Common Mistakes

### Wrong: no checkpointer with interrupts

```python
graph = builder.compile(interrupt_before=["review"])  # No checkpointer!
# Graph cannot pause/resume without persistence

# Fix: always add a checkpointer
graph = builder.compile(checkpointer=checkpointer, interrupt_before=["review"])
```

### Wrong: forgetting thread_id on resume

```python
graph.invoke(Command(resume=True))  # No thread_id — cannot find paused state

# Fix: use the same thread_id from the initial invoke
graph.invoke(Command(resume=True), config={"configurable": {"thread_id": "123"}})
```

## Verification
- Graph is compiled with both a checkpointer and interrupt configuration.
- Resume calls use the same `thread_id` as the original invoke.
- Dynamic interrupts handle both approval and rejection paths.
- Sensitive actions are gated behind an interrupt.

## References
- [Human-in-the-Loop Patterns](.devagent/ai_docs/langgraph/human-in-the-loop.md) — static interrupts, dynamic interrupts, review patterns
- [Persistence Patterns](.devagent/ai_docs/langgraph/persistence.md) — checkpointer setup required for HITL

## Related Skills
- `langgraph-persistence` — checkpointer setup that HITL depends on
- `langgraph-fundamentals` — building the graph structure
