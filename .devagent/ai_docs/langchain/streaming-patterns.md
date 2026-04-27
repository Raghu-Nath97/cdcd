# LangChain Streaming Patterns

Guide to implementing real-time streaming in LangChain agents and applications.

## Table of Contents
1. [Streaming Overview](#streaming-overview)
2. [Token Streaming](#token-streaming)
3. [Agent Step Streaming](#agent-step-streaming)
4. [Tool Progress Updates](#tool-progress-updates)
5. [Production Patterns](#production-patterns)

---

## Streaming Overview

Streaming provides real-time feedback during LLM operations, improving user experience for long-running tasks.

### Benefits
- **Better UX**: Users see progress immediately
- **Lower latency perception**: Appears faster even if total time is the same
- **Real-time updates**: See agent reasoning and tool calls as they happen
- **Interruptibility**: Can cancel long-running operations

---

## Token Streaming

Stream tokens as the model generates them:

### Basic Token Streaming

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-4o")

# Stream tokens
for chunk in model.stream("Write a short story about a robot"):
    print(chunk.text, end="", flush=True)
```

### With Message Aggregation

```python
from langchain_core.messages import AIMessageChunk

full_message = None

for chunk in model.stream("Explain quantum computing"):
    # Aggregate chunks
    if full_message is None:
        full_message = chunk
    else:
        full_message = full_message + chunk
    
    # Display incrementally
    print(chunk.text, end="", flush=True)

print("\n\nFull message:", full_message.content)
```

### Async Token Streaming

```python
async def stream_async():
    async for chunk in model.astream("Write a poem"):
        print(chunk.text, end="", flush=True)

import asyncio
asyncio.run(stream_async())
```

---

## Agent Step Streaming

Stream agent execution steps to see reasoning and tool calls:

### Stream Mode: "values"

```python
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = create_agent(
    model="openai:gpt-4o",
    tools=[search],
    system_prompt="You are a helpful assistant."
)

# Stream agent steps
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "Search for AI trends"}]},
    stream_mode="values"
):
    # Each chunk is the current state
    latest_message = chunk["messages"][-1]
    print(f"Step: {latest_message.__class__.__name__}")
    print(f"Content: {latest_message.content[:100] if hasattr(latest_message, 'content') else 'N/A'}")
    print("---")
```

### Stream Mode: "messages"

```python
# Stream only new messages
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "What's the weather?"}]},
    stream_mode="messages"
):
    # chunk is a tuple: (message, metadata)
    message, metadata = chunk
    print(f"New message: {message}")
```

### Stream Mode: "updates"

```python
# Stream state updates
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "Help me plan a trip"}]},
    stream_mode="updates"
):
    # chunk shows what changed in state
    print(f"Update: {chunk}")
```

---

## Tool Progress Updates

Tools can stream progress updates during execution:

### Basic Tool Streaming

```python
from langchain.tools import tool, ToolRuntime
import time

@tool
def long_running_task(
    task_name: str,
    runtime: ToolRuntime
) -> str:
    """Execute a long-running task with progress updates."""
    writer = runtime.stream_writer
    
    writer(f"Starting {task_name}...")
    time.sleep(1)
    
    writer("Processing step 1/4...")
    time.sleep(1)
    
    writer("Processing step 2/4...")
    time.sleep(1)
    
    writer("Processing step 3/4...")
    time.sleep(1)
    
    writer("Processing step 4/4...")
    time.sleep(1)
    
    writer("Complete!")
    return f"Finished {task_name}"

agent = create_agent(
    model="openai:gpt-4o",
    tools=[long_running_task]
)

# Stream to see progress updates
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "Run data analysis"}]},
    stream_mode="values"
):
    print(chunk)
```

### Async Tool Streaming

```python
import asyncio

@tool
async def async_long_task(
    task_name: str,
    runtime: ToolRuntime
) -> str:
    """Async long-running task."""
    writer = runtime.stream_writer
    
    for i in range(5):
        writer(f"Progress: {(i+1)*20}%")
        await asyncio.sleep(0.5)
    
    return f"Completed {task_name}"
```

---

## Production Patterns

### Web Application Streaming (FastAPI)

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json

app = FastAPI()

@app.post("/chat/stream")
async def stream_chat(message: str):
    """Stream chat responses."""
    async def generate():
        agent = create_agent(
            model="openai:gpt-4o",
            tools=[search_tool]
        )
        
        async for chunk in agent.astream(
            {"messages": [{"role": "user", "content": message}]},
            stream_mode="values"
        ):
            latest = chunk["messages"][-1]
            
            # Send as server-sent events
            data = {
                "type": latest.__class__.__name__,
                "content": getattr(latest, 'content', ''),
            }
            yield f"data: {json.dumps(data)}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

### Progress Bar Integration

```python
from tqdm import tqdm

@tool
def process_batch(
    items: list[str],
    runtime: ToolRuntime
) -> str:
    """Process items with progress bar."""
    writer = runtime.stream_writer
    
    for i, item in enumerate(items):
        # Process item
        time.sleep(0.1)
        
        # Update progress
        progress = int((i + 1) / len(items) * 100)
        writer(f"Progress: {progress}% ({i+1}/{len(items)})")
    
    return f"Processed {len(items)} items"
```

### Error Handling in Streaming

```python
def safe_stream(agent, input_data):
    """Stream with error handling."""
    try:
        for chunk in agent.stream(input_data, stream_mode="values"):
            yield chunk
    except Exception as e:
        # Send error message
        error_chunk = {
            "messages": [{
                "role": "error",
                "content": f"Error: {str(e)}"
            }]
        }
        yield error_chunk
```

### Cancellation Support

```python
import threading

class CancellableStream:
    """Streaming with cancellation support."""
    
    def __init__(self):
        self.cancelled = threading.Event()
    
    def cancel(self):
        """Cancel the stream."""
        self.cancelled.set()
    
    def stream(self, agent, input_data):
        """Stream with cancellation checks."""
        for chunk in agent.stream(input_data, stream_mode="values"):
            if self.cancelled.is_set():
                print("Stream cancelled")
                break
            yield chunk

# Usage
stream = CancellableStream()

# In another thread
# stream.cancel()  # Cancels the stream
```

---

## Best Practices

1. **Choose appropriate stream mode**: `values` for full state, `messages` for incremental
2. **Handle incomplete chunks**: Not all chunks have all fields
3. **Buffer for UI**: Aggregate small chunks for smoother display
4. **Error handling**: Always wrap streaming in try/except
5. **Timeout protection**: Add timeouts for production systems
6. **Progress updates**: Use `runtime.stream_writer` in tools
7. **Async when possible**: Use `astream()` for better concurrency
8. **Test streaming**: Verify streaming works before production
9. **Monitor performance**: Track latency of first token
10. **User feedback**: Show clear progress indicators

---

## Production Example

Batch processing with streaming progress updates:

```python
@tool
def process_batch(
    items: list[str],
    runtime: ToolRuntime
) -> str:
    """Process multiple items with progress updates."""
    writer = runtime.stream_writer
    
    results = []
    for i, item in enumerate(items):
        # Process item
        result = process_item(item)
        results.append(result)
        
        # Progress update
        writer(f"Processed {i+1}/{len(items)}")
    
    return f"Completed {len(results)} items"

# Stream processing progress
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "Process these items"}]},
    stream_mode="values"
):
    # Display progress to user
    print(chunk)
```

---

## Integration with NileGPT

Example streaming for batch translation:

```python
@tool
def translate_batch(
    texts: list[str],
    runtime: ToolRuntime
) -> str:
    """Translate multiple texts with progress."""
    writer = runtime.stream_writer
    
    results = []
    for i, text in enumerate(texts):
        # Translate
        result = translate(text)
        results.append(result)
        
        # Progress update
        writer(f"Translated {i+1}/{len(texts)}")
    
    return f"Completed {len(results)} translations"

# Stream translation progress
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "Translate these reviews"}]},
    stream_mode="values"
):
    # Display progress to user
    print(chunk)
```
