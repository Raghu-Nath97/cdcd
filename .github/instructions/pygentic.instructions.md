---
name: 'PyGentic Framework'
description: 'Instructions for working with the PyGentic framework'
applyTo: '**/*.py'
---

# PyGentic Framework Guidelines

## Overview

PyGentic is P&G's enterprise agentic framework for building secure, reliable, and scalable AI Agents. When working with PyGentic, adhere to the following principles and best practices.

**Note**: PyGentic is built on LangGraph. For LangGraph technical best practices (state schemas, persistence, graph patterns), refer to `../instructions/langgraph.instructions.md` and `.devagent/ai_docs/langgraph/`. This guide focuses on P&G-specific aspects.

## Core Principles

1.  **Agentic by Design**: Your code should reflect the goal-driven, autonomous nature of AI Agents. Agents should be able to receive instructions in natural language, formulate dynamic plans, and use tools to achieve their goals.
2.  **Enterprise-Grade**: All code must be secure, reliable, and scalable. This includes proper error handling, logging, and consideration for performance.
3.  **Python Best Practices**: Follow standard Python best practices. Use `pathlib.Path` for all file system operations to ensure cross-platform compatibility.

## Framework Integration

-   **AI Factory**: Leverage the native integrations with the AI Factory ecosystem. This includes using the GenAI Platform for LLM and utility APIs, AI Observability for tracing and monitoring, and IPA for deployment.
-   **Chainlit and chatPG**: When building user-facing applications, use the built-in support for AI Apps Chainlit for interactive UIs and integrate with chatPG for a consistent user experience.

## Development Workflow

1.  **Register Your Use Case**: Before starting a new project, register your use case via the PyGentic Use Case Registration form.
2.  **Follow Agentic Principles**: Always refer to the [agentic principles](.devagent/ai_docs/pygentic/core/principles.md) for guidance on building responsible AI.
3.  **Use Templates**: Start with PyGentic's quickstart templates to ensure your project is set up correctly.
4.  **Tutorials and Guides**: Refer to the official PyGentic tutorials and component guides for in-depth information.

By following these instructions, you will create robust and compliant AI solutions using the PyGentic framework.
