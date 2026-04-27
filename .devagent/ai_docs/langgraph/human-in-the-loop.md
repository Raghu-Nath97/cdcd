# LangGraph Human-in-the-Loop Patterns

## Overview

Human-in-the-loop (HITL) enables human oversight and intervention in agent workflows. LangGraph provides flexible interrupts to pause execution, collect human input, and resume.

## Types of Interrupts

### Static Interrupts

Predefined breakpoints in the graph.

**Interrupt Before:**

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
graph = builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["critical_action", "send_email"]
)
```

**Interrupt After:**

```python
graph = builder.compile(
    checkpointer=checkpointer,
    interrupt_after=["generate_response"]
)
```

### Dynamic Interrupts

Conditional pauses based on state.

**Basic Usage:**

```python
from langgraph.types import interrupt

def approval_node(state: State) -> dict:
    if state["requires_approval"]:
        # Pause and request human input
        user_response = interrupt({
            "action": state["proposed_action"],
            "message": "Please approve this action"
        })
        
        return {"approved": user_response["approved"]}
    
    return {"approved": True}
```

**With Command:**

```python
from typing import Literal
from langgraph.types import interrupt, Command

def review_node(state: State) -> Command[Literal["execute", "revise", "cancel"]]:
    review_data = interrupt({
        "draft": state["draft"],
        "message": "Review the draft"
    })
    
    if review_data["action"] == "approve":
        return Command(update={"approved": True}, goto="execute")
    elif review_data["action"] == "edit":
        return Command(update={"draft": review_data["edits"]}, goto="revise")
    else:
        return Command(goto="cancel")
```

## Common Patterns

### 1. Approve or Reject

Pause before critical operations.

```python
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.types import Command
from typing import Literal

class ApprovalState(MessagesState):
    proposed_action: dict
    approved: bool

def plan_action(state: ApprovalState) -> dict:
    """Plan what action to take."""
    action = {"type": "send_email", "to": "customer@example.com"}
    return {"proposed_action": action}

def request_approval(state: ApprovalState) -> Command[Literal["execute", "cancel"]]:
    """Request human approval."""
    approval = interrupt({
        "action": state["proposed_action"],
        "message": "Approve this action?"
    })
    
    if approval["approved"]:
        return Command(update={"approved": True}, goto="execute")
    return Command(update={"approved": False}, goto="cancel")

def execute_action(state: ApprovalState) -> dict:
    """Execute the approved action."""
    # Perform action
    return {"messages": [AIMessage(content="Action executed")]}

def cancel_action(state: ApprovalState) -> dict:
    """Handle cancellation."""
    return {"messages": [AIMessage(content="Action cancelled")]}

builder = StateGraph(ApprovalState)
builder.add_node("plan", plan_action)
builder.add_node("approval", request_approval)
builder.add_node("execute", execute_action)
builder.add_node("cancel", cancel_action)

builder.add_edge(START, "plan")
builder.add_edge("plan", "approval")
builder.add_edge("execute", END)
builder.add_edge("cancel", END)

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)
```

**Usage:**

```python
config = {"configurable": {"thread_id": "1"}}

# Start execution - will pause at interrupt
result = graph.invoke(
    {"messages": [HumanMessage(content="Send email to customer")]},
    config=config
)

# Check state
state = graph.get_state(config)
print("Waiting for approval:", state.values["proposed_action"])

# Resume with approval
result = graph.invoke(
    Command(resume={"approved": True}),
    config=config
)
```

### 2. Edit Graph State

Review and modify state before continuing.

```python
class EditState(MessagesState):
    draft: str
    final: str

def generate_draft(state: EditState) -> dict:
    """Generate initial draft."""
    llm = ChatAnthropic(model="claude-3-7-sonnet-latest")
    draft = llm.invoke(state["messages"])
    return {"draft": draft.content}

def review_draft(state: EditState) -> Command[Literal["finalize", "generate"]]:
    """Allow human to review and edit."""
    review_result = interrupt({
        "draft": state["draft"],
        "message": "Review and edit the draft"
    })
    
    if review_result["action"] == "approve":
        return Command(update={"final": state["draft"]}, goto="finalize")
    else:
        # Human provided edits
        return Command(
            update={"draft": review_result["edited_draft"]},
            goto="finalize"
        )

def finalize(state: EditState) -> dict:
    """Finalize the content."""
    return {
        "final": state.get("final", state["draft"]),
        "messages": [AIMessage(content="Draft finalized")]
    }

builder = StateGraph(EditState)
builder.add_node("generate", generate_draft)
builder.add_node("review", review_draft)
builder.add_node("finalize", finalize)

builder.add_edge(START, "generate")
builder.add_edge("generate", "review")
builder.add_edge("finalize", END)

graph = builder.compile(checkpointer=checkpointer)
```

**Usage:**

```python
# Start
config = {"configurable": {"thread_id": "2"}}
graph.invoke({"messages": [HumanMessage(content="Write about AI")]}, config)

# Review state
state = graph.get_state(config)
print("Draft:", state.values["draft"])

# Resume with edits
graph.invoke(
    Command(resume={
        "action": "edit",
        "edited_draft": "Human-edited version..."
    }),
    config=config
)
```

### 3. Review Tool Calls

Inspect and modify LLM tool calls before execution.

```python
from langgraph.prebuilt import ToolNode

def review_tool_calls(state: MessagesState) -> Command[Literal["tools", "agent", "END"]]:
    """Review tool calls before execution."""
    last_message = state["messages"][-1]
    
    if not last_message.tool_calls:
        return Command(goto="END")
    
    # Present tool calls to human
    review = interrupt({
        "tool_calls": last_message.tool_calls,
        "message": "Review these tool calls"
    })
    
    if review["action"] == "approve":
        return Command(goto="tools")
    elif review["action"] == "modify":
        # Update tool calls
        modified_message = last_message.copy()
        modified_message.tool_calls = review["modified_calls"]
        return Command(
            update={"messages": [modified_message]},
            goto="tools"
        )
    else:
        # Reject and ask agent to reconsider
        return Command(
            update={"messages": [HumanMessage(content="Reconsider your approach")]},
            goto="agent"
        )

builder = StateGraph(MessagesState)
builder.add_node("agent", call_model)
builder.add_node("review", review_tool_calls)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "agent")
builder.add_edge("agent", "review")
builder.add_edge("tools", "agent")

graph = builder.compile(checkpointer=checkpointer)
```

### 4. Validate Human Input

Pause to collect and validate user input.

```python
class ValidationState(MessagesState):
    user_data: dict
    validated: bool

def request_input(state: ValidationState) -> dict:
    """Request user input."""
    user_input = interrupt({
        "message": "Please provide required information",
        "fields": ["name", "email", "preferences"]
    })
    
    return {"user_data": user_input}

def validate_input(state: ValidationState) -> Command[Literal["process", "request_input"]]:
    """Validate the input."""
    data = state["user_data"]
    
    # Validation logic
    if is_valid(data):
        return Command(update={"validated": True}, goto="process")
    else:
        error_msg = HumanMessage(content="Invalid input. Please try again.")
        return Command(
            update={"messages": [error_msg], "validated": False},
            goto="request_input"
        )

def process_data(state: ValidationState) -> dict:
    """Process validated data."""
    # Processing logic
    return {"messages": [AIMessage(content="Data processed successfully")]}

builder = StateGraph(ValidationState)
builder.add_node("request_input", request_input)
builder.add_node("validate", validate_input)
builder.add_node("process", process_data)

builder.add_edge(START, "request_input")
builder.add_edge("request_input", "validate")
builder.add_edge("process", END)

graph = builder.compile(checkpointer=checkpointer)
```

## Advanced Patterns

### Multi-Stage Approval

Multiple approval points in workflow.

```python
def stage1_approval(state: State) -> Command[Literal["stage2", "cancel"]]:
    approval = interrupt({"stage": "initial_review"})
    if approval["approved"]:
        return Command(goto="stage2")
    return Command(goto="cancel")

def stage2_approval(state: State) -> Command[Literal["execute", "cancel"]]:
    approval = interrupt({"stage": "final_review"})
    if approval["approved"]:
        return Command(goto="execute")
    return Command(goto="cancel")
```

### Conditional Interrupts

Only interrupt when certain conditions are met.

```python
def conditional_check(state: State) -> dict:
    if state["confidence_score"] < 0.8:
        # Low confidence - ask for human input
        feedback = interrupt({
            "result": state["result"],
            "confidence": state["confidence_score"],
            "message": "Low confidence. Please review."
        })
        return {"result": feedback["corrected_result"]}
    
    # High confidence - proceed automatically
    return state
```

### Timeout Handling

Add timeout for human response.

```python
import asyncio

async def timed_approval(state: State) -> Command:
    try:
        # Wait for human input with timeout
        approval = await asyncio.wait_for(
            interrupt_async({"message": "Approve?"}),
            timeout=300  # 5 minutes
        )
        if approval["approved"]:
            return Command(goto="execute")
    except asyncio.TimeoutError:
        # Default action on timeout
        return Command(goto="default_action")
    
    return Command(goto="cancel")
```

## Best Practices

### 1. Clear Communication

Provide context in interrupts:

```python
interrupt({
    "message": "Review this action",
    "context": state["context"],
    "proposed_action": state["action"],
    "potential_impact": "This will send 1000 emails"
})
```

### 2. State Management

Save enough state to resume:

```python
def node_with_interrupt(state: State) -> dict:
    partial_result = compute_partial()
    
    approval = interrupt({
        "partial_result": partial_result,
        "next_steps": ["step1", "step2"]
    })
    
    # Can resume with all context
    return {"result": complete_computation(partial_result, approval)}
```

### 3. Error Handling

Handle cancellations gracefully:

```python
def safe_interrupt_node(state: State) -> Command[Literal["continue", "cancel"]]:
    try:
        response = interrupt({"message": "Continue?"})
        if response.get("continue"):
            return Command(goto="continue")
    except Exception as e:
        # Log error and use safe default
        log_error(e)
    
    return Command(goto="cancel")
```

### 4. Resumption Patterns

Use Command for clean resumption:

```python
# Instead of complex state updates
result = graph.invoke(Command(resume=response), config=config)

# Rather than
graph.update_state(config, complex_state_updates)
result = graph.invoke(None, config=config)
```

### 5. Testing HITL Workflows

Test without human interaction:

```python
def mock_interrupt(data):
    """Mock interrupt for testing."""
    return {"approved": True}  # Auto-approve in tests

# In tests, replace interrupt function
import langgraph.types
langgraph.types.interrupt = mock_interrupt
```

## Usage Examples

### Basic Interrupt Flow

```python
# Initial invocation
config = {"configurable": {"thread_id": "abc123"}}
result = graph.invoke(inputs, config=config)

# Check if interrupted
state = graph.get_state(config)
if state.next:  # Has pending nodes
    # Show interrupt data to human
    interrupt_data = state.tasks[0].interrupts[0] if state.tasks else None
    
    # Get human decision
    human_response = get_human_input(interrupt_data)
    
    # Resume execution
    result = graph.invoke(Command(resume=human_response), config=config)
```

### Static Interrupt Pattern

```python
# Compile with breakpoints
graph = builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["critical_node"]
)

# Execution pauses before critical_node
graph.invoke(inputs, config=config)

# Review state
state = graph.get_state(config)

# Optionally update state
graph.update_state(config, {"reviewed": True})

# Resume
graph.invoke(None, config=config)
```

## Integration with UI

### Web Application Pattern

```python
# Backend API
@app.post("/start")
def start_workflow(data: dict):
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        result = graph.invoke(data, config=config)
        return {"thread_id": thread_id, "result": result}
    except InterruptError:
        state = graph.get_state(config)
        return {
            "thread_id": thread_id,
            "status": "awaiting_input",
            "interrupt_data": extract_interrupt_data(state)
        }

@app.post("/resume/{thread_id}")
def resume_workflow(thread_id: str, response: dict):
    config = {"configurable": {"thread_id": thread_id}}
    result = graph.invoke(Command(resume=response), config=config)
    return {"result": result}
```

Human-in-the-loop is essential for production agent systems, enabling safety, oversight, and quality control.
