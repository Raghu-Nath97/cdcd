---
name: building-langgraph-agents
description: 'Builds LangGraph stateful agent workflows. Use when creating StateGraph workflows, defining state schemas, implementing nodes, adding checkpointers, designing multi-agent systems, or debugging graph execution.'
---

# LangGraph Agent Development

This skill has been split into focused skills for better activation. Use the specific skill that matches your task:

| Task | Skill |
|------|-------|
| Creating graphs, state schemas, nodes, edges, routing | `langgraph-fundamentals` |
| Adding checkpointers, memory stores, state persistence | `langgraph-persistence` |
| Adding human approval, interrupts, resume flows | `langgraph-human-in-the-loop` |

## Quick Start

```python
from langgraph.graph import StateGraph, START, END, MessagesState

class State(MessagesState):
    result: str

def process(state: State) -> dict:
    return {"result": "processed"}

builder = StateGraph(State)
builder.add_node("process", process)
builder.add_edge(START, "process")
builder.add_edge("process", END)

graph = builder.compile()
result = graph.invoke({"messages": [], "result": ""})
```

## Decision Guide

| Need | Solution | Reference |
|------|----------|-----------|
| Basic workflow | `StateGraph` + nodes + edges | [Core Concepts](.devagent/ai_docs/langgraph/core-concepts.md) |
| Chat application | Extend `MessagesState` | [Core Concepts](.devagent/ai_docs/langgraph/core-concepts.md) |
| Routing + state update | Use `Command` | [Core Concepts](.devagent/ai_docs/langgraph/core-concepts.md) |
| Conversation memory | Add checkpointer | [Persistence](.devagent/ai_docs/langgraph/persistence.md) |
| Human approval | `interrupt_before` | [Human-in-the-Loop](.devagent/ai_docs/langgraph/human-in-the-loop.md) |
| Multi-agent design | Supervisor or swarm pattern | [Agent Architectures](.devagent/ai_docs/langgraph/agent-architectures.md) |

## References
- [Core Concepts](.devagent/ai_docs/langgraph/core-concepts.md)
- [Persistence Patterns](.devagent/ai_docs/langgraph/persistence.md)
- [Agent Architectures](.devagent/ai_docs/langgraph/agent-architectures.md)
- [Human-in-the-Loop](.devagent/ai_docs/langgraph/human-in-the-loop.md)
- [Examples Library](.devagent/ai_docs/langgraph/examples.md)

## Related Skills
- `langgraph-fundamentals` — state schemas, nodes, edges, routing
- `langgraph-persistence` — checkpointers and memory stores
- `langgraph-human-in-the-loop` — interrupts and approval gates
- `developing-pyrogai-pipelines` — deploying LangGraph agents on PyrogAI
- `reviewing-python-code` — Python coding standards in agent code
