# LangChain Model Integration Guide

Comprehensive guide to initializing and configuring language models in LangChain.

## Table of Contents
1. [Model Initialization](#model-initialization)
2. [Provider-Specific Configuration](#provider-specific-configuration)
3. [Model Parameters](#model-parameters)
4. [Model Selection Strategies](#model-selection-strategies)
5. [Token Management](#token-management)

---

## Model Initialization

### Using `init_chat_model()` (Recommended)

The `init_chat_model()` function provides a provider-agnostic way to initialize models:

```python
from langchain.chat_models import init_chat_model

# Provider inference (works for common models)
model = init_chat_model("gpt-4o")  # Auto-inferred as openai:gpt-4o
model = init_chat_model("claude-sonnet-4-5")  # Auto-inferred as anthropic:claude-sonnet-4-5

# Explicit provider (recommended for clarity)
model = init_chat_model("openai:gpt-5")
model = init_chat_model("anthropic:claude-sonnet-4-5")
model = init_chat_model("google:gemini-2.5-pro")

# With configuration
model = init_chat_model(
    "openai:gpt-4o",
    temperature=0.7,
    max_tokens=2000,
    timeout=30
)
```

### Provider-Specific Initialization

For advanced configuration, use provider-specific classes:

#### OpenAI
```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4o",
    temperature=0.0,
    max_tokens=1000,
    timeout=60,
    max_retries=3,
    api_key="...",  # Or use OPENAI_API_KEY env var
    organization="..."  # Optional organization ID
)
```

#### Anthropic
```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(
    model="claude-sonnet-4-5",
    temperature=1.0,
    max_tokens=4096,
    timeout=30,
    api_key="...",  # Or use ANTHROPIC_API_KEY env var
    # Anthropic-specific parameters
    top_p=0.9,
    top_k=40
)
```

#### Google (Gemini)
```python
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.5,
    max_output_tokens=8192,
    api_key="...",  # Or use GOOGLE_API_KEY env var
    # Gemini-specific parameters
    top_p=0.95,
    top_k=64
)
```

---

## Provider-Specific Configuration

### OpenAI Configuration Options

```python
from langchain_openai import ChatOpenAI
from langchain_core.rate_limiters import InMemoryRateLimiter

rate_limiter = InMemoryRateLimiter(requests_per_second=10/60)

model = ChatOpenAI(
    model="gpt-4o",
    # Core parameters
    temperature=0.7,          # 0.0 = deterministic, 2.0 = very creative
    max_tokens=2000,          # Maximum tokens in response
    timeout=60,               # Request timeout in seconds
    max_retries=3,            # Retry failed requests
    
    # Authentication
    api_key="...",            # Or use OPENAI_API_KEY env var
    organization="...",       # Optional organization ID
    
    # Advanced options
    rate_limiter=rate_limiter,  # Rate limiting
    streaming=True,           # Enable streaming by default
    
    # Model-specific parameters
    presence_penalty=0.0,     # -2.0 to 2.0
    frequency_penalty=0.0,    # -2.0 to 2.0
    logit_bias={},           # Token probability biases
    seed=42,                 # For reproducible outputs
)
```

### Anthropic Configuration Options

```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(
    model="claude-sonnet-4-5",
    # Core parameters
    temperature=1.0,          # 0.0 = deterministic, 1.0 = creative
    max_tokens=4096,          # Maximum tokens in response
    timeout=30,               # Request timeout in seconds
    
    # Authentication
    api_key="...",            # Or use ANTHROPIC_API_KEY env var
    
    # Anthropic-specific parameters
    top_p=0.9,               # Nucleus sampling
    top_k=40,                # Top-k sampling
    
    # Streaming
    streaming=True,          # Enable streaming
    
    # Advanced features
    # Note: Prompt caching is automatic for large prompts
)
```

### Google Gemini Configuration Options

```python
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    # Core parameters
    temperature=0.5,          # 0.0 = deterministic, 1.0 = creative
    max_output_tokens=8192,   # Maximum tokens in response
    
    # Authentication
    api_key="...",            # Or use GOOGLE_API_KEY env var
    
    # Gemini-specific parameters
    top_p=0.95,              # Nucleus sampling
    top_k=64,                # Top-k sampling
    
    # Safety settings
    safety_settings={
        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
    }
)
```

---

## Model Parameters

### Temperature
Controls randomness in output:
- `0.0`: Deterministic, always picks highest probability token
- `0.3-0.7`: Balanced, good for most use cases
- `1.0+`: Creative, more random outputs

```python
# Use cases by temperature
model_deterministic = init_chat_model("openai:gpt-4o", temperature=0.0)  # Extraction, classification
model_balanced = init_chat_model("openai:gpt-4o", temperature=0.5)       # General Q&A
model_creative = init_chat_model("openai:gpt-4o", temperature=1.0)       # Story writing, brainstorming
```

### Max Tokens
Limits the length of model responses:

```python
model_concise = init_chat_model("openai:gpt-4o", max_tokens=500)   # Short answers
model_detailed = init_chat_model("openai:gpt-4o", max_tokens=4000)  # Long-form content
```

### Timeout
Prevents requests from hanging indefinitely:

```python
model = init_chat_model(
    "anthropic:claude-sonnet-4-5",
    timeout=60  # Timeout after 60 seconds
)
```

### Rate Limiting
Control API request frequency:

```python
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_openai import ChatOpenAI

# 10 requests per minute
rate_limiter = InMemoryRateLimiter(
    requests_per_second=10/60,
    check_every_n_seconds=0.1
)

model = ChatOpenAI(
    model="gpt-4o",
    rate_limiter=rate_limiter
)
```

---

## Model Selection Strategies

### By Task Complexity

```python
from langchain.chat_models import init_chat_model

# Simple tasks: Fast, cost-effective models
simple_model = init_chat_model("openai:gpt-4o-mini", temperature=0.3)

# Complex reasoning: Powerful models
reasoning_model = init_chat_model("openai:o3-mini", temperature=1.0)

# General purpose: Balanced models
general_model = init_chat_model("anthropic:claude-sonnet-4-5", temperature=0.7)

# Long context: Models with large context windows
long_context_model = init_chat_model("google:gemini-2.5-pro", temperature=0.5)
```

### Dynamic Model Selection with Middleware

```python
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain_openai import ChatOpenAI

fast_model = ChatOpenAI(model="gpt-4o-mini")
smart_model = ChatOpenAI(model="gpt-4o")
reasoning_model = ChatOpenAI(model="o3-mini")

@wrap_model_call
def select_model(request: ModelRequest, handler) -> ModelResponse:
    """Choose model based on task complexity."""
    last_message = request.state["messages"][-1].content.lower()
    
    # Complex analytical tasks
    if any(word in last_message for word in ["analyze", "compare", "evaluate"]):
        request.model = reasoning_model
    # Creative tasks
    elif any(word in last_message for word in ["create", "write", "design"]):
        request.model = smart_model
    # Simple tasks
    else:
        request.model = fast_model
    
    return handler(request)
```

### By Cost and Latency

```python
# Cost-optimized (cheapest)
budget_model = init_chat_model("openai:gpt-4o-mini", temperature=0.5)

# Latency-optimized (fastest)
fast_model = init_chat_model("anthropic:claude-sonnet-3-5", temperature=0.5)

# Quality-optimized (best results)
quality_model = init_chat_model("openai:gpt-5", temperature=0.7)
```

---

## Token Management

### Monitoring Token Usage

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-4o")

response = model.invoke("Explain quantum computing in 100 words")

# Access token usage
if response.usage_metadata:
    print(f"Input tokens: {response.usage_metadata['input_tokens']}")
    print(f"Output tokens: {response.usage_metadata['output_tokens']}")
    print(f"Total tokens: {response.usage_metadata['total_tokens']}")
```

### Calculating Costs

```python
def calculate_cost(usage_metadata, model_name):
    """Estimate API cost based on token usage."""
    input_tokens = usage_metadata['input_tokens']
    output_tokens = usage_metadata['output_tokens']
    
    # Pricing (approximate, check current rates)
    prices = {
        "gpt-4o": {"input": 2.5 / 1_000_000, "output": 10 / 1_000_000},
        "gpt-4o-mini": {"input": 0.15 / 1_000_000, "output": 0.60 / 1_000_000},
        "claude-sonnet-4-5": {"input": 3 / 1_000_000, "output": 15 / 1_000_000},
    }
    
    if model_name in prices:
        cost = (input_tokens * prices[model_name]["input"] + 
                output_tokens * prices[model_name]["output"])
        return f"${cost:.6f}"
    return "Unknown"

# Usage
response = model.invoke("Hello, world!")
cost = calculate_cost(response.usage_metadata, "gpt-4o")
print(f"Request cost: {cost}")
```

### Batch Processing for Efficiency

```python
# Inefficient: Sequential calls
results = []
for item in items:
    result = model.invoke(item)
    results.append(result)

# Efficient: Batch processing
results = model.batch(
    items,
    config={"max_concurrency": 10}  # Process 10 at a time
)

# Token usage for batch
total_tokens = sum(r.usage_metadata['total_tokens'] for r in results)
print(f"Total tokens used: {total_tokens}")
```

### Prompt Caching (Provider-Specific)

#### OpenAI
```python
# OpenAI automatically caches repeated prompt prefixes
# No explicit configuration needed
model = ChatOpenAI(model="gpt-4o")

# This prompt prefix will be cached
system_message = SystemMessage(content="You are an expert Python programmer. " * 100)

# Subsequent calls with same prefix are cheaper
for query in queries:
    response = model.invoke([system_message, HumanMessage(query)])
```

#### Anthropic
```python
# Anthropic automatically caches large prompts (2048+ tokens)
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-sonnet-4-5")

# Large system prompt (will be cached)
long_system_prompt = SystemMessage(content="..." * 1000)

# First call: Full cost
response1 = model.invoke([long_system_prompt, HumanMessage("Question 1")])

# Subsequent calls: Reduced cost (cache hit)
response2 = model.invoke([long_system_prompt, HumanMessage("Question 2")])
```

---

## Best Practices

1. **Use `init_chat_model()` for flexibility**: Easier to swap providers
2. **Set appropriate timeouts**: Prevent hung requests
3. **Monitor token usage**: Track costs and optimize prompts
4. **Implement rate limiting**: Protect against quota exhaustion
5. **Choose models by task**: Don't overpay for simple tasks
6. **Use batch processing**: More efficient than sequential calls
7. **Cache when possible**: Leverage provider caching mechanisms
8. **Set reasonable max_tokens**: Prevent runaway costs
9. **Test with cheaper models first**: Validate logic before scaling
10. **Use environment variables**: Keep API keys secure

---

## Production Configuration Example

Typical production model configuration:

```python
from langchain.chat_models import init_chat_model

# For production LLM operations
model = init_chat_model(
    "openai:gpt-4o",
    temperature=0.0,  # Deterministic for classification/extraction
    max_tokens=2000,
    timeout=30
)

# For development/testing
model = init_chat_model(
    "openai:gpt-4o-mini",
    temperature=0.0,
    max_tokens=500
)
```

---

## Integration with Project

In this NileGPT project, models are typically configured like:

```python
from langchain.chat_models import init_chat_model

# For production LLM operations
model = init_chat_model(
    "openai:gpt-4o",
    temperature=0.0,  # Deterministic for sentiment/translation
    max_tokens=2000,
    timeout=30
)

# For development/testing
model = init_chat_model(
    "openai:gpt-4o-mini",
    temperature=0.0,
    max_tokens=500
)
