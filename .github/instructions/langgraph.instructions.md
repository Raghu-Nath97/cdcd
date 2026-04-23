---
name: 'LangGraph Standards'
description: 'LangGraph coding standards and best practices'
applyTo: '**/*.py'
---

# LangGraph Coding Standards

These constraints apply when code imports from `langgraph`. For procedural guidance, see skills and ai_docs.

## Non-Negotiable Constraints

1. **Return state updates as dicts** — never mutate state directly; nodes return partial dicts
2. **Use `MessagesState`** for chat applications — it includes the `add_messages` reducer
3. **Add a checkpointer** for any stateful workflow — enables memory, HITL, and fault-tolerance
4. **Use `Command`** to combine routing and state updates in one node — avoids heavy routing functions
5. **Use type hints** for all state schemas and `Command` returns — `TypedDict` with `Annotated` reducers
6. **Compile the graph** before invoking — call `builder.compile()`, never `builder.invoke()`

## Additional Resources

- **Skills**: `langgraph-fundamentals`, `langgraph-persistence`, `langgraph-human-in-the-loop`
- **Deep reference**: `.devagent/ai_docs/langgraph/` (core concepts, persistence, architectures, human-in-the-loop, examples)
- **Expert assistance**: `../agents/langgraph.agent.md`
- **Official docs**: https://langchain-ai.github.io/langgraph/
