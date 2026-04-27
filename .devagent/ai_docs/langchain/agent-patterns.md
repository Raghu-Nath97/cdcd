# LangChain Agent Architecture Patterns

## Table of Contents
1. [Basic Agents](#basic-agents)
2. [Agents with Structured Output](#agents-with-structured-output)
3. [Agents with Custom State](#agents-with-custom-state)
4. [Multi-Tool Agents](#multi-tool-agents)
5. [Context-Aware Agents](#context-aware-agents)
6. [Production Patterns](#production-patterns)

---

## Basic Agents

### Simple Question-Answer Agent
```python
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def search_knowledge_base(query: str) -> str:
    """Search the knowledge base for information.
    
    Args:
        query: The search query
    """
    # Your search implementation
    return f"Knowledge base results for: {query}"

agent = create_agent(
    model="openai:gpt-4o",
    tools=[search_knowledge_base],
    system_prompt="You are a helpful knowledge assistant. Use the search tool to find accurate information."
)

# Use the agent
result = agent.invoke({
    "messages": [{"role": "user", "content": "What is machine learning?"}]
})

print(result["messages"][-1].content)
```

### Research Agent with Multiple Steps
```python
from langchain.tools import tool

@tool
def web_search(query: str) -> str:
    """Search the web for current information."""
    return f"Web results for: {query}"

@tool
def summarize_text(text: str, max_words: int = 100) -> str:
    """Summarize text to a maximum word count."""
    return f"Summary of {len(text)} characters (max {max_words} words)"

agent = create_agent(
    model="anthropic:claude-sonnet-4-5",
    tools=[web_search, summarize_text],
    system_prompt="""You are a research assistant.
    1. First search for information
    2. Then summarize the findings
    3. Provide a clear, concise answer"""
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Research recent AI developments and summarize"}]
})
```

---

## Agents with Structured Output

### Data Extraction Agent
```python
from pydantic import BaseModel, Field
from langchain.agents.structured_output import ToolStrategy

class PersonInfo(BaseModel):
    """Extracted person information."""
    name: str = Field(description="Full name")
    email: str = Field(description="Email address")
    phone: str | None = Field(default=None, description="Phone number if present")
    role: str | None = Field(default=None, description="Job title or role")

agent = create_agent(
    model="openai:gpt-4o",
    tools=[],  # No tools needed for pure extraction
    response_format=ToolStrategy(PersonInfo),
    system_prompt="Extract person information from the given text."
)

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "Contact: John Doe, Software Engineer at Acme Corp, john.doe@acme.com, (555) 123-4567"
    }]
})

person = result["structured_response"]
print(f"Name: {person.name}, Email: {person.email}")
```

### Classification Agent
```python
from typing import Literal

class SupportTicketClassification(BaseModel):
    """Support ticket classification."""
    category: Literal["bug", "feature_request", "question", "complaint"] = Field(
        description="Type of support ticket"
    )
    priority: Literal["low", "medium", "high", "critical"] = Field(
        description="Ticket priority level"
    )
    department: Literal["engineering", "sales", "support", "billing"] = Field(
        description="Department that should handle this"
    )
    sentiment: Literal["positive", "neutral", "negative"] = Field(
        description="Customer sentiment"
    )

agent = create_agent(
    model="anthropic:claude-sonnet-4-5",
    tools=[],
    response_format=ToolStrategy(SupportTicketClassification),
    system_prompt="Analyze support tickets and classify them accurately."
)

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "URGENT: The payment system is completely broken! I can't process any orders!"
    }]
})

classification = result["structured_response"]
print(f"Category: {classification.category}, Priority: {classification.priority}")
```

---

## Agents with Custom State

### Conversation Agent with User Preferences
```python
from langchain.agents import AgentState
from typing import TypedDict

class ConversationState(AgentState):
    """Extended state with user preferences."""
    user_name: str
    preferences: dict
    conversation_count: int

@tool
def update_preference(
    key: str,
    value: str,
    runtime: ToolRuntime
) -> str:
    """Update user preferences."""
    # Return Command to update state
    from langgraph.types import Command
    
    current_prefs = runtime.state.get("preferences", {})
    current_prefs[key] = value
    
    return Command(update={"preferences": current_prefs})

agent = create_agent(
    model="openai:gpt-4o",
    tools=[update_preference],
    state_schema=ConversationState,
    system_prompt="You are a personalized assistant. Remember user preferences."
)

# First conversation
result = agent.invoke({
    "messages": [{"role": "user", "content": "I prefer technical explanations"}],
    "user_name": "Alice",
    "preferences": {},
    "conversation_count": 0
})
```

### Session-Based Agent
```python
from datetime import datetime

class SessionState(AgentState):
    """State with session tracking."""
    session_id: str
    started_at: str
    actions_taken: list[str]

@tool
def log_action(action: str, runtime: ToolRuntime) -> str:
    """Log an action taken in this session."""
    from langgraph.types import Command
    
    actions = runtime.state.get("actions_taken", [])
    actions.append(f"{datetime.now().isoformat()}: {action}")
    
    return Command(update={"actions_taken": actions})

agent = create_agent(
    model="anthropic:claude-sonnet-4-5",
    tools=[log_action],
    state_schema=SessionState
)
```

---

## Multi-Tool Agents

### Customer Service Agent
```python
@tool
def lookup_order(order_id: str) -> str:
    """Look up order details by order ID."""
    return f"Order {order_id}: Status - Shipped, ETA - 2 days"

@tool
def check_inventory(product_id: str) -> str:
    """Check product inventory levels."""
    return f"Product {product_id}: 150 units in stock"

@tool
def create_return_label(order_id: str, reason: str) -> str:
    """Generate a return shipping label.
    
    Args:
        order_id: The order number
        reason: Reason for return
    """
    return f"Return label created for order {order_id}. Reason: {reason}"

@tool
def escalate_to_human(summary: str) -> str:
    """Escalate complex issues to human support.
    
    Args:
        summary: Brief summary of the issue
    """
    return f"Ticket created and assigned to support team. Summary: {summary}"

agent = create_agent(
    model="openai:gpt-4o",
    tools=[lookup_order, check_inventory, create_return_label, escalate_to_human],
    system_prompt="""You are a customer service agent.
    
    Guidelines:
    - Be helpful and empathetic
    - Look up order information when needed
    - Help with returns and exchanges
    - Escalate to human support if the issue is complex or the customer is frustrated
    """
)

# Example interactions
result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "I want to return order #12345 because it arrived damaged"
    }]
})
```

### Data Analysis Agent
```python
@tool
def query_database(sql_query: str) -> str:
    """Execute a SQL query against the database.
    
    Args:
        sql_query: Valid SQL SELECT statement
    """
    # Validate and execute query
    return "Query results: [...]"

@tool
def create_visualization(data_description: str, chart_type: str) -> str:
    """Create a data visualization.
    
    Args:
        data_description: Description of the data to visualize
        chart_type: Type of chart (bar, line, pie, scatter)
    """
    return f"Created {chart_type} chart for {data_description}"

@tool
def calculate_statistics(metric: str, data_source: str) -> str:
    """Calculate statistical metrics.
    
    Args:
        metric: The metric to calculate (mean, median, std, correlation)
        data_source: The data source to analyze
    """
    return f"Statistics for {metric} on {data_source}: ..."

agent = create_agent(
    model="anthropic:claude-sonnet-4-5",
    tools=[query_database, create_visualization, calculate_statistics],
    system_prompt="""You are a data analyst assistant.
    
    Workflow:
    1. Query the database to get relevant data
    2. Calculate necessary statistics
    3. Create visualizations if helpful
    4. Provide clear insights and recommendations
    """
)
```

---

## Context-Aware Agents

### User-Aware Agent with Context
```python
from typing import TypedDict

class UserContext(TypedDict):
    user_id: str
    role: str
    department: str
    permissions: list[str]

@tool
def access_sensitive_data(
    data_type: str,
    runtime: ToolRuntime[UserContext]
) -> str:
    """Access sensitive data (requires proper permissions)."""
    user_role = runtime.context.role
    permissions = runtime.context.permissions
    
    if "admin" in permissions or data_type in permissions:
        return f"Sensitive {data_type} data: [REDACTED FOR DEMO]"
    else:
        return f"Access denied. User role '{user_role}' lacks permission for {data_type}"

@tool
def get_department_info(runtime: ToolRuntime[UserContext]) -> str:
    """Get information about the user's department."""
    dept = runtime.context.department
    return f"Department: {dept}, Team size: 25, Location: Building B"

agent = create_agent(
    model="openai:gpt-4o",
    tools=[access_sensitive_data, get_department_info],
    context_schema=UserContext,
    system_prompt="You are an enterprise assistant. Respect user permissions."
)

# Invoke with context
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Show me salary data"}]},
    context={
        "user_id": "user123",
        "role": "manager",
        "department": "Engineering",
        "permissions": ["salary_data", "performance_reviews"]
    }
)
```

### Tenant-Aware Multi-Tenant Agent
```python
class TenantContext(TypedDict):
    tenant_id: str
    subscription_tier: str
    feature_flags: dict

@tool
def get_tenant_data(
    query: str,
    runtime: ToolRuntime[TenantContext]
) -> str:
    """Get data scoped to the current tenant."""
    tenant_id = runtime.context.tenant_id
    tier = runtime.context.subscription_tier
    
    # Scope queries by tenant
    return f"Data for tenant {tenant_id} (tier: {tier}): {query} results"

@tool
def check_feature_availability(
    feature_name: str,
    runtime: ToolRuntime[TenantContext]
) -> str:
    """Check if a feature is available for this tenant."""
    flags = runtime.context.feature_flags
    tier = runtime.context.subscription_tier
    
    if feature_name in flags and flags[feature_name]:
        return f"Feature '{feature_name}' is enabled"
    elif tier == "enterprise":
        return f"Feature '{feature_name}' is available in enterprise tier"
    else:
        return f"Feature '{feature_name}' requires an upgrade"

agent = create_agent(
    model="anthropic:claude-sonnet-4-5",
    tools=[get_tenant_data, check_feature_availability],
    context_schema=TenantContext
)
```

---

## Production Patterns

### Resilient Agent with Error Handling
```python
from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage

@wrap_tool_call
def handle_tool_errors(request, handler):
    """Robust error handling for all tools."""
    try:
        return handler(request)
    except ValueError as e:
        # Validation errors - recoverable
        return ToolMessage(
            content=f"Invalid input: {str(e)}. Please check your parameters and try again.",
            tool_call_id=request.tool_call["id"]
        )
    except ConnectionError as e:
        # Network errors - potentially retryable
        return ToolMessage(
            content=f"Connection error: {str(e)}. The service may be temporarily unavailable.",
            tool_call_id=request.tool_call["id"]
        )
    except Exception as e:
        # Unexpected errors
        logger.error(f"Tool execution error: {e}", exc_info=True)
        return ToolMessage(
            content=f"An unexpected error occurred. Please try a different approach.",
            tool_call_id=request.tool_call["id"]
        )

agent = create_agent(
    model="openai:gpt-4o",
    tools=[database_tool, api_tool],
    middleware=[handle_tool_errors]
)
```

### Agent with Dynamic Model Selection
```python
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain_openai import ChatOpenAI

# Different models for different scenarios
fast_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
smart_model = ChatOpenAI(model="gpt-4o", temperature=0.7)
reasoning_model = ChatOpenAI(model="o3-mini", temperature=1.0)

@wrap_model_call
def select_model_by_complexity(request: ModelRequest, handler) -> ModelResponse:
    """Choose model based on task complexity."""
    messages = request.state["messages"]
    last_message = messages[-1].content if messages else ""
    
    # Use reasoning model for complex analytical tasks
    if any(keyword in last_message.lower() for keyword in ["analyze", "compare", "evaluate", "explain why"]):
        request.model = reasoning_model
    # Use smart model for creative tasks
    elif any(keyword in last_message.lower() for keyword in ["create", "design", "write", "generate"]):
        request.model = smart_model
    # Use fast model for simple tasks
    else:
        request.model = fast_model
    
    return handler(request)

agent = create_agent(
    model=fast_model,  # Default
    tools=[search_tool, calculator_tool],
    middleware=[select_model_by_complexity]
)
```

### Agent with Observability (LangSmith)
```python
import os
from langsmith import Client

# Set up LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "production-agents"

# Create agent with automatic tracing
agent = create_agent(
    model="openai:gpt-4o",
    tools=[tool1, tool2, tool3],
    system_prompt="Production agent with full observability"
)

# All invocations are automatically traced
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Process this request"}]},
    config={
        "run_name": "customer_request_processing",
        "tags": ["production", "customer-facing"],
        "metadata": {
            "customer_id": "cust_12345",
            "request_type": "order_inquiry"
        }
    }
)

# View traces at: https://smith.langchain.com/
```

### Agent with Rate Limiting
```python
from langchain_core.rate_limiters import InMemoryRateLimiter

# Create rate limiter: 10 requests per minute
rate_limiter = InMemoryRateLimiter(
    requests_per_second=10/60,  # 10 per minute
    check_every_n_seconds=0.1
)

# Initialize model with rate limiter
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4o",
    rate_limiter=rate_limiter
)

agent = create_agent(
    model=model,
    tools=[expensive_api_tool],
    system_prompt="Agent with controlled API usage"
)
```

### Agent with Streaming Progress Updates
```python
from langchain.tools import tool, ToolRuntime

@tool
def long_running_task(
    task_description: str,
    runtime: ToolRuntime
) -> str:
    """Execute a long-running task with progress updates."""
    writer = runtime.stream_writer
    
    writer("Starting task...")
    # Simulate work
    time.sleep(1)
    
    writer("Processing data (25% complete)")
    time.sleep(1)
    
    writer("Analyzing results (50% complete)")
    time.sleep(1)
    
    writer("Finalizing output (75% complete)")
    time.sleep(1)
    
    writer("Task complete!")
    return f"Completed: {task_description}"

agent = create_agent(
    model="anthropic:claude-sonnet-4-5",
    tools=[long_running_task]
)

# Stream the execution
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "Run the analytics report"}]},
    stream_mode="values"
):
    print(chunk)  # See progress updates in real-time
```

## Best Practices Summary

1. **Clear System Prompts**: Provide explicit instructions about agent behavior and capabilities
2. **Tool Descriptions**: Write clear, detailed docstrings - they guide the model's tool selection
3. **Error Handling**: Use middleware to catch and handle errors gracefully
4. **Context Awareness**: Leverage `ToolRuntime` for user context and permissions
5. **Model Selection**: Use appropriate models for different task complexities
6. **Observability**: Integrate LangSmith for production monitoring and debugging
7. **Rate Limiting**: Protect external APIs with rate limiters
8. **Streaming**: Provide real-time feedback for long-running operations
9. **State Management**: Use custom state for multi-turn conversations and session data
10. **Testing**: Test tools independently before integrating into agents
