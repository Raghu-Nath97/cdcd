# LangGraph Common Examples

## Quick Start Examples

### 1. Simple Chat Agent

Basic conversational agent with memory:

```python
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import InMemorySaver

# Create agent with tools
model = ChatAnthropic(model="claude-3-7-sonnet-latest")
tools = []  # Add your tools here

agent = create_react_agent(
    model,
    tools,
    prompt="You are a helpful assistant"
)

# Use with persistence
checkpointer = InMemorySaver()
agent = create_react_agent(model, tools, checkpointer=checkpointer)

# Invoke with thread
config = {"configurable": {"thread_id": "user-123"}}
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Hello!"}]},
    config=config
)
```

### 2. Custom Sequential Workflow

Multi-step processing pipeline:

```python
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

class WorkflowState(TypedDict):
    input: str
    step1_result: str
    step2_result: str
    final_output: str

def step1(state: WorkflowState) -> dict:
    result = process_step1(state["input"])
    return {"step1_result": result}

def step2(state: WorkflowState) -> dict:
    result = process_step2(state["step1_result"])
    return {"step2_result": result}

def finalize(state: WorkflowState) -> dict:
    result = create_output(state["step2_result"])
    return {"final_output": result}

builder = StateGraph(WorkflowState)
builder.add_node("step1", step1)
builder.add_node("step2", step2)
builder.add_node("finalize", finalize)

builder.add_edge(START, "step1")
builder.add_edge("step1", "step2")
builder.add_edge("step2", "finalize")
builder.add_edge("finalize", END)

graph = builder.compile()

result = graph.invoke({"input": "process this"})
```

### 3. Conditional Routing

Branch based on state:

```python
from typing import Literal

class RouterState(TypedDict):
    input: str
    category: str
    result: str

def classify(state: RouterState) -> dict:
    category = determine_category(state["input"])
    return {"category": category}

def route(state: RouterState) -> Literal["handler_a", "handler_b", "handler_c"]:
    category = state["category"]
    if category == "type_a":
        return "handler_a"
    elif category == "type_b":
        return "handler_b"
    return "handler_c"

def handler_a(state: RouterState) -> dict:
    return {"result": "Handled by A"}

def handler_b(state: RouterState) -> dict:
    return {"result": "Handled by B"}

def handler_c(state: RouterState) -> dict:
    return {"result": "Handled by C"}

builder = StateGraph(RouterState)
builder.add_node("classify", classify)
builder.add_node("handler_a", handler_a)
builder.add_node("handler_b", handler_b)
builder.add_node("handler_c", handler_c)

builder.add_edge(START, "classify")
builder.add_conditional_edges("classify", route)
builder.add_edge("handler_a", END)
builder.add_edge("handler_b", END)
builder.add_edge("handler_c", END)

graph = builder.compile()
```

### 4. Using Command for Routing

Combine state updates and routing:

```python
from langgraph.types import Command

class ProcessState(TypedDict):
    data: str
    processed: bool
    retry_count: int

def process_node(state: ProcessState) -> Command[Literal["validate", "retry", "END"]]:
    try:
        result = process_data(state["data"])
        return Command(
            update={"data": result, "processed": True},
            goto="validate"
        )
    except Exception as e:
        if state.get("retry_count", 0) < 3:
            return Command(
                update={"retry_count": state.get("retry_count", 0) + 1},
                goto="retry"
            )
        return Command(goto="END")

def validate_node(state: ProcessState) -> Command[Literal["END", "process"]]:
    if is_valid(state["data"]):
        return Command(goto="END")
    return Command(update={"processed": False}, goto="process")

def retry_node(state: ProcessState) -> Command[Literal["process"]]:
    # Wait and retry
    return Command(goto="process")

builder = StateGraph(ProcessState)
builder.add_node("process", process_node)
builder.add_node("validate", validate_node)
builder.add_node("retry", retry_node)

builder.add_edge(START, "process")
graph = builder.compile()
```

### 5. Parallel Processing with Send

Map-reduce pattern:

```python
from langgraph.types import Send
from typing import Annotated
from operator import add

class MapReduceState(TypedDict):
    items: list[str]
    processed_items: Annotated[list[str], add]
    final_result: str

def map_items(state: MapReduceState) -> list[Send]:
    # Create parallel tasks
    return [
        Send("process_item", {"item": item})
        for item in state["items"]
    ]

def process_item(state: dict) -> dict:
    # Process individual item
    result = expensive_operation(state["item"])
    return {"processed_items": [result]}

def reduce_results(state: MapReduceState) -> dict:
    # Combine results
    final = combine(state["processed_items"])
    return {"final_result": final}

builder = StateGraph(MapReduceState)
builder.add_node("map", map_items)
builder.add_node("process_item", process_item)
builder.add_node("reduce", reduce_results)

builder.add_edge(START, "map")
builder.add_conditional_edges("map", lambda s: [])  # Send handles routing
builder.add_edge("process_item", "reduce")
builder.add_edge("reduce", END)

graph = builder.compile()

result = graph.invoke({"items": ["item1", "item2", "item3"]})
```

### 6. Chat with RAG

Retrieval-augmented generation:

```python
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, AIMessage

class RAGState(MessagesState):
    documents: list[str]
    context: str

def retrieve_docs(state: RAGState) -> dict:
    # Get last user message
    query = state["messages"][-1].content
    
    # Retrieve relevant documents
    docs = vector_store.similarity_search(query, k=3)
    
    return {
        "documents": [doc.page_content for doc in docs],
        "context": "\n\n".join([doc.page_content for doc in docs])
    }

def generate_response(state: RAGState) -> dict:
    llm = ChatAnthropic(model="claude-3-7-sonnet-latest")
    
    # Create prompt with context
    prompt = f"""Context:
{state['context']}

Question: {state['messages'][-1].content}

Answer the question based on the context."""
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"messages": [response]}

builder = StateGraph(RAGState)
builder.add_node("retrieve", retrieve_docs)
builder.add_node("generate", generate_response)

builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# Use in conversation
config = {"configurable": {"thread_id": "chat-1"}}
result = graph.invoke(
    {"messages": [HumanMessage(content="What is LangGraph?")]},
    config=config
)
```

### 7. Human-in-the-Loop Approval

Pause for human review:

```python
from langgraph.types import interrupt, Command

class ApprovalState(MessagesState):
    action: dict
    approved: bool

def plan_action(state: ApprovalState) -> dict:
    action = {"type": "database_write", "data": {"user": "update"}}
    return {"action": action}

def request_approval(state: ApprovalState) -> Command[Literal["execute", "cancel"]]:
    # Pause for human input
    response = interrupt({
        "action": state["action"],
        "message": "Approve this database write?"
    })
    
    if response.get("approved"):
        return Command(update={"approved": True}, goto="execute")
    return Command(update={"approved": False}, goto="cancel")

def execute_action(state: ApprovalState) -> dict:
    # Execute the action
    execute(state["action"])
    return {"messages": [AIMessage(content="Action executed")]}

def cancel_action(state: ApprovalState) -> dict:
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

# Start workflow
config = {"configurable": {"thread_id": "workflow-1"}}
graph.invoke({"messages": []}, config=config)

# Check state (paused at interrupt)
state = graph.get_state(config)

# Resume with approval
graph.invoke(Command(resume={"approved": True}), config=config)
```

### 8. Multi-Agent Collaboration

Multiple agents working together:

```python
class MultiAgentState(MessagesState):
    current_agent: str
    task_complete: bool

def researcher(state: MultiAgentState) -> Command[Literal["writer", "END"]]:
    research_results = conduct_research(state["messages"][-1].content)
    
    return Command(
        update={
            "messages": [AIMessage(content=f"Research: {research_results}")],
            "current_agent": "writer"
        },
        goto="writer"
    )

def writer(state: MultiAgentState) -> Command[Literal["reviewer", "END"]]:
    draft = write_content(state["messages"])
    
    return Command(
        update={
            "messages": [AIMessage(content=f"Draft: {draft}")],
            "current_agent": "reviewer"
        },
        goto="reviewer"
    )

def reviewer(state: MultiAgentState) -> Command[Literal["writer", "END"]]:
    review = review_content(state["messages"][-1].content)
    
    if review["needs_revision"]:
        return Command(
            update={
                "messages": [AIMessage(content=f"Feedback: {review['feedback']}")],
                "current_agent": "writer"
            },
            goto="writer"
        )
    
    return Command(
        update={"task_complete": True},
        goto="END"
    )

builder = StateGraph(MultiAgentState)
builder.add_node("researcher", researcher)
builder.add_node("writer", writer)
builder.add_node("reviewer", reviewer)

builder.add_edge(START, "researcher")
graph = builder.compile()
```

### 9. Persistent Memory Store

Cross-session user memory:

```python
from langgraph.store.memory import InMemoryStore
from langchain.embeddings import init_embeddings
import uuid

# Create store with semantic search
store = InMemoryStore(
    index={
        "embed": init_embeddings("openai:text-embedding-3-small"),
        "dims": 1536,
        "fields": ["content"]
    }
)

class MemoryState(MessagesState):
    user_id: str

def recall_memories(state: MemoryState, config, *, store) -> dict:
    user_id = config["configurable"]["user_id"]
    namespace = (user_id, "memories")
    
    # Semantic search for relevant memories
    query = state["messages"][-1].content
    memories = store.search(namespace, query=query, limit=3)
    
    memory_context = "\n".join([m.value["content"] for m in memories])
    return {"messages": [AIMessage(content=f"Context: {memory_context}")]}

def respond(state: MemoryState, config, *, store) -> dict:
    llm = ChatAnthropic(model="claude-3-7-sonnet-latest")
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def save_memory(state: MemoryState, config, *, store) -> dict:
    user_id = config["configurable"]["user_id"]
    namespace = (user_id, "memories")
    
    # Extract and save important information
    conversation = state["messages"][-2:]  # Last exchange
    memory_content = extract_memory(conversation)
    
    if memory_content:
        memory_id = str(uuid.uuid4())
        store.put(namespace, memory_id, {"content": memory_content})
    
    return {}

builder = StateGraph(MemoryState)
builder.add_node("recall", recall_memories)
builder.add_node("respond", respond)
builder.add_node("save", save_memory)

builder.add_edge(START, "recall")
builder.add_edge("recall", "respond")
builder.add_edge("respond", "save")
builder.add_edge("save", END)

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer, store=store)

# Use across multiple conversations
config1 = {"configurable": {"thread_id": "chat-1", "user_id": "user-123"}}
config2 = {"configurable": {"thread_id": "chat-2", "user_id": "user-123"}}

# Memories persist across both threads
graph.invoke({"messages": [HumanMessage(content="I love pizza")]}, config1)
graph.invoke({"messages": [HumanMessage(content="What do I like?")]}, config2)
```

### 10. Error Handling and Retry

Robust error handling:

```python
class RetryState(TypedDict):
    input: str
    result: str
    error: str
    retry_count: int

def process_with_retry(state: RetryState) -> Command[Literal["validate", "retry", "error_handler"]]:
    try:
        result = risky_operation(state["input"])
        return Command(
            update={"result": result, "error": ""},
            goto="validate"
        )
    except Exception as e:
        retry_count = state.get("retry_count", 0)
        
        if retry_count < 3:
            return Command(
                update={
                    "error": str(e),
                    "retry_count": retry_count + 1
                },
                goto="retry"
            )
        
        return Command(
            update={"error": str(e)},
            goto="error_handler"
        )

def retry_with_backoff(state: RetryState) -> Command[Literal["process"]]:
    # Exponential backoff
    import time
    backoff = 2 ** state["retry_count"]
    time.sleep(backoff)
    return Command(goto="process")

def validate_result(state: RetryState) -> Command[Literal["END", "process"]]:
    if is_valid(state["result"]):
        return Command(goto="END")
    
    return Command(
        update={"error": "Validation failed"},
        goto="process"
    )

def handle_error(state: RetryState) -> dict:
    # Log error and return safe default
    log_error(state["error"])
    return {"result": "default_safe_value"}

builder = StateGraph(RetryState)
builder.add_node("process", process_with_retry)
builder.add_node("retry", retry_with_backoff)
builder.add_node("validate", validate_result)
builder.add_node("error_handler", handle_error)

builder.add_edge(START, "process")
builder.add_edge("error_handler", END)

graph = builder.compile()
```

## Testing Patterns

### Unit Testing Nodes

```python
def test_node_function():
    state = {"input": "test data"}
    result = my_node(state)
    assert result["output"] == expected_output

def test_with_mock_llm():
    from unittest.mock import Mock
    
    mock_llm = Mock()
    mock_llm.invoke.return_value = AIMessage(content="mocked response")
    
    # Test node with mock
    result = llm_node(state, llm=mock_llm)
    assert "mocked response" in result["messages"][-1].content
```

### Integration Testing

```python
def test_full_workflow():
    graph = builder.compile()
    result = graph.invoke({"input": "test"})
    assert result["final_output"] is not None
    
def test_with_persistence():
    checkpointer = InMemorySaver()
    graph = builder.compile(checkpointer=checkpointer)
    
    config = {"configurable": {"thread_id": "test-1"}}
    
    # First call
    graph.invoke({"messages": [HumanMessage(content="Hello")]}, config)
    
    # Verify state persisted
    state = graph.get_state(config)
    assert len(state.values["messages"]) > 0
```

These examples cover the most common LangGraph patterns and should help you build production-ready agent workflows!
