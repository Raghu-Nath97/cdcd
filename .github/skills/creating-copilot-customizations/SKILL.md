---
name: creating-copilot-customizations
description: 'Guides creation and review of GitHub Copilot customization files (agents, skills, instructions, prompts). Use when creating .agent.md, .prompt.md, .instructions.md, SKILL.md files, reviewing existing customizations for quality, or learning how to write effective Copilot configurations.'
---

# Creating GitHub Copilot Customizations

Guides you through creating high-quality GitHub Copilot customization files for your repository. Covers agents, skills, instructions, and prompts with rules, quality criteria, and best practices.

> **Created something great?** Share your customizations with the DevAgent team for possible inclusion in DevAgent's official framework collection. Contact the maintainers with your files and a description of the value they provide.

## When to Use Each Type

| Type | Purpose | Activation |
|------|---------|------------|
| **Instructions** (`.instructions.md`) | Always-on coding standards for matching files | Automatic via `applyTo` glob pattern |
| **Skills** (`SKILL.md`) | Procedural workflows triggered by user intent | On-demand when task matches description |
| **Agents** (`.agent.md`) | Domain experts with tool access and personality | User selects via `@agent-name` |
| **Prompts** (`.prompt.md`) | Reusable task templates with variable support | User selects via `/prompt-name` |

## Key Rules

### Rule 1: Keep Customizations Focused and Concise

Research shows that verbose, comprehensive context **hurts** AI performance. Follow these limits:

- **Instructions**: Only include non-obvious, project-specific constraints. Avoid generic advice the model already knows.
- **Skills**: 1 skill = 1 workflow area. Aim for 2–3 skills per framework, not 8–12 overlapping ones.
- **Agents**: Single domain of expertise. Use handoffs for multi-domain workflows.
- **Never** duplicate content that exists in README, docs, or other accessible files.

### Rule 2: Do Not Auto-Generate Instructions

Auto-generated "comprehensive" instructions increase cost and reasoning overhead without improving success. Always hand-craft customizations with specific, actionable content.

### Rule 3: Validate All Frontmatter

Every customization file requires valid YAML frontmatter. Invalid frontmatter silently breaks functionality.

## Creating Instructions (`.instructions.md`)

```yaml
---
description: "What these instructions cover"
applyTo: "**/*.py"
---
```

**Required fields**: `description`, `applyTo`

**Rules**:
- Always include `description` — without it, VS Code may not apply the instructions correctly
- Use specific `applyTo` patterns — never use `applyTo: '**'` (injects into every file context, hurting performance)
- Include only constraints that are **non-obvious** and **project-specific**
- Keep content under 50 lines — move detailed references to `.devagent/ai_docs/`

**Good instruction content**: required naming conventions, mandatory error handling patterns, project-specific architecture constraints, security policies.

**Bad instruction content**: generic "write tests", "handle errors", "use type hints" — the model already knows these.

## Creating Skills (`SKILL.md`)

```yaml
---
name: skill-name-here
description: 'Action-oriented description. Use when [specific trigger conditions].'
---
```

**Required fields**: `name`, `description`

**Rules**:
- Description must clearly signal **when to activate** — include explicit trigger phrases
- Encode **procedural steps** (steps, checks, decision points), not general knowledge
- Include at least one **working example**
- Link to `.devagent/ai_docs/` for deep reference material
- Keep compact — focused skills outperform comprehensive verbose ones

**Structure**:
1. Quick overview (2–3 lines)
2. Step-by-step procedure
3. Working example with code
4. Decision guide table (when to use what)
5. Common pitfalls (3–5 bullets max)
6. References to ai_docs

**Quality criteria** (score 0–2 each, target 9+/12):
1. Procedural clarity — are steps concrete and executable?
2. Task-class generality — reusable across similar tasks?
3. Trigger quality — does description clearly signal when to activate?
4. Conciseness — compact and high-value content?
5. Verifier alignment — includes check steps for expected outputs?
6. Reference hygiene — links to ai_docs accurate and minimal?

## Creating Agents (`.agent.md`)

```yaml
---
description: 'Brief description for UI display'
tools: ['codebase', 'search', 'fetch']
---
```

**Required fields**: `description`
**Optional fields**: `tools`, `handoffs`

**Rules**:
- Use the **full explicit list** of tools — never use wildcards for built-in or extension tools in agent files. Check the [VS Code Copilot docs](https://code.visualstudio.com/docs/copilot/copilot-customization) for the current list of available tool names.
- **MCP tools**: Wildcards are acceptable (e.g., `atlassian/*`)
- Keep agent expertise focused on a single domain
- Use `handoffs` for multi-step workflows across agents
- **Do not set `model`** — model selection is a runtime decision based on task complexity and available models (which depend on your organization's Copilot subscription). Agent expertise is orthogonal to model capability.

**Minimal example** — a focused agent for a specific domain:
```markdown
---
description: 'FastAPI development expert - helps with routes, middleware, and async patterns'
tools: ['codebase', 'search', 'fetch', 'edit', 'runCommands']
---

# FastAPI Expert

You are an expert in FastAPI development. Help users with:
- Creating new route handlers with proper request/response models
- Setting up middleware and dependency injection
- Async database integration patterns

## Key Conventions
- All routes use Pydantic v2 models for validation
- Error responses follow RFC 7807 Problem Details format
- Use `Depends()` for shared logic, not decorators
```

**Handoffs structure**:
```yaml
handoffs:
  - label: 'Next Step'
    agent: 'target-agent'
    prompt: 'Optional context for the next agent'
    send: false
```

## Creating Prompts (`.prompt.md`)

```yaml
---
description: 'What this prompt does'
mode: 'agent'
tools: ['codebase', 'search']
---
```

**Required fields**: `description`
**Optional fields**: `mode`, `tools`, `model`

**Modes**: `ask` (Q&A), `edit` (code changes), `agent` (autonomous with tools)

**Variable support**: `${workspaceFolder}`, `${selection}`, `${file}`, `${input:varName:placeholder}`

## Reviewing Existing Customizations

When reviewing a customization file, check:

- [ ] Frontmatter is valid YAML with required fields
- [ ] Content is concise and project-specific (not generic advice)
- [ ] No duplication of readily available documentation
- [ ] Tool names match approved list exactly
- [ ] `applyTo` patterns are specific (not `**`)
- [ ] Cross-references use correct relative paths
- [ ] Skills have clear trigger conditions in description

## Sharing with DevAgent

If your customizations work well and could benefit others:

1. Document what problem they solve and for whom
2. Contact the DevAgent maintainers with your files
3. Include usage examples and evidence of value
4. The team will evaluate for inclusion in DevAgent's framework collection

## Reference Materials

- [Frontmatter Specifications](.devagent/ai_docs/devagent-frontmatter-specs.md) — frontmatter format rules and key descriptions
- [Framework Development Guide](.devagent/ai_docs/framework-development-guide.md) — guide for creating complete framework packages
- For the latest VS Code Copilot customization features, available tool names, and model options, use `web` or `fetch` tools to check [VS Code Copilot docs](https://code.visualstudio.com/docs/copilot/copilot-customization) and [Custom instructions docs](https://aka.ms/vscode-instructions-docs)
