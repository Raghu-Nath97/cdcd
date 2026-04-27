# DevAgent GitHub Copilot Frontmatter Specifications

This document provides the frontmatter specifications for GitHub Copilot customization files. Follow these rules when creating or reviewing `.agent.md`, `.prompt.md`, `.instructions.md`, or `SKILL.md` files.

> **Tool names and models change frequently.** Always verify current options against the official [VS Code Copilot customization docs](https://code.visualstudio.com/docs/copilot/copilot-customization) and [Custom instructions docs](https://aka.ms/vscode-instructions-docs). Use `web` or `fetch` tools to check the latest documentation when in doubt.

## Tool Names (`tools` key)

The `tools` array controls which capabilities an agent or prompt can access. Tool names must match the exact identifiers recognized by VS Code — these are **not free-form strings**.

**How to find current tool names**: Check the [VS Code Copilot customization docs](https://code.visualstudio.com/docs/copilot/copilot-customization) for the authoritative list. Tool names evolve across VS Code releases.

**Key rules**:
- Use array format: `tools: ['tool1', 'tool2']`
- Use the exact tool identifier (e.g., `runCommands`, not `run_in_terminal` or `terminal`)
- **Built-in tools**: Use exact names from VS Code docs
- **Extension tools**: Use full qualified paths (e.g., `github.vscode-pull-request-github/copilotCodingAgent`)
- **MCP tools**: Wildcards are acceptable (e.g., `atlassian/*`)

**Common mistakes**:
```yaml
# WRONG - not an array
tools: codebase, search

# WRONG - inconsistent quotes
tools: ["codebase", 'search']
```

## Model Selection (`model` key)

**Recommendation: Do not set `model` in agent or prompt frontmatter.**

Reasons:
- Available models depend on your organization's GitHub Copilot subscription tier and enterprise license configuration
- Models are added, deprecated, and rotated every 1-2 months — hardcoded values go stale quickly
- Model selection is a **runtime decision** based on task complexity, not a design-time property of an agent's expertise
- Users naturally select the appropriate model (powerful for complex tasks, fast for simple ones) at invocation time

If you must override the model (e.g., forcing a fast model for a trivially simple prompt), use the display name exactly as shown in the VS Code model picker (e.g., `'Claude Sonnet 4'`, not `claude-sonnet-4` or `sonnet`).

## Required Frontmatter Formats

### Custom Agent Files (`.agent.md`)
```yaml
---
description: 'Brief description for UI display'
tools: ['codebase', 'search', 'fetch']  # Array format required
handoffs:  # Optional: Agent-to-agent workflows
  - label: Start Implementation
    agent: agent
    prompt: Implement the plan outlined above.
    send: false
target: vscode  # Optional: Platform targeting (vscode | github-copilot)
---
```

**Required fields**: `description`
**Optional fields**: `tools`, `handoffs`, `target`

### Custom Instructions (`.instructions.md`)
```yaml
---
description: "What these instructions cover"
applyTo: "**/*.py"                       # Valid glob pattern
---
```

**Required fields**: `applyTo` (for path-specific instructions)
**Optional fields**: `description`

### Prompt Files (`.prompt.md`)
```yaml
---
description: 'Prompt purpose description'
mode: 'agent'                           # 'ask', 'edit', or 'agent'
tools: ['codebase', 'search']           # Array format required
---
```

**Required fields**: `description`
**Optional fields**: `mode`, `tools`

### Skill Files (`SKILL.md`)
```yaml
---
name: skill-name-here
description: 'Action-oriented description. Use when [trigger conditions].'
---
```

**Required fields**: `name`, `description`

### Valid Prompt Modes
- `ask` - Answering questions and explanations
- `edit` - Making code edits across files
- `agent` - Autonomous operations with tools (default)

## Validation Checklist

When creating or reviewing customization files:

- [ ] Tools use array format: `['tool1', 'tool2']`
- [ ] Tool names are exact identifiers (verify against VS Code docs if unsure)
- [ ] `model` is **not set** unless there's a specific reason to override
- [ ] Descriptions use appropriate quotes
- [ ] Required fields are present for each file type
- [ ] YAML syntax is valid (proper indentation, colons, quotes)
- [ ] Glob patterns in `applyTo` are specific (never `**` alone)
- [ ] Prompt modes are from: `ask`, `edit`, `agent`

## Cross-Reference Integration

Generated content should reference related DevAgent materials:

```markdown
You have access to:
1. **P&G Python standards** (from Python coding standards in ai_docs)
2. **Framework expertise** (from the framework agent, e.g., `@pyrogai`)
3. **Development workflows** (from framework-specific prompts/commands)
```

This creates a cohesive ecosystem where different customization types work together effectively.