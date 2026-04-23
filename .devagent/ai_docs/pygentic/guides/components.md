# PyGentic Components

This guide provides an overview of the various components and features available in PyGentic.

## Stable Features

### AskPG Agent
The AskPG agent leverages the AskPG API to interact with P&G's public and private knowledge bases. It can search, retrieve, and process information from corporate knowledge repositories.

### Chainlit UI
PyGentic's Chainlit template enables rapid development of interactive chat applications for agentic flows. Key features include:
- Web-based chat interface
- Multi-agent conversations
- Markdown support
- File uploads and downloads

### Data Analytics Agent
The data analytics agentic flow leverages the InsightsPG data agent to perform SQL queries and data analysis tasks. Supported data sources include:
- SQLite
- Databricks
- Other SQL-based systems

### Memory System
PyGentic provides a comprehensive memory system for AI agents, enabling them to:
- Remember user preferences
- Store experiences
- Maintain long-term knowledge across interactions
- Recall previous conversations and context

### Prebuilt Tools
PyGentic includes ready-to-use tools that enhance agent capabilities:
- Google Search: Search the web for information
- Translate Text: Translate content between languages
- SQL Query: Execute database queries
- Document Processing: Extract and process text from documents

## Experimental Features

### Agent-to-Agent (A2A)
PyGentic's A2A implementation enables standardized inter-agent communication and context preservation across multi-turn interactions. This allows for complex agent ecosystems where specialized agents collaborate on tasks.

### Model Context Protocol (MCP)
The MCP template provides a standardized way to create MCP servers that expose tools and functionality to AI Agents and other MCP clients. This enables integration with VS Code Copilot and other MCP-compatible systems.

### Realtime Voice Agent
The Realtime Voice Agent feature demonstrates PyGentic's integration with OpenAI's Realtime API for building voice-enabled AI agents, supporting:
- Real-time speech recognition
- Natural voice responses
- Continuous conversations