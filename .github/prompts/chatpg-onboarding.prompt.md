---
description: 'ChatPG onboarding overview for a new AIE SRE. Run /chatpg-onboarding when someone asks "what is ChatPG", "how does it work", "how is it managed", or anything similar in the first couple of weeks. Reads the local diagram analyses under Docs/ChatPG/, pulls the ChatPG Confluence page (TURING/4354081339) live through the Atlassian MCP, and produces an 8-section briefing with ASCII flow diagrams. No Mermaid.'
mode: 'agent'
tools: ['vscode', 'read', 'search', 'web', 'browser', 'genai-platform/*', 'mcp-atlassian/*', 'com.atlassian/atlassian-mcp-server/*']
---

# ChatPG Onboarding Briefing

This prompt produces a single, focused briefing on ChatPG for someone who is brand new to the AIE SRE team. Treat the reader as someone who has never opened the ChatPG repo and doesn't know the P&G enterprise-AI vocabulary yet — they want a clean mental model first, not a brain-dump.

Always answer from the source material below, not from memory.

## Sources to read first

Work through these in order before writing anything:

1. **The onboarding skill** — [`.github/skills/aie-sre-onboarding/SKILL.md`](.github/skills/aie-sre-onboarding/SKILL.md). It carries the canonical Confluence/Jira links, the GitHub repo URLs, and the full diagram-drawing rules referenced throughout this prompt.
2. **The local diagram analyses** under `.github/skills/aie-sre-onboarding/Docs/ChatPG/`:

   | File | What it covers |
   |------|----------------|
   | `ChatPG - AED.md` | Application Environment — what ChatPG depends on and integrates with |
   | `ChatPG - TID.md` | Technical Infrastructure — subscriptions, RGs, AKS, networking |
   | `ChatPG - Communication Flow Diagram.md` | End-to-end request flow between components |

   These `.md` files are the structural source of truth for every diagram. The matching `.drawio.png` next to each is for human cross-check only.

3. **The ChatPG Confluence page** — page ID `4354081339`, TURING space. Fetch the body live via the Atlassian MCP (prefer a direct page-fetch tool; fall back to Rovo search if only that's wired). Pull narrative the diagrams don't carry: business purpose, owning team, recent changes, open incidents. If the MCP errors out (no tool, 401, 403, 404, server down), put a single one-line note at the very top of the briefing — *"Confluence MCP unavailable this turn — briefing built from local Docs/ChatPG/ analyses only"* — and continue. Don't retry, don't halt.

4. **Jira** *(optional, only when the user's question needs it)* — query the TURING project via the Atlassian MCP for incident or ticket context.

If the diagram `.md` files are missing entirely (folder has only `.drawio.png` exports), stop and tell the user to regenerate the analyses before re-running the slash command. Don't draw diagrams from generic ChatPG knowledge. If only one is missing, say so and skip the section that depended on it.

## Briefing format — 8 sections, in order

The sections are sequential by design. A new joiner should be able to read top-to-bottom and gradually build understanding. Keep prose tight; the diagrams do most of the work.

### 1. ChatPG in one paragraph
Three or four sentences in plain language: what ChatPG is, who uses it, and why it's more than an LLM wrapper. No acronyms — this is the only section a busy new joiner is guaranteed to read. Source: `AED.md` + Confluence.

### 2. Mental model + system integration diagram
Two parts.

**(a)** A small ASCII block showing the three layers of ChatPG, followed by a 3-row table mapping each layer to its repo and one-line responsibility.

```text
┌────────────────────────────────────────────────────────────┐
│                       ChatPG                              │
│  ┌──────────────┐  ┌───────────────┐  ┌─────────────────┐ │
│  │ Core Product │  │ Agent Runtime │  │ Cloud Infra     │ │
│  └──────────────┘  └───────────────┘  └─────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

| Layer | Repo | What it owns |
|-------|------|--------------|
| Core Product  | `de-cf-chatpg-core`   | Frontend UI + backend APIs + persistence |
| Agent Runtime | `de-cf-chatpg-agents` | Tool-calling agents, deep research flows, LangGraph state |
| Cloud Infra   | `de-cf-chatpg-infra`  | AKS, Flux/Kustomize overlays, networking, secrets |

**(b)** A top-down system integration diagram following the *system integration diagram* template in `SKILL.md`. Use the six canonical layers in order: USERS / CLIENTS → EDGE / GATEWAY → AUTH / IDENTITY → CORE SERVICE → INTEGRATION / DOWNSTREAM, with PERSISTENCE and OBSERVABILITY drawn as side-blocks below the main chain. Pull the actual component names (`Web Browser (HTTPS)`, `Microsoft Teams (WebRTC)`, `Application Gateway`, `Azure APIM`, `MSTF EntraID`, `PingFederate Prod Instance`, `PingID MFA`, `Authle`, `MSTF Active Directory`, `ChatPG Service`, `GenAI Platform`, `PostgreSQL flex server`, `Cache for Redis`, `BLOB Storage`, `Container Registry`, `Key Vault`, `Application Insights`, `Spyglass`) from `AED.md` and the communication flow `.md`.

Caption the diagram: *Source: ChatPG - AED.md + ChatPG - Communication Flow Diagram.md*.

### 3. How a single user request flows
Two views, both required, sharing the same circled-digit step numbers so the reader can correlate them.

**View 1 — Horizontal numbered request-flow diagram.** Follow the *request-flow diagrams* template in `SKILL.md`: main happy path left-to-right on a single line, auth providers as one labelled `Auth chain` cluster above the line joining with one arrow, exact labels from `ChatPG - Communication Flow Diagram.md` (e.g. `PingFederate Prod Instance`, not `PingFed`). Caption it. Then 6–8 plain-English numbered sentences underneath, one per circled digit. Newbie level — no internal CI numbers, no resource IDs.

**View 2 — Vertical narrative step boxes.** Follow the *numbered narrative step boxes* template in `SKILL.md`. One box per step, top-to-bottom, separated by a single centred `▼`. Step numbers in the headers (`STEP 4`) match the circled digits in View 1 (`④`). For the auth step, use the fan-out / re-merge layout with parallel boxes for EntraID / PingFederate / PingID MFA. 6–8 boxes total.

### 4. The stack
Six bullets, one short line each:
- Frontend
- Backend
- Agent runtime
- Infra
- Identity
- Observability

Source: onboarding skill + `AED.md` + Confluence (if it adds anything concrete).

### 5. How ChatPG is run in Azure
One infrastructure diagram from `ChatPG - TID.md`, following the *infrastructure / deployment diagrams* template in `SKILL.md`. One outer box per Azure subscription with the subscription name and resource-group names on the top border; vertical groups inside (`Services`, `Network`, `AKS`); externals (Spyglass, GenAI Platform, PingFederate Prod Instance, EntraID, Microsoft Teams, Application Insights) in their own `External` cluster at the bottom. Caption: *Source: ChatPG - TID.md*.

Then four short bullets:
- **How releases ship** — CICD framework + GHA Runner
- **Where secrets live** — Key Vault
- **What is monitored** — Application Insights + Spyglass
- **Where incidents are tracked** — Jira TURING project

### 6. Where to go next
A 6-row links table. Pull URLs from the onboarding skill — don't invent them and don't fall back to *(see SKILL.md)*; the data is right there.

| Resource | Link |
|----------|------|
| ChatPG Confluence section | https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/pages/4354081339/ChatPG |
| `de-cf-chatpg-core` repo | `https://github.com/procter-gamble/de-cf-chatpg-core` |
| `de-cf-chatpg-agents` repo | `https://github.com/procter-gamble/de-cf-chatpg-agents` |
| `de-cf-chatpg-infra` repo | `https://github.com/procter-gamble/de-cf-chatpg-infra` |
| Local diagrams folder | `.github/skills/aie-sre-onboarding/Docs/ChatPG/` |
| Jira incidents | TURING project |

Wrap the GitHub URLs in backticks so the chat surface doesn't auto-link them — the literal URL needs to remain visible. The local diagrams cell is the literal path string, not a markdown link.

### 7. Reference material on disk
List the `.md` files you actually read this turn (full repo-relative paths) plus the Confluence page id if the fetch succeeded. Five or six bullets. This lets the reader replay the same calls.

### 8. Want to go deeper?
End with one focused offer, not a menu. For example:

> *"Want me to walk through the auth chain, the agent runtime internals, the AKS deploy pipeline, or a recent incident playbook? Pick one and I'll dig in."*

One line. No trailing summary or *"let me know if you have questions"*.

## Scope

- **ASCII diagrams only** — never Mermaid or PlantUML. All diagram styles are defined in `SKILL.md`; this prompt only specifies which template to use where.
- **Use exact labels from the source `.md` files** in every diagram. If the source says `mlwCHATPGPROD` or `PingFederate Prod Instance`, write that.
- **Don't invent specifics** — incident IDs, Azure resource IDs, CI numbers, code paths, model names. They have to come from the local sources, the onboarding skill, or the live Confluence fetch. If asked about something not covered: *"I don't have that in the onboarding overview — check the ChatPG Confluence page or the relevant repo."*
- **Newbie language**. Expand each acronym the first time it appears (`AKS (Azure Kubernetes Service)`, `APIM (Azure API Management)`, `MFA (multi-factor auth)`).
- **Length cap ~220 lines** including the diagrams. If you go over, cut prose — never the diagrams.
- Don't load `github-chatpg` or `leanix` for this briefing. Those are for code-level questions and live LeanIX exports, not the overview.
