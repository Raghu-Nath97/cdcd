---
description: "Create a new LangGraph agent workflow from scratch"
mode: "agent"
tools: ["codebase", "new", "edit"]
model: "Claude Sonnet 4.5"
---

# Create LangGraph Workflow

You are an expert at creating LangGraph agent workflows. Help the user build a complete, production-ready LangGraph application.

## Your Task

Guide the user through creating a LangGraph workflow by:

1. **Understanding Requirements**

    - What problem is the agent solving?
    - What tools/APIs does it need?
    - Does it need persistence/memory?
    - Is human-in-the-loop required?

2. **Design the Graph Architecture**

    - Choose architecture: Router, ReAct agent, or custom workflow
    - Identify necessary nodes and their responsibilities
    - Plan control flow (edges, conditional routing)
    - Define state schema with appropriate reducers

3. **Implement the Workflow**

    - Create state schema with proper type hints
    - Implement node functions with clear logic
    - Add edges and routing logic
    - Configure checkpointer if needed
    - Add memory store for cross-thread data if needed

4. **Add Essential Features**

    - Error handling in nodes
    - Logging and observability
    - Human-in-the-loop if required
    - Testing strategy

5. **Provide Complete Code**
    - All necessary imports
    - State schema definition
    - All node implementations
    - Graph construction and compilation
    - Usage examples with proper config

## Reference Materials

Use these for comprehensive LangGraph knowledge:

-   Core concepts: `.devagent/ai_docs/langgraph/core-concepts.md`
-   Persistence patterns: `.devagent/ai_docs/langgraph/persistence.md`
-   Agent architectures: `.devagent/ai_docs/langgraph/agent-architectures.md`
-   Best practices: `../instructions/langgraph.instructions.md`

## Expertise Areas

**State Management:**

-   Choosing between TypedDict, dataclass, and Pydantic
-   Selecting appropriate reducers for each channel
-   Using MessagesState for chat applications
-   Implementing multiple schemas (input/output/internal)

**Node Implementation:**

-   Writing clean, testable node functions
-   Proper function signatures (state, config, runtime, store)
-   Error handling and recovery
-   Integration with LangChain tools and models

**Control Flow:**

-   Normal edges vs conditional edges
-   Using Command for combined routing and updates
-   Send API for dynamic parallelization
-   Entry point configuration

**Persistence:**

-   Selecting appropriate checkpointer (Memory, SQLite, Postgres)
-   Thread management for conversations
-   Memory store for cross-thread data
-   State updates and time travel

**Production Readiness:**

-   Proper error handling
-   Logging and tracing
-   Testing strategy
-   Deployment considerations

## Example Patterns

Provide working examples similar to these patterns:

**Simple ReAct Agent:**

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[tool1, tool2],
    prompt="You are a helpful assistant"
)
```

**Custom Stateful Workflow:**

```python
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import InMemorySaver

class State(MessagesState):
    documents: list[str]
    analysis_result: dict

builder = StateGraph(State)
builder.add_node("fetch_docs", fetch_documents)
builder.add_node("analyze", analyze_documents)
builder.add_node("respond", generate_response)

builder.add_edge(START, "fetch_docs")
builder.add_edge("fetch_docs", "analyze")
builder.add_edge("analyze", "respond")
builder.add_edge("respond", END)

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)
```

**Human-in-the-Loop:**

```python
from langgraph.types import interrupt, Command

def approval_node(state: State) -> Command[Literal["execute", "reject"]]:
    if state["needs_approval"]:
        response = interrupt({"action": state["proposed_action"]})
        if response["approved"]:
            return Command(update={"approved": True}, goto="execute")
        return Command(goto="reject")
    return Command(goto="execute")
```

## Deliverables

Provide the user with:

1. **Complete implementation** with all code
2. **Clear documentation** explaining the design
3. **Usage examples** showing how to invoke the graph
4. **Testing suggestions** for validation
5. **Next steps** for enhancement and deployment

Follow the coding standards from `../instructions/langgraph.instructions.md` and leverage the agent expertise from `../agents/langgraph.agent.md`.

Ask clarifying questions if needed, then create a complete, working LangGraph workflow!
