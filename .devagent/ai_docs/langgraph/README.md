# LangGraph Custom GitHub Copilot Configuration

This directory contains custom GitHub Copilot configurations optimized for LangGraph development.

## What is LangGraph?

LangGraph is a low-level orchestration framework for building stateful, long-running agent workflows. It enables:

- **Stateful workflows**: Graph state persists across executions
- **Human-in-the-loop**: Pause for human review and input
- **Memory management**: Short-term (threads) and long-term (store) memory
- **Multi-agent systems**: Coordinate multiple specialized agents
- **Durable execution**: Fault-tolerant, resumable workflows
- **Flexible control flow**: Dynamic routing, conditional edges, parallel processing

## Available Customizations

### 🤖 Custom Chat Mode

**File**: `.github/agents/langgraph.agent.md`

Activate with: `@langgraph` in GitHub Copilot Chat

An expert AI assistant specialized in LangGraph with deep knowledge of:

- Graph architecture (StateGraph, nodes, edges)
- State management and reducers
- Persistence patterns (checkpointers, memory stores)
- Agent architectures (ReAct, hierarchical, collaborative)
- Human-in-the-loop workflows
- Best practices and common patterns

### 📋 Custom Instructions

**File**: `.github/instructions/langgraph.instructions.md`

Automatically applied to Python files containing LangGraph code.

Enforces best practices:

- Proper type annotations for state schemas
- Correct reducer usage
- Command return type annotations
- Checkpointer configuration
- Error handling patterns
- Testing strategies

### 🎯 Custom Prompts

#### 1. Create LangGraph Workflow

**File**: `.github/prompts/create-langgraph-workflow.prompt.md`

Use when: Starting a new LangGraph agent from scratch

Helps you:

- Choose the right architecture
- Design state schema
- Implement nodes and edges
- Add persistence and memory
- Set up human-in-the-loop

#### 2. Debug LangGraph Workflow

**File**: `.github/prompts/debug-langgraph.prompt.md`

Use when: Fixing issues in existing LangGraph code

Provides:

- Common issue diagnosis
- Visualization tools
- State inspection methods
- Fix patterns for typical problems
- Performance optimization tips

#### 3. Add LangGraph Persistence

**File**: `.github/prompts/add-langgraph-persistence.prompt.md`

Use when: Adding state persistence to a workflow

Covers:

- Choosing appropriate checkpointers
- Thread management
- Memory store setup
- Semantic search configuration
- Migration checklist

### 📚 AI Documentation

**Directory**: `.devagent/ai_docs/langgraph/`

Comprehensive reference materials that Copilot can access:

1. **core-concepts.md**: StateGraph, nodes, edges, state management, compilation
2. **persistence.md**: Checkpointers, threads, memory stores, serialization
3. **agent-architectures.md**: Router, ReAct, hierarchical, collaborative patterns
4. **human-in-the-loop.md**: Interrupts, approval patterns, validation flows
5. **examples.md**: 10+ working examples of common LangGraph patterns

## Quick Start

### Using the Chat Mode

```
@langgraph How do I create a multi-agent workflow with approval steps?
```

### Using Custom Prompts

In GitHub Copilot Chat:

1. Type `/` to see available prompts
2. Select the LangGraph prompt you need
3. Answer the questions and get customized code

### Leveraging Custom Instructions

Simply write LangGraph code - the instructions automatically:

- Suggest proper patterns
- Catch common mistakes
- Enforce best practices
- Provide relevant examples

## Example Usage

### Creating a New Agent

```python
# Ask @langgraph:
# "Create a research agent that can search the web, 
# analyze results, and needs human approval before 
# sending reports"

# You'll get a complete implementation with:
# - Proper state schema
# - Tool integration
# - Human-in-the-loop approval
# - Persistence configuration
# - Usage examples
```

### Debugging an Issue

```python
# When you get an error like:
# "GraphRecursionError: Recursion limit exceeded"

# Ask @langgraph:
# "My graph is hitting recursion limit, help me debug"

# You'll get:
# - Diagnosis of the infinite loop
# - Visualization of the graph
# - Fix with proper exit conditions
# - Tips to prevent similar issues
```

### Adding Features

```python
# Ask @langgraph:
# "Add persistent memory to my existing agent 
# so it remembers user preferences across sessions"

# You'll get:
# - Checkpointer setup
# - Memory store configuration
# - Node modifications to use store
# - Testing examples
```

## Architecture Patterns

The configurations support all LangGraph patterns:

| Pattern | Use Case | Prompt |
|---------|----------|--------|
| **Router** | Simple classification | "Create a router agent" |
| **ReAct Agent** | Tool-calling with reasoning | "Build a research agent" |
| **Hierarchical** | Supervisor + specialists | "Multi-agent with coordinator" |
| **Collaborative** | Peer agents | "Collaborative data science team" |
| **Reflection** | Self-improving | "Agent that critiques its output" |
| **Planning** | Multi-step tasks | "Planning agent for complex tasks" |

## Best Practices Built-In

These configurations enforce:

✅ **Type Safety**: Proper TypedDict/Pydantic usage  
✅ **State Management**: Correct reducer patterns  
✅ **Control Flow**: Command vs conditional edges  
✅ **Persistence**: Appropriate checkpointer selection  
✅ **Error Handling**: Try-catch and retry patterns  
✅ **Testing**: Node isolation and integration tests  
✅ **Performance**: Caching and parallelization  
✅ **Security**: Encryption and validation  
✅ **Observability**: Logging and tracing  
✅ **Documentation**: Clear comments and examples  

## Learning Resources

The AI documentation provides:

- Concept explanations with examples
- Common patterns and anti-patterns
- Troubleshooting guides
- Architecture decision guides
- Production deployment tips

## Integration with Your Workflow

These configurations integrate seamlessly with:

- **LangChain**: Tools, models, and components
- **LangSmith**: Tracing and debugging
- **Python testing**: pytest, unittest
- **Type checking**: mypy, pyright
- **Your existing code**: Analyze and suggest improvements

## Getting Help

In GitHub Copilot Chat, you can always ask:

```
@langgraph explain [concept]
@langgraph help with [problem]
@langgraph show example of [pattern]
@langgraph best practice for [scenario]
```

The agent has access to all the documentation and will provide expert guidance!

## What's Included

```
.github/
├── agents/
│   └── langgraph.agent.md          # Expert AI assistant
├── instructions/
│   └── langgraph.instructions.md      # Coding standards
├── prompts/
│   ├── create-langgraph-workflow.prompt.md
│   ├── debug-langgraph.prompt.md
│   └── add-langgraph-persistence.prompt.md
└── ai_docs/
    └── langgraph/
        ├── core-concepts.md           # Graph fundamentals
        ├── persistence.md             # State & memory
        ├── agent-architectures.md     # Design patterns
        ├── human-in-the-loop.md       # HITL patterns
        └── examples.md                # Code examples
```

## Contributing

To enhance these configurations:

1. Add new examples to `examples.md`
2. Document new patterns in appropriate docs
3. Update instructions with new best practices
4. Create prompts for common workflows

## Version

These configurations are optimized for:

- **LangGraph**: v1.0+
- **LangChain**: Latest
- **Python**: 3.9+

---

**Happy building with LangGraph! 🚀**

For more information, visit: <https://langchain-ai.github.io/langgraph/>
