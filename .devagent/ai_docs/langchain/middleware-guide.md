# LangChain Middleware Guide

Comprehensive guide to using middleware for customizing agent behavior in LangChain.

## Table of Contents
1. [Middleware Overview](#middleware-overview)
2. [Model Middleware](#model-middleware)
3. [Tool Middleware](#tool-middleware)
4. [Dynamic Prompts](#dynamic-prompts)
5. [Common Patterns](#common-patterns)
6. [Production Examples](#production-examples)

---

## Middleware Overview

Middleware in LangChain allows you to intercept and modify agent execution at various points. This enables cross-cutting concerns like logging, error handling, model selection, and guardrails.

### Available Middleware Hooks

```python
from langchain.agents.middleware import (
    before_model,        # Run before model invocation
    after_model,         # Run after model response
    wrap_model_call,     # Wrap entire model call
    wrap_tool_call,      # Wrap tool execution
    dynamic_prompt,      # Generate system prompts dynamically
)
```

### How Middleware Works

```python
from langchain.agents import create_agent

agent = create_agent(
    model="openai:gpt-4o",
    tools=[my_tool],
    middleware=[
        my_middleware_1,  # Executes first
        my_middleware_2,  # Executes second
        my_middleware_3,  # Executes third
    ]
)
```

Middleware executes in order for "before" hooks and reverse order for "after" hooks.

---

## Model Middleware

### Before Model Hook

Runs before the model is invoked:

```python
from langchain.agents.middleware import before_model, ModelRequest

@before_model
def log_before_model(request: ModelRequest):
    """Log information before model call."""
    messages = request.state["messages"]
    print(f"Calling model with {len(messages)} messages")
    print(f"Last message: {messages[-1].content}")
    
    # You can modify the request here
    # But don't return anything for before_model
```

### After Model Hook

Runs after the model responds:

```python
from langchain.agents.middleware import after_model, ModelResponse

@after_model
def log_after_model(response: ModelResponse):
    """Log model response information."""
    print(f"Model responded with: {response.message.content[:100]}...")
    
    if response.message.usage_metadata:
        tokens = response.message.usage_metadata['total_tokens']
        print(f"Tokens used: {tokens}")
    
    # Don't return anything for after_model
```

### Wrap Model Call

Wraps the entire model invocation with before/after logic:

```python
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse

@wrap_model_call
def timing_middleware(request: ModelRequest, handler) -> ModelResponse:
    """Measure model call latency."""
    import time
    
    start = time.time()
    
    # Call the actual model
    response = handler(request)
    
    elapsed = time.time() - start
    print(f"Model call took {elapsed:.2f}s")
    
    return response
```

### Dynamic Model Selection

```python
from langchain_openai import ChatOpenAI

fast_model = ChatOpenAI(model="gpt-4o-mini")
smart_model = ChatOpenAI(model="gpt-4o")
reasoning_model = ChatOpenAI(model="o3-mini")

@wrap_model_call
def select_model_by_complexity(request: ModelRequest, handler) -> ModelResponse:
    """Choose model based on query complexity."""
    messages = request.state["messages"]
    last_content = messages[-1].content.lower() if messages else ""
    
    # Reasoning tasks
    if any(word in last_content for word in ["analyze", "compare", "evaluate", "why"]):
        request.model = reasoning_model
        print("Using reasoning model")
    # Complex tasks
    elif any(word in last_content for word in ["create", "design", "write"]):
        request.model = smart_model
        print("Using smart model")
    # Simple tasks
    else:
        request.model = fast_model
        print("Using fast model")
    
    return handler(request)

agent = create_agent(
    model=fast_model,  # Default
    tools=[search_tool],
    middleware=[select_model_by_complexity]
)
```

### Model Call with Retries

```python
import time

@wrap_model_call
def retry_on_error(request: ModelRequest, handler, max_retries=3) -> ModelResponse:
    """Retry failed model calls with exponential backoff."""
    from langchain_core.exceptions import RateLimitError
    
    for attempt in range(max_retries):
        try:
            return handler(request)
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Rate limited. Retrying in {wait_time}s...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
```

---

## Tool Middleware

### Wrap Tool Call

Intercept and handle tool executions:

```python
from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage

@wrap_tool_call
def handle_tool_errors(request, handler):
    """Gracefully handle tool execution errors."""
    try:
        return handler(request)
    except ValueError as e:
        # Input validation errors
        return ToolMessage(
            content=f"Invalid input: {str(e)}. Please check your parameters.",
            tool_call_id=request.tool_call["id"]
        )
    except ConnectionError as e:
        # Network/API errors
        return ToolMessage(
            content=f"Service temporarily unavailable: {str(e)}",
            tool_call_id=request.tool_call["id"]
        )
    except Exception as e:
        # Unexpected errors
        import logging
        logging.error(f"Tool error: {e}", exc_info=True)
        return ToolMessage(
            content="An unexpected error occurred. Please try again or use a different approach.",
            tool_call_id=request.tool_call["id"]
        )

agent = create_agent(
    model="openai:gpt-4o",
    tools=[database_tool, api_tool],
    middleware=[handle_tool_errors]
)
```

### Tool Logging and Monitoring

```python
@wrap_tool_call
def log_tool_calls(request, handler):
    """Log tool execution for monitoring."""
    tool_name = request.tool_call.get("name", "unknown")
    tool_args = request.tool_call.get("args", {})
    
    print(f"Executing tool: {tool_name}")
    print(f"Arguments: {tool_args}")
    
    import time
    start = time.time()
    
    result = handler(request)
    
    elapsed = time.time() - start
    print(f"Tool '{tool_name}' completed in {elapsed:.2f}s")
    
    return result
```

### Tool Access Control

```python
from typing import TypedDict

class UserContext(TypedDict):
    user_id: str
    role: str
    permissions: list[str]

@wrap_tool_call
def enforce_permissions(request, handler):
    """Check permissions before executing tools."""
    from langchain_core.messages import ToolMessage
    
    tool_name = request.tool_call.get("name", "")
    runtime = request.runtime
    
    # Check if user has permission for this tool
    permissions = runtime.context.get("permissions", [])
    
    # Define tool permission requirements
    tool_permissions = {
        "delete_data": ["admin"],
        "access_sensitive_data": ["admin", "manager"],
        "export_report": ["admin", "manager", "analyst"],
    }
    
    required_perms = tool_permissions.get(tool_name, [])
    
    if required_perms and not any(p in permissions for p in required_perms):
        return ToolMessage(
            content=f"Access denied. Tool '{tool_name}' requires one of: {required_perms}",
            tool_call_id=request.tool_call["id"]
        )
    
    return handler(request)

agent = create_agent(
    model="openai:gpt-4o",
    tools=[delete_data, access_sensitive_data, export_report],
    context_schema=UserContext,
    middleware=[enforce_permissions]
)
```

---

## Dynamic Prompts

### Basic Dynamic Prompt

```python
from langchain.agents.middleware import dynamic_prompt, ModelRequest

@dynamic_prompt
def context_aware_prompt(request: ModelRequest) -> str:
    """Generate system prompt based on context."""
    context = request.runtime.context
    user_role = context.get("role", "user")
    
    if user_role == "admin":
        return "You are an admin assistant with full system access. You can perform any operation."
    elif user_role == "manager":
        return "You are a manager assistant. You have elevated privileges for reporting and analytics."
    else:
        return "You are a helpful assistant. You can answer questions and perform basic tasks."

agent = create_agent(
    model="openai:gpt-4o",
    tools=[my_tools],
    middleware=[context_aware_prompt]
)
```

### Time-Aware Prompts

```python
from datetime import datetime

@dynamic_prompt
def time_aware_prompt(request: ModelRequest) -> str:
    """Adjust prompt based on time of day."""
    hour = datetime.now().hour
    
    if 0 <= hour < 6:
        return "You are a helpful night assistant. Keep responses concise as users may be tired."
    elif 6 <= hour < 12:
        return "You are an energetic morning assistant. Be helpful and encouraging!"
    elif 12 <= hour < 18:
        return "You are a productive afternoon assistant. Focus on getting things done efficiently."
    else:
        return "You are a friendly evening assistant. Be helpful but mindful that it's late."
```

### State-Based Prompts

```python
@dynamic_prompt
def state_based_prompt(request: ModelRequest) -> str:
    """Generate prompt based on conversation state."""
    messages = request.state.get("messages", [])
    message_count = len(messages)
    
    if message_count <= 2:
        return """You are a welcoming assistant starting a new conversation.
        - Introduce yourself briefly
        - Understand the user's needs
        - Offer to help"""
    elif message_count < 10:
        return """You are an engaged assistant in an active conversation.
        - Build on previous context
        - Ask clarifying questions if needed
        - Provide detailed, helpful responses"""
    else:
        return """You are an assistant in a lengthy conversation.
        - Reference earlier parts of the conversation when relevant
        - Offer to summarize if the conversation is getting complex
        - Check if the user needs anything else"""
```

### Multi-Language Prompts

```python
@dynamic_prompt
def multilingual_prompt(request: ModelRequest) -> str:
    """Adjust prompt based on user language preference."""
    context = request.runtime.context
    language = context.get("language", "en")
    
    prompts = {
        "en": "You are a helpful assistant. Respond in clear, professional English.",
        "es": "Eres un asistente útil. Responde en español claro y profesional.",
        "fr": "Vous êtes un assistant utile. Répondez en français clair et professionnel.",
        "de": "Sie sind ein hilfreicher Assistent. Antworten Sie in klarem, professionellem Deutsch.",
    }
    
    return prompts.get(language, prompts["en"])
```

---

## Common Patterns

### Logging and Observability

```python
import logging

logger = logging.getLogger(__name__)

@wrap_model_call
def comprehensive_logging(request: ModelRequest, handler) -> ModelResponse:
    """Log detailed information about model calls."""
    import time
    
    # Log request
    messages = request.state["messages"]
    logger.info(f"Model call started with {len(messages)} messages")
    
    start = time.time()
    
    try:
        response = handler(request)
        
        # Log success
        elapsed = time.time() - start
        tokens = response.message.usage_metadata.get('total_tokens', 0) if response.message.usage_metadata else 0
        
        logger.info(f"Model call succeeded in {elapsed:.2f}s, used {tokens} tokens")
        
        return response
    
    except Exception as e:
        # Log error
        elapsed = time.time() - start
        logger.error(f"Model call failed after {elapsed:.2f}s: {e}", exc_info=True)
        raise
```

### Content Filtering (Guardrails)

```python
@wrap_model_call
def content_filter(request: ModelRequest, handler) -> ModelResponse:
    """Filter sensitive content from responses."""
    response = handler(request)
    
    # Check for sensitive content
    content = response.message.content.lower()
    sensitive_words = ["password", "api_key", "secret", "token"]
    
    if any(word in content for word in sensitive_words):
        # Redact sensitive information
        for word in sensitive_words:
            response.message.content = response.message.content.replace(word, "[REDACTED]")
        
        logger.warning("Redacted sensitive content from response")
    
    return response
```

### Caching Responses

```python
from functools import lru_cache
import hashlib
import json

# Simple in-memory cache
response_cache = {}

@wrap_model_call
def cache_responses(request: ModelRequest, handler) -> ModelResponse:
    """Cache model responses for identical requests."""
    # Create cache key from messages
    messages_str = json.dumps([
        {"role": m.__class__.__name__, "content": str(m.content)}
        for m in request.state["messages"]
    ])
    cache_key = hashlib.md5(messages_str.encode()).hexdigest()
    
    # Check cache
    if cache_key in response_cache:
        print("Cache hit!")
        return response_cache[cache_key]
    
    # Call model
    response = handler(request)
    
    # Store in cache
    response_cache[cache_key] = response
    
    return response
```

---

## Production Examples

### Complete Production Middleware Stack

```python
from langchain.agents import create_agent
from langchain.agents.middleware import (
    wrap_model_call,
    wrap_tool_call,
    dynamic_prompt,
)
import logging
import time

logger = logging.getLogger(__name__)

# 1. Dynamic prompt based on context
@dynamic_prompt
def production_prompt(request: ModelRequest) -> str:
    """Generate context-aware system prompts."""
    role = request.runtime.context.get("role", "user")
    environment = request.runtime.context.get("environment", "production")
    
    base_prompt = "You are a professional assistant for enterprise users."
    
    if environment == "development":
        base_prompt += " You're in development mode - be verbose with explanations."
    
    if role == "admin":
        base_prompt += " You have administrative privileges."
    
    return base_prompt

# 2. Model call monitoring and retry
@wrap_model_call
def production_model_middleware(request: ModelRequest, handler) -> ModelResponse:
    """Production-ready model call handling."""
    start = time.time()
    
    try:
        response = handler(request)
        
        # Log metrics
        elapsed = time.time() - start
        tokens = response.message.usage_metadata.get('total_tokens', 0) if response.message.usage_metadata else 0
        
        logger.info(f"Model call: {elapsed:.2f}s, {tokens} tokens")
        
        return response
    
    except Exception as e:
        logger.error(f"Model call failed: {e}", exc_info=True)
        raise

# 3. Tool error handling and logging
@wrap_tool_call
def production_tool_middleware(request, handler):
    """Production-ready tool execution."""
    tool_name = request.tool_call.get("name", "unknown")
    
    logger.info(f"Executing tool: {tool_name}")
    start = time.time()
    
    try:
        result = handler(request)
        elapsed = time.time() - start
        logger.info(f"Tool '{tool_name}' succeeded in {elapsed:.2f}s")
        return result
    
    except Exception as e:
        elapsed = time.time() - start
        logger.error(f"Tool '{tool_name}' failed after {elapsed:.2f}s: {e}", exc_info=True)
        
        from langchain_core.messages import ToolMessage
        return ToolMessage(
            content=f"Tool error: {str(e)}",
            tool_call_id=request.tool_call["id"]
        )

# Create agent with production middleware
agent = create_agent(
    model="openai:gpt-4o",
    tools=[search_tool, database_tool, api_tool],
    middleware=[
        production_prompt,
        production_model_middleware,
        production_tool_middleware,
    ]
)
```

### Integration with LangSmith

```python
import os

# Enable LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "production-agents"

@wrap_model_call
def langsmith_metadata(request: ModelRequest, handler) -> ModelResponse:
    """Add custom metadata to LangSmith traces."""
    # Metadata is automatically captured by LangSmith
    # You can add custom tags via config parameter
    return handler(request)

# Use with custom tags
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Hello"}]},
    config={
        "run_name": "customer_interaction",
        "tags": ["production", "customer-facing"],
        "metadata": {
            "customer_id": "cust_12345",
            "interaction_type": "support_query"
        }
    }
)
```

---

## Best Practices

1. **Order matters**: Place middleware in logical order (auth → validation → logging → execution)
2. **Return properly**: `@wrap_*` hooks must return values, `@before_*` and `@after_*` should not
3. **Handle errors**: Always catch and handle exceptions in middleware
4. **Log appropriately**: Use appropriate log levels (info, warning, error)
5. **Keep it focused**: Each middleware should have a single responsibility
6. **Test independently**: Test middleware functions separately before integration
7. **Document behavior**: Clearly document what each middleware does
8. **Monitor performance**: Be aware of latency added by middleware
9. **Use context**: Leverage `runtime.context` for user-specific behavior
10. **Fail gracefully**: Don't let middleware failures break the entire agent

---

## Production Integration Examples

Common middleware patterns for production applications:

```python
# Error handling for LLM operations
@wrap_model_call
def production_error_handling(request, handler):
    """Handle errors in LLM operations with proper logging."""
    try:
        return handler(request)
    except Exception as e:
        logger.error(f"LLM operation failed: {e}")
        # Fallback behavior
        raise

# Token usage tracking
@wrap_model_call
def track_token_usage(request, handler):
    """Track token usage for cost monitoring."""
    response = handler(request)
    
    if response.message.usage_metadata:
        tokens = response.message.usage_metadata['total_tokens']
        # Log to monitoring system
        logger.info(f"Tokens used: {tokens}")
    
    return response
```

---

## Integration with Project

In NileGPT, middleware can be used for:

```python
# Error handling for LLM operations
@wrap_model_call
def nilegpt_error_handling(request, handler):
    """Handle errors in NileGPT LLM operations."""
    try:
        return handler(request)
    except Exception as e:
        logger.error(f"LLM operation failed: {e}")
        # Fallback behavior
        raise

# Token usage tracking
@wrap_model_call
def track_token_usage(request, handler):
    """Track token usage for cost monitoring."""
    response = handler(request)
    
    if response.message.usage_metadata:
        tokens = response.message.usage_metadata['total_tokens']
        # Log to monitoring system
        logger.info(f"Tokens used: {tokens}")
    
    return response
```
