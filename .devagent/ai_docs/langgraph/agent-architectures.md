# LangGraph Agent Architectures

## Overview

LangGraph enables various agent architectures, from simple routers to complex multi-agent systems. Choose the right architecture based on your use case.

## Architecture Types

### 1. Router

**Use Case:** Select a single action from predefined options.

**Characteristics:**

- Simple, single-step decision
- Limited LLM control
- Fast execution
- Good for classification/routing tasks

**Example:**

```python
from langchain_openai import ChatOpenAI
from typing import Literal
from langgraph.graph import StateGraph, START, END

class RouterState(TypedDict):
    query: str
    route: Literal["sales", "support", "billing"]

def classify_query(state: RouterState) -> dict:
    llm = ChatOpenAI(model="gpt-4")
    response = llm.invoke([
        {"role": "system", "content": "Classify query as: sales, support, or billing"},
        {"role": "user", "content": state["query"]}
    ])
    return {"route": response.content}

builder = StateGraph(RouterState)
builder.add_node("classifier", classify_query)
builder.add_edge(START, "classifier")
builder.add_edge("classifier", END)
graph = builder.compile()
```

**When to Use:**

- Simple categorization tasks
- Directing queries to appropriate handlers
- Low latency requirements
- Deterministic outcomes preferred

### 2. Tool-Calling Agent (ReAct)

**Use Case:** Multi-step reasoning with tool access.

**Characteristics:**

- LLM decides which tools to use
- Iterative planning and execution
- Combines reasoning (Re) and acting (Act)
- Handles complex, multi-step tasks

**Prebuilt Implementation:**

```python
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic

def search_tool(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

def calculator(expression: str) -> float:
    """Evaluate math expressions."""
    return eval(expression)

agent = create_react_agent(
    model=ChatAnthropic(model="claude-3-7-sonnet-latest"),
    tools=[search_tool, calculator],
    prompt="You are a helpful research assistant"
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "What is 25 * 4 + 10?"}]
})
```

**Custom Implementation:**

```python
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage

class AgentState(MessagesState):
    pass

def should_continue(state: AgentState) -> Literal["tools", "END"]:
    """Route based on tool calls."""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return "END"

def call_model(state: AgentState):
    llm = ChatAnthropic(model="claude-3-7-sonnet-latest")
    llm_with_tools = llm.bind_tools([search_tool, calculator])
    
    messages = [SystemMessage(content="You are a helpful assistant")] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

builder = StateGraph(AgentState)
builder.add_node("agent", call_model)
builder.add_node("tools", ToolNode([search_tool, calculator]))

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", should_continue)
builder.add_edge("tools", "agent")

graph = builder.compile()
```

**When to Use:**

- Complex problem-solving
- Need multiple tools
- Multi-step reasoning required
- Flexible decision-making needed

### 3. Hierarchical Agent

**Use Case:** Supervisor coordinating specialized sub-agents.

**Characteristics:**

- Main agent delegates to specialists
- Each sub-agent has specific expertise
- Hierarchical decision-making
- Good for complex, domain-specific tasks

**Example:**

```python
from typing import Literal
from langgraph.types import Command

class SupervisorState(MessagesState):
    next_agent: str

def supervisor(state: SupervisorState) -> Command[Literal["research_agent", "writer_agent", "reviewer_agent", "END"]]:
    """Coordinate sub-agents."""
    llm = ChatAnthropic(model="claude-3-7-sonnet-latest")
    
    system_msg = """You are a supervisor coordinating:
    - research_agent: Gathers information
    - writer_agent: Creates content
    - reviewer_agent: Reviews and improves
    
    Choose the next agent or END if complete."""
    
    messages = [SystemMessage(content=system_msg)] + state["messages"]
    response = llm.invoke(messages)
    
    next_agent = extract_agent_choice(response.content)
    return Command(
        update={"messages": [response]},
        goto=next_agent
    )

def research_agent(state: SupervisorState) -> dict:
    """Research specialist."""
    # Research implementation
    return {"messages": [AIMessage(content="Research results...")]}

def writer_agent(state: SupervisorState) -> dict:
    """Writing specialist."""
    # Writing implementation
    return {"messages": [AIMessage(content="Draft content...")]}

def reviewer_agent(state: SupervisorState) -> dict:
    """Review specialist."""
    # Review implementation
    return {"messages": [AIMessage(content="Reviewed content...")]}

builder = StateGraph(SupervisorState)
builder.add_node("supervisor", supervisor)
builder.add_node("research_agent", research_agent)
builder.add_node("writer_agent", writer_agent)
builder.add_node("reviewer_agent", reviewer_agent)

builder.add_edge(START, "supervisor")
# Sub-agents report back to supervisor
builder.add_edge("research_agent", "supervisor")
builder.add_edge("writer_agent", "supervisor")
builder.add_edge("reviewer_agent", "supervisor")

graph = builder.compile()
```

**When to Use:**

- Complex multi-domain problems
- Need specialized expertise
- Clear task delegation
- Coordinated workflow needed

### 4. Collaborative Multi-Agent

**Use Case:** Peer agents collaborating on tasks.

**Characteristics:**

- Agents communicate directly
- Shared state
- Collaborative decision-making
- Flexible interaction patterns

**Example:**

```python
from typing import Literal
from langgraph.types import Command

class CollaborativeState(MessagesState):
    current_agent: str
    task_status: dict

def data_analyst(state: CollaborativeState) -> Command[Literal["engineer", "scientist", "END"]]:
    """Analyze data and route to appropriate specialist."""
    # Analysis logic
    analysis = perform_analysis(state["messages"])
    
    if analysis["needs_engineering"]:
        return Command(
            update={"messages": [AIMessage(content=f"Analysis: {analysis}")]},
            goto="engineer"
        )
    elif analysis["needs_modeling"]:
        return Command(
            update={"messages": [AIMessage(content=f"Analysis: {analysis}")]},
            goto="scientist"
        )
    return Command(goto="END")

def data_engineer(state: CollaborativeState) -> Command[Literal["scientist", "analyst", "END"]]:
    """Handle data engineering tasks."""
    # Engineering logic
    result = engineering_task(state)
    
    if result["ready_for_modeling"]:
        return Command(
            update={"messages": [AIMessage(content=f"Data prepared: {result}")]},
            goto="scientist"
        )
    return Command(goto="END")

def data_scientist(state: CollaborativeState) -> Command[Literal["analyst", "engineer", "END"]]:
    """Build and evaluate models."""
    # Science logic
    model_result = build_model(state)
    
    if model_result["needs_more_data"]:
        return Command(
            update={"messages": [AIMessage(content="Need more data")]},
            goto="engineer"
        )
    elif model_result["needs_analysis"]:
        return Command(
            update={"messages": [AIMessage(content="Results ready for analysis")]},
            goto="analyst"
        )
    return Command(goto="END")

builder = StateGraph(CollaborativeState)
builder.add_node("analyst", data_analyst)
builder.add_node("engineer", data_engineer)
builder.add_node("scientist", data_scientist)

builder.add_edge(START, "analyst")
graph = builder.compile()
```

**When to Use:**

- Team-based problem solving
- Iterative collaboration needed
- Complex interdependencies
- Flexible workflow

### 5. Reflection Agent

**Use Case:** Self-improving agent with feedback loops.

**Characteristics:**

- Generates output
- Evaluates quality
- Refines based on feedback
- Iterative improvement

**Example:**

```python
class ReflectionState(MessagesState):
    draft: str
    reflection: str
    iterations: int

def generate(state: ReflectionState) -> dict:
    """Generate initial response."""
    llm = ChatAnthropic(model="claude-3-7-sonnet-latest")
    response = llm.invoke(state["messages"])
    return {
        "draft": response.content,
        "iterations": state.get("iterations", 0) + 1
    }

def reflect(state: ReflectionState) -> dict:
    """Critique the draft."""
    llm = ChatAnthropic(model="claude-3-7-sonnet-latest")
    
    reflection_prompt = f"""Review this draft:
    {state['draft']}
    
    Provide specific feedback on:
    - Accuracy
    - Completeness
    - Clarity
    - Areas for improvement
    """
    
    response = llm.invoke([{"role": "user", "content": reflection_prompt}])
    return {"reflection": response.content}

def should_continue(state: ReflectionState) -> Literal["generate", "END"]:
    """Decide whether to refine further."""
    if state["iterations"] >= 3:
        return "END"
    
    # Check if reflection indicates improvement needed
    if "needs improvement" in state.get("reflection", "").lower():
        return "generate"
    return "END"

builder = StateGraph(ReflectionState)
builder.add_node("generate", generate)
builder.add_node("reflect", reflect)

builder.add_edge(START, "generate")
builder.add_edge("generate", "reflect")
builder.add_conditional_edges("reflect", should_continue)

graph = builder.compile()
```

**When to Use:**

- Quality is critical
- Self-correction needed
- Iterative refinement beneficial
- Complex output generation

### 6. Planning Agent

**Use Case:** Create and execute multi-step plans.

**Characteristics:**

- Decomposes tasks into steps
- Executes plan sequentially
- Adapts based on results
- Tracks progress

**Example:**

```python
class PlanningState(MessagesState):
    plan: list[str]
    current_step: int
    step_results: list[dict]

def create_plan(state: PlanningState) -> dict:
    """Generate execution plan."""
    llm = ChatAnthropic(model="claude-3-7-sonnet-latest")
    
    prompt = f"""Create a step-by-step plan for:
    {state['messages'][-1].content}
    
    Output as numbered list."""
    
    response = llm.invoke([{"role": "user", "content": prompt}])
    plan = parse_plan(response.content)
    return {"plan": plan, "current_step": 0, "step_results": []}

def execute_step(state: PlanningState) -> dict:
    """Execute current plan step."""
    current_step = state["plan"][state["current_step"]]
    
    # Execute the step
    result = perform_step(current_step)
    
    step_results = state["step_results"] + [result]
    return {
        "current_step": state["current_step"] + 1,
        "step_results": step_results
    }

def should_continue(state: PlanningState) -> Literal["execute_step", "END"]:
    """Check if more steps remain."""
    if state["current_step"] < len(state["plan"]):
        return "execute_step"
    return "END"

builder = StateGraph(PlanningState)
builder.add_node("create_plan", create_plan)
builder.add_node("execute_step", execute_step)

builder.add_edge(START, "create_plan")
builder.add_edge("create_plan", "execute_step")
builder.add_conditional_edges("execute_step", should_continue)

graph = builder.compile()
```

**When to Use:**

- Complex multi-step tasks
- Need explicit planning
- Sequential execution
- Progress tracking required

## Choosing the Right Architecture

| Architecture | Complexity | Control | Use Case |
|-------------|-----------|---------|----------|
| Router | Low | Simple | Classification, routing |
| ReAct Agent | Medium | Flexible | Tool use, research |
| Hierarchical | High | Coordinated | Complex domains |
| Collaborative | High | Distributed | Team workflows |
| Reflection | Medium | Self-improving | Quality-critical |
| Planning | Medium-High | Structured | Multi-step tasks |

## Advanced Patterns

### Human-in-the-Loop

Add approval steps at critical points:

```python
graph = builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["execute_action"]
)
```

### Dynamic Parallelization

Process items concurrently:

```python
from langgraph.types import Send

def fan_out(state):
    return [Send("process", {"item": i}) for i in state["items"]]
```

### Subgraphs

Isolate agent subsystems:

```python
subgraph = create_specialized_graph()
builder.add_node("specialized_agent", subgraph)
```

## Best Practices

1. **Start simple** - Use prebuilt agents when possible
2. **Add complexity gradually** - Layer features as needed
3. **Test components independently** - Validate nodes before integration
4. **Monitor performance** - Track token usage and latency
5. **Use appropriate persistence** - Checkpoints for state, store for memory
6. **Handle errors gracefully** - Add retry logic and fallbacks
7. **Visualize workflows** - Graph diagrams aid understanding
8. **Document intent** - Clear node and edge naming
9. **Consider scalability** - Async execution for production
10. **Enable observability** - LangSmith tracing for debugging
