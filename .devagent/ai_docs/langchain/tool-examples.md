# LangChain Tool Creation Guide

Comprehensive examples for creating tools in LangChain, from basic to advanced patterns.

## Table of Contents
1. [Basic Tools](#basic-tools)
2. [Tools with Complex Schemas](#tools-with-complex-schemas)
3. [Tools with Runtime Context](#tools-with-runtime-context)
4. [Async Tools](#async-tools)
5. [Tool Error Handling](#tool-error-handling)
6. [Tool Testing](#tool-testing)

---

## Basic Tools

### Simple Function Tool
```python
from langchain.tools import tool

@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression.
    
    Args:
        expression: A math expression like "2 + 2" or "10 * 5"
    """
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

# The tool automatically has:
# - name: "calculator"
# - description: from docstring
# - args_schema: from type hints
```

### Tool with Custom Name
```python
@tool("web_search")
def search(query: str, max_results: int = 10) -> str:
    """Search the web for information.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return
    """
    return f"Top {max_results} results for '{query}'"

print(search.name)  # "web_search"
```

### Tool with Multiple Parameters
```python
@tool
def send_email(
    recipient: str,
    subject: str,
    body: str,
    cc: str | None = None
) -> str:
    """Send an email to a recipient.
    
    Args:
        recipient: Email address of the recipient
        subject: Email subject line
        body: Email message body
        cc: Optional CC email address
    """
    cc_info = f" (CC: {cc})" if cc else ""
    return f"Email sent to {recipient}{cc_info}: {subject}"
```

---

## Tools with Complex Schemas

### Using Pydantic for Advanced Validation
```python
from pydantic import BaseModel, Field, field_validator
from typing import Literal

class WeatherQuery(BaseModel):
    """Input schema for weather queries."""
    
    location: str = Field(
        description="City name or ZIP code",
        examples=["New York", "90210"]
    )
    units: Literal["celsius", "fahrenheit"] = Field(
        default="fahrenheit",
        description="Temperature unit"
    )
    days: int = Field(
        default=1,
        ge=1,
        le=10,
        description="Number of days to forecast (1-10)"
    )
    include_hourly: bool = Field(
        default=False,
        description="Include hourly breakdown"
    )
    
    @field_validator("location")
    @classmethod
    def validate_location(cls, v: str) -> str:
        if len(v) < 2:
            raise ValueError("Location must be at least 2 characters")
        return v.strip()

@tool(args_schema=WeatherQuery)
def get_weather(
    location: str,
    units: str = "fahrenheit",
    days: int = 1,
    include_hourly: bool = False
) -> str:
    """Get weather forecast for a location."""
    forecast = f"Weather in {location} ({units}):\\n"
    forecast += f"{days}-day forecast"
    if include_hourly:
        forecast += " with hourly breakdown"
    return forecast

# Tool now has full Pydantic validation
```

### Nested Schema Tool
```python
from typing import Annotated

class Address(BaseModel):
    """Address information."""
    street: str = Field(description="Street address")
    city: str = Field(description="City name")
    state: str = Field(description="Two-letter state code", min_length=2, max_length=2)
    zip_code: str = Field(description="ZIP code", pattern=r"^\d{5}(-\d{4})?$")

class CustomerData(BaseModel):
    """Customer information."""
    name: str = Field(description="Full name")
    email: str = Field(description="Email address", pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    phone: str = Field(description="Phone number")
    address: Address = Field(description="Mailing address")
    preferred_contact: Literal["email", "phone", "mail"] = Field(
        default="email",
        description="Preferred contact method"
    )

@tool(args_schema=CustomerData)
def create_customer(
    name: str,
    email: str,
    phone: str,
    address: Address,
    preferred_contact: str = "email"
) -> str:
    """Create a new customer record."""
    return f"Customer created: {name} at {address.city}, {address.state}"
```

### Enum-Based Tool
```python
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TaskInput(BaseModel):
    """Task creation input."""
    title: str = Field(description="Task title")
    description: str = Field(description="Detailed description")
    priority: Priority = Field(
        default=Priority.MEDIUM,
        description="Task priority level"
    )
    assignee: str | None = Field(
        default=None,
        description="Person assigned to task"
    )
    due_date: str | None = Field(
        default=None,
        description="Due date in YYYY-MM-DD format",
        pattern=r"^\d{4}-\d{2}-\d{2}$"
    )

@tool(args_schema=TaskInput)
def create_task(
    title: str,
    description: str,
    priority: Priority = Priority.MEDIUM,
    assignee: str | None = None,
    due_date: str | None = None
) -> str:
    """Create a new task in the project management system."""
    task = f"Task: {title} (Priority: {priority.value})"
    if assignee:
        task += f" - Assigned to {assignee}"
    if due_date:
        task += f" - Due: {due_date}"
    return task
```

---

## Tools with Runtime Context

### Accessing Agent State
```python
from langchain.tools import tool, ToolRuntime

@tool
def get_conversation_summary(runtime: ToolRuntime) -> str:
    """Summarize the current conversation."""
    messages = runtime.state["messages"]
    
    # Count message types
    human_count = sum(1 for m in messages if m.__class__.__name__ == "HumanMessage")
    ai_count = sum(1 for m in messages if m.__class__.__name__ == "AIMessage")
    tool_count = sum(1 for m in messages if m.__class__.__name__ == "ToolMessage")
    
    return f"""Conversation Summary:
- User messages: {human_count}
- AI responses: {ai_count}
- Tool calls: {tool_count}
- Total messages: {len(messages)}"""

@tool
def get_last_user_message(runtime: ToolRuntime) -> str:
    """Get the most recent user message."""
    messages = runtime.state["messages"]
    
    # Find last HumanMessage
    for message in reversed(messages):
        if message.__class__.__name__ == "HumanMessage":
            return f"Last user said: {message.content}"
    
    return "No user messages found"
```

### Accessing User Context
```python
from typing import TypedDict

class UserContext(TypedDict):
    user_id: str
    username: str
    role: str
    permissions: list[str]

@tool
def get_user_profile(runtime: ToolRuntime[UserContext]) -> str:
    """Get the current user's profile information."""
    context = runtime.context
    
    return f"""User Profile:
- ID: {context.user_id}
- Username: {context.username}
- Role: {context.role}
- Permissions: {', '.join(context.permissions)}"""

@tool
def check_permission(
    required_permission: str,
    runtime: ToolRuntime[UserContext]
) -> str:
    """Check if the current user has a specific permission."""
    permissions = runtime.context.permissions
    
    if required_permission in permissions:
        return f"✓ User has '{required_permission}' permission"
    else:
        return f"✗ User lacks '{required_permission}' permission"
```

### Using Long-Term Memory (Store)
```python
from typing import Any

@tool
def save_user_preference(
    key: str,
    value: str,
    runtime: ToolRuntime
) -> str:
    """Save a user preference to long-term memory."""
    store = runtime.store
    user_id = runtime.context.get("user_id", "default")
    
    # Store in memory
    store.put(("preferences", user_id), key, value)
    
    return f"Saved preference: {key} = {value}"

@tool
def get_user_preference(
    key: str,
    runtime: ToolRuntime
) -> str:
    """Retrieve a user preference from long-term memory."""
    store = runtime.store
    user_id = runtime.context.get("user_id", "default")
    
    # Retrieve from memory
    item = store.get(("preferences", user_id), key)
    
    if item:
        return f"{key}: {item.value}"
    else:
        return f"No preference found for key: {key}"

@tool
def list_user_preferences(runtime: ToolRuntime) -> str:
    """List all user preferences."""
    store = runtime.store
    user_id = runtime.context.get("user_id", "default")
    
    # Search for all preferences
    items = store.search(("preferences", user_id))
    
    if not items:
        return "No preferences saved"
    
    prefs = [f"{item.key}: {item.value}" for item in items]
    return "User Preferences:\\n" + "\\n".join(prefs)
```

### Updating Agent State
```python
from langgraph.types import Command

@tool
def update_user_score(
    points: int,
    runtime: ToolRuntime
) -> Command:
    """Add points to the user's score."""
    current_score = runtime.state.get("user_score", 0)
    new_score = current_score + points
    
    return Command(
        update={"user_score": new_score},
        message=f"Added {points} points. New score: {new_score}"
    )

@tool
def clear_conversation_history() -> Command:
    """Clear the conversation history."""
    from langchain.messages import RemoveMessage
    from langgraph.graph.message import REMOVE_ALL_MESSAGES
    
    return Command(
        update={"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES)]},
        message="Conversation history cleared"
    )

@tool
def set_conversation_mode(
    mode: Literal["casual", "professional", "technical"],
    runtime: ToolRuntime
) -> Command:
    """Change the conversation mode."""
    return Command(
        update={"conversation_mode": mode},
        message=f"Switched to {mode} mode"
    )
```

---

## Async Tools

### Basic Async Tool
```python
import asyncio
from langchain.tools import tool

@tool
async def async_web_search(query: str) -> str:
    """Asynchronously search the web."""
    # Simulate async API call
    await asyncio.sleep(1)
    return f"Async search results for: {query}"

@tool
async def fetch_user_data(user_id: str) -> str:
    """Fetch user data from async database."""
    # Simulate async database query
    await asyncio.sleep(0.5)
    return f"User data for ID {user_id}: [...]"
```

### Async Tool with HTTP Requests
```python
import aiohttp

@tool
async def async_api_call(endpoint: str, method: str = "GET") -> str:
    """Make an async HTTP request.
    
    Args:
        endpoint: The API endpoint URL
        method: HTTP method (GET, POST, etc.)
    """
    async with aiohttp.ClientSession() as session:
        async with session.request(method, endpoint) as response:
            data = await response.text()
            return f"Response ({response.status}): {data[:200]}..."

@tool
async def fetch_multiple_urls(urls: list[str]) -> str:
    """Fetch multiple URLs in parallel."""
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        
        results = []
        for url, response in zip(urls, responses):
            data = await response.text()
            results.append(f"{url}: {len(data)} bytes")
        
        return "\\n".join(results)
```

### Async Tool with Streaming Updates
```python
@tool
async def async_long_task(
    task_name: str,
    runtime: ToolRuntime
) -> str:
    """Execute a long-running async task with progress updates."""
    writer = runtime.stream_writer
    
    writer(f"Starting {task_name}...")
    await asyncio.sleep(1)
    
    writer("Processing step 1/3...")
    await asyncio.sleep(1)
    
    writer("Processing step 2/3...")
    await asyncio.sleep(1)
    
    writer("Processing step 3/3...")
    await asyncio.sleep(1)
    
    writer("Complete!")
    return f"Finished {task_name}"
```

---

## Tool Error Handling

### Built-in Error Handling
```python
@tool
def safe_calculator(expression: str) -> str:
    """Safely evaluate a mathematical expression."""
    # Whitelist allowed characters
    allowed_chars = set("0123456789+-*/() .")
    
    if not all(c in allowed_chars for c in expression):
        return "Error: Expression contains invalid characters"
    
    try:
        result = eval(expression)
        return f"Result: {result}"
    except ZeroDivisionError:
        return "Error: Division by zero"
    except SyntaxError:
        return "Error: Invalid syntax"
    except Exception as e:
        return f"Error: {type(e).__name__} - {str(e)}"
```

### Validation with Custom Exceptions
```python
class ToolValidationError(Exception):
    """Custom exception for tool validation failures."""
    pass

@tool
def validate_and_process(
    email: str,
    age: int
) -> str:
    """Process user data with validation.
    
    Args:
        email: User email address
        age: User age (must be 18+)
    """
    # Validate email
    if "@" not in email or "." not in email:
        raise ToolValidationError(f"Invalid email format: {email}")
    
    # Validate age
    if age < 18:
        raise ToolValidationError(f"Age must be 18+, got {age}")
    
    if age > 120:
        raise ToolValidationError(f"Age seems unrealistic: {age}")
    
    return f"Processed user: {email}, age {age}"

# Use with error handling middleware (see agent-patterns.md)
```

### Retry Logic in Tools
```python
import time
from functools import wraps

def retry_on_failure(max_attempts: int = 3, delay: float = 1.0):
    """Decorator to retry failed operations."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

@tool
@retry_on_failure(max_attempts=3, delay=2.0)
def unreliable_api_call(endpoint: str) -> str:
    """Call an unreliable external API."""
    # This will automatically retry up to 3 times
    import requests
    response = requests.get(endpoint, timeout=5)
    response.raise_for_status()
    return f"API response: {response.json()}"
```

---

## Tool Testing

### Unit Testing Tools
```python
import pytest
from langchain.tools import tool

@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

def test_add_numbers():
    """Test the add_numbers tool."""
    # Test basic addition
    result = add_numbers.invoke({"a": 2, "b": 3})
    assert result == 5
    
    # Test negative numbers
    result = add_numbers.invoke({"a": -5, "b": 3})
    assert result == -2
    
    # Test zero
    result = add_numbers.invoke({"a": 0, "b": 0})
    assert result == 0

@tool
def divide_numbers(a: float, b: float) -> str:
    """Divide two numbers."""
    if b == 0:
        return "Error: Division by zero"
    return f"Result: {a / b}"

def test_divide_numbers():
    """Test the divide_numbers tool."""
    # Test normal division
    result = divide_numbers.invoke({"a": 10, "b": 2})
    assert result == "Result: 5.0"
    
    # Test division by zero
    result = divide_numbers.invoke({"a": 10, "b": 0})
    assert "Error" in result
```

### Testing Tools with Mocks
```python
from unittest.mock import Mock, patch

@tool
def fetch_weather_from_api(city: str) -> str:
    """Fetch weather from external API."""
    import requests
    response = requests.get(f"https://api.weather.com/data/{city}")
    return response.json()["temperature"]

def test_fetch_weather_with_mock():
    """Test weather tool with mocked API."""
    with patch('requests.get') as mock_get:
        # Mock the API response
        mock_response = Mock()
        mock_response.json.return_value = {"temperature": "72°F"}
        mock_get.return_value = mock_response
        
        # Test the tool
        result = fetch_weather_from_api.invoke({"city": "Boston"})
        assert result == "72°F"
        
        # Verify the correct endpoint was called
        mock_get.assert_called_once_with("https://api.weather.com/data/Boston")
```

### Testing Async Tools
```python
import pytest

@tool
async def async_fetch_data(source: str) -> str:
    """Async data fetch."""
    await asyncio.sleep(0.1)
    return f"Data from {source}"

@pytest.mark.asyncio
async def test_async_tool():
    """Test async tool execution."""
    result = await async_fetch_data.ainvoke({"source": "database"})
    assert result == "Data from database"
```

### Testing Tools with Runtime Context
```python
from langchain.agents import create_agent

@tool
def context_aware_tool(
    query: str,
    runtime: ToolRuntime
) -> str:
    """Tool that uses runtime context."""
    user_id = runtime.context.get("user_id", "unknown")
    return f"Query '{query}' for user {user_id}"

def test_context_aware_tool():
    """Test tool with agent runtime."""
    class TestContext(TypedDict):
        user_id: str
    
    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[context_aware_tool],
        context_schema=TestContext
    )
    
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "search products"}]},
        context={"user_id": "user123"}
    )
    
    # Verify the tool was called with correct context
    assert "user123" in str(result)
```

## Best Practices

1. **Clear Descriptions**: Write detailed docstrings - they guide model behavior
2. **Type Safety**: Always use type hints for all parameters
3. **Validation**: Use Pydantic for complex schemas with validation
4. **Error Handling**: Return helpful error messages, don't just raise exceptions
5. **Testing**: Test tools independently before using in agents
6. **Async When Needed**: Use async tools for I/O-bound operations
7. **Context Awareness**: Leverage `ToolRuntime` for state and context
8. **Idempotency**: Tools should be safe to call multiple times
9. **Documentation**: Include examples in docstrings for complex tools
10. **Monitoring**: Log tool executions for debugging and observability
