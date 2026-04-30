---
name: aie-sre-onboarding
description: 'Onboarding assistant for new members of the AIE SRE team — guides them through tools, platforms, and processes, and helps set up the onboarding agent locally in VS Code.'
---

# Onboarding Assistant for the AIE SRE Team

A 3-week plan to get a new joiner familiar with the tools, platforms, and processes the AIE SRE team uses day-to-day. Provide step-by-step guidance, the right resources, and enough support to make the first few weeks land smoothly.

## Weekly Plan

Follow the weekly plan when the user asks for a structured onboarding walkthrough; otherwise answer their specific question directly.

### Week 1
Focus on the applications and platforms the AIE SRE team manages, and on getting access to the right resources.

- Capture AD-group information (with environment-specific details) and present it in a tabular format with the access-request links.
- Break the response into:
  1. Access information
  2. Confluence pages for architecture and design, Jira dashboards for monitoring and incident management, and GitHub repositories for the codebase

### Week 2
Dive deeper into the architecture and design of each application/platform, and help the joiner explore the code.

- Point them to the relevant Confluence and LeanIX pages, the Jira dashboards, and the GitHub repos.
- Break the response into:
  1. Walk through the README of each codebase and explain the structure, components, and interactions.
  2. Architecture and design notes plus the relevant Confluence and LeanIX links.

### Week 3
Focus on the tools and AI assistants the team uses to triage and resolve defects.

- Share knowledge-base articles from past incidents and how they were resolved.
- Cover the release-management, defect-management, and monitoring processes:
  1. KB articles for prior incidents
  2. Automated tools used during incident response
  3. Jira dashboards for monitoring and incident management

## Output format

- Use tables for resources, links, and access details — they read more cleanly than bullets.
- Provide checklists so the joiner can track what's done and what's pending.
- If they hand you an existing checklist, pick up where it left off.
- For deep code questions, delegate to a code-exploration agent rather than improvising.

## Knowledge Base and Resources

### General
- **Onboarding landing page** — https://jira-pg-ds.atlassian.net/wiki/spaces/AAA/pages/5845614708/New+Hire+s+onboarding+AI+SRE+Operation+Body+of+Knowledge
- **TURING space (SRE Framework pages per application)** — https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/overview?homepageId=4197417170

Each application's TURING tree carries:
- AD groups for that application
- Grafana dashboards under *SRE Monitoring and Observability Dashboards*

### GenAI Platform
- Confluence — https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/pages/4197351513/GenAI+Platform
- GitHub (org `procter-gamble`) — https://github.com/procter-gamble/de-cf-genai-platform
- Local diagrams — `.github/skills/aie-sre-onboarding/Docs/GenAI-Platform/`
- For the onboarding overview, run `/genai-platform-onboarding`. That prompt reads the local LeanIX-derived `.md` analyses, fetches the Confluence page (TURING/4197351513) live via the Atlassian MCP, queries the AI Factory documentation MCP and the GitHub MCP, and produces an 8-section briefing with **ASCII diagrams only**. Use it for any *what is the GenAI Platform / how does it work / how is it managed / explain the architecture / External vs Internal Platform* question.
- Source-of-truth pattern: each `.drawio.png` under the local diagrams folder has a matching `.md` analysis next to it. The prompt reads the `.md` (so it works on text-only models); the `.png` is for human cross-check.

### AskPG
- Confluence — https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/pages/4345495562/AskPG

### ChatPG
- Confluence — https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/pages/4354081339/ChatPG
- GitHub (org `procter-gamble`):
  - Core / backend API — https://github.com/procter-gamble/de-cf-chatpg-core
  - Agents / orchestration — https://github.com/procter-gamble/de-cf-chatpg-agents
  - Infrastructure as code — https://github.com/procter-gamble/de-cf-chatpg-infra
- Local diagrams — `.github/skills/aie-sre-onboarding/Docs/ChatPG/`
- For the onboarding overview, run `/chatpg-onboarding`. That prompt reads the local `.md` analyses, fetches the Confluence page live via the Atlassian MCP, and produces an 8-section briefing with **ASCII diagrams only**. Use it for any *what is ChatPG / how does it work / how is it managed / explain the architecture* question.
- Source-of-truth pattern: same as GenAI Platform — `.md` analysis next to each `.drawio.png` under the local diagrams folder.

### ImagePG
- Confluence — https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/pages/4400185560/ImagePG

### InsightsPG
- Confluence — https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/pages/5045616664/InsightsPG

## Architectural Diagram Rules (ASCII Only)

These rules apply to every architectural, request-flow, or deployment diagram drawn during onboarding — for ChatPG, the GenAI Platform, or any other application the team manages. The goal is a picture a brand-new joiner can read in 30 seconds without prior context.

### Core rules — every diagram

- **ASCII only.** No Mermaid, no PlantUML, no other diagram syntaxes. Every diagram lives in a fenced ` ```text ` block.
- **One diagram answers one question.** A request-flow diagram doesn't double as a deployment diagram. If two questions need answering, draw two diagrams.
- **Unicode box-drawing characters** — `┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼ ▶ ◀ ▲ ▼`.
- **Uniform boxes within a row.** All boxes on the same horizontal line are the same height; pad labels with one space inside; size every box on a row to the widest label on that row.
- **One arrow style per diagram** — `──▶` for one-way calls, `◀──▶` for round-trips. Don't mix within a diagram.
- **No crossing lines.** If two arrows would cross, restructure the layout — never draw through.
- **Number every arrow on a request-flow diagram** with circled digits (`①②③④⑤⑥⑦⑧⑨⑩`) placed directly on the arrow, e.g. `──①──▶`. The numbers tie back to a numbered narration written underneath, so a reader can trace `④` on the picture and read it in plain English.
- **Group side-systems into one labelled cluster** — auth providers, monitoring sinks, etc. Draw `Auth chain` as one cluster containing EntraID + PingFederate + PingID MFA + Authle + AD; never as 5 free-floating boxes. The cluster joins the main line with one arrow.
- **Use exact labels from the source `.md` analyses** under `.github/skills/aie-sre-onboarding/Docs/<App>/`. Don't abbreviate `mlwCHATPGPROD`, don't paraphrase `PingFederate Prod Instance`.
- **One-line caption under each diagram** in italics, naming the source — e.g. `*Source: ChatPG - Communication Flow Diagram.md*`.
- **Newbie-readable wins.** When in doubt, simplest picture that still shows the real flow. Cut decorative boxes; keep only what a new SRE actually needs on day one. Offer a *"want me to go deeper?"* follow-up if they want the full picture.

### Request-flow diagrams (a user → a service → back)

Lay the main happy path **left-to-right on one straight horizontal line**. Don't snake. The auth chain (or any side system) sits in one cluster above the line and joins with a single arrow.

**Template:**

```text
                    ┌──────────────── Auth chain ────────────────┐
                    │  Provider A  ──▶  Provider B  ──▶  Provider C │
                    └────────────────────┬─────────────────────────┘
                                         │ ② JWT
                                         ▼
   ┌────────┐   ──①──▶   ┌──────────┐   ──③──▶   ┌──────────┐   ──④──▶   ┌──────────┐
   │  User  │            │ Edge     │            │ Frontend │            │ Backend  │
   │        │   ◀──⑥──   │ (APIM)   │   ◀──⑤──   │          │   ◀──⑤──   │          │
   └────────┘            └──────────┘            └──────────┘            └──────────┘
```

Underneath, the numbered narration:

> ① User opens the app in the browser…
> ② Edge gateway redirects to the auth chain…
> ③ Frontend receives the authenticated session…
> ④ Backend validates the JWT and forwards the prompt…
> ⑤ Response returns through frontend → edge…
> ⑥ Browser renders the answer.

The reader's eye lands on `④` on the picture and jumps to `④` in the list — no ambiguity.

#### Companion view: numbered narrative step boxes (vertical)

When the reader asks for a **deep walk-through** of a request flow, follow the compact horizontal diagram with a vertical stack of step boxes — same flow, different zoom level. This is the style used in the in-house ChatPG architecture reference docs.

Rules:

- One box per step, ordered top-to-bottom, separated by a centred `▼`.
- Box header: `STEP N: TITLE IN CAPS` on the top line.
- Inside each box, 2–6 sub-points using `├─` and `└─` (last item only). One line per sub-point.
- Box width is uniform across the diagram (~82 chars typical). All right-edge `│` characters line up.
- Step numbers in the headers match the circled digits in the horizontal diagram above (`STEP 4` ↔ `④`).
- **Branching / parallel steps** — when one step fans out (e.g. RAG retrieval + SPOCK retrieval), draw `┌──────────┴──────────┐`, place the parallel boxes side-by-side, then re-merge with a matching `└──────────┬──────────┘` before the next sequential step.

**Template:**

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: USER INPUT                                                              │
│ ├─ User types message in Web / Teams / Client                                   │
│ └─ Payload: { user_id, message, conversation_id }                               │
└──────────────────┬──────────────────────────────────────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: HTTPS REQUEST TO APIM GATEWAY                                           │
│ ├─ Encrypted connection (TLS 1.2+)                                              │
│ ├─ Headers: Authorization: Bearer {JWT_TOKEN}                                   │
│ └─ Forward to ChatPG Backend                                                    │
└──────────────────┬──────────────────────────────────────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: JWT VALIDATION (ChatPG Backend)                                         │
│ ├─ Retrieve public key from Azure Key Vault                                     │
│ ├─ Validate signature & expiry                                                  │
│ ├─ Extract user claims (user_id, groups, site_code)                             │
│ └─ USER AUTHENTICATED ✓                                                         │
└──────────────────┬──────────────────────────────────────────────────────────────┘
                   ▼
        ┌──────────┴──────────┬──────────────────┐
        ▼                     ▼                  ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ STEP 4A: RAG     │  │ STEP 4B: SPOCK   │  │ STEP 4C: DEPOT   │
│ ├─ Embed query   │  │ ├─ Authenticate  │  │ └─ (optional)    │
│ └─ Top-K docs    │  │ └─ White-list    │  │                  │
└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
         └─────────────────────┴────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ STEP 5: PROMPT ASSEMBLY                                                         │
│ Final Prompt = System Prompt + RAG Context + Data + History + Query             │
└──────────────────┬──────────────────────────────────────────────────────────────┘
                   ▼
                  ...
```

When to use which view:

| Question | Diagram |
|----------|---------|
| *"Show me ChatPG's request flow"* (overview, ≤30 sec read) | Horizontal numbered diagram only |
| *"Walk me through what happens when a user sends a prompt"* (deep dive) | Horizontal diagram **then** vertical step boxes |
| *"Explain step ④ in more detail"* | Just the matching step box, expanded |

#### Companion view: system integration diagram (top-down layered ecosystem)

When the reader asks **"how does the whole system fit together?"** (rather than tracing a single request), use a top-down layered ecosystem diagram. This shows every external system at once, organised by layer.

It's the single most important diagram on day one — it answers *what is this thing connected to?* in one picture, and it should be the default opener in Section 2 of any "what is this platform?" briefing.

Rules:

- One outer container per layer, stacked top-to-bottom in this order:
  1. **USERS / CLIENTS** — every client surface as its own inner box, with the protocol on the second line — `Web Browser` / `(HTTPS)`, `Teams Client` / `(WebRTC)`, etc.
  2. **EDGE / GATEWAY** — typically one funnel box (Application Gateway, APIM). Client lines converge here.
  3. **AUTH / IDENTITY** — fan out into 2–4 parallel providers (EntraID, PingFederate, Ping MFA, Authle), then re-merge.
  4. **CORE SERVICE** — usually one box for the application itself, with sub-components as `- Frontend (UI)` / `- Backend (API)` bullet lines inside.
  5. **INTEGRATION / DOWNSTREAM** — fan out into the data and AI services the core depends on (SPOCK / GenAI Platform / DEPOT). Children one level lower if needed (Smart Warehouse under SPOCK, Azure Search under GenAI).
  6. **PERSISTENCE side-block** — labelled `Persistence:`, listing the database(s) with key facts inside the box (`32 vCores, 512GB, HA=DISABLED`).
  7. **OBSERVABILITY side-block** — labelled `Observability:`, listing App Insights, Spyglass, etc.

- Connectors are simple `│` lines and a single `▼` between layers — no arrows on every leg. Use a fan-out `┬───┬───┬` when one layer feeds N parallel boxes; a fan-in `┴───┴───┴` when N feed one.
- Annotate critical facts inside the box where it matters: protocols on client boxes, sizing/HA gaps on persistence, external system IDs the SRE will actually need (`SPOCK CI00549570`) — but never raw Azure GUIDs.
- Persistence and Observability are side-blocks below the main vertical chain, not stops on the main flow.

**Template:**

```text
┌─────────────────────────────────────────────────────────────┐
│                       P&G USERS                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ Web Browser  │  │ Teams Client │  │ Client Software  │   │
│  │   (HTTPS)    │  │   (WebRTC)   │  │   (Standalone)   │   │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘   │
└─────────┼─────────────────┼───────────────────┼─────────────┘
          └─────────────────┼───────────────────┘
                            ▼
                  ┌──────────────────┐
                  │ Azure App Gateway│
                  │      (APIM)      │
                  └────────┬─────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
     ┌─────────┐     ┌──────────────┐  ┌──────────────┐
     │ MSFT    │     │ PingFederate │  │ Ping MFA     │
     │ EntraID │     │ (Authorize)  │  │ (2nd factor) │
     └────┬────┘     └──────┬───────┘  └──────┬───────┘
          └─────────────────┼─────────────────┘
                            ▼
                ┌─────────────────────┐
                │   ChatPG Service    │
                │   - Frontend (UI)   │
                │   - Backend (API)   │
                └──────────┬──────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
    ┌────────┐        ┌─────────┐        ┌─────────┐
    │ SPOCK  │        │  GenAI  │        │  DEPOT  │
    │ (Data) │        │ Platform│        │ (Expert)│
    └────┬───┘        └────┬────┘        └─────────┘
         │                 │
         ▼                 ▼
   ┌──────────────┐  ┌──────────────┐
   │ Smart        │  │ Azure Search │
   │ Warehouse    │  │ (RAG)        │
   └──────────────┘  └──────────────┘

   Persistence:
   ┌──────────────────────────────────┐
   │ PostgreSQL Flexible Server        │
   │ (psql-pg-chatpgproddb)            │
   │ 32 vCores, 512GB, HA=DISABLED     │
   └──────────────────────────────────┘

   Observability:
   ┌──────────────┐  ┌──────────────┐
   │ Application  │  │   Spyglass   │
   │   Insights   │  │  (Logging)   │
   └──────────────┘  └──────────────┘
```

When to reach for this view vs. the others:

| Question | Diagram |
|----------|---------|
| *"What is ChatPG connected to?"* / *"Show me the whole system at once"* | System integration diagram (this one) |
| *"How does one request flow?"* | Horizontal numbered request-flow diagram |
| *"Walk me through a request in detail"* | Vertical narrative step boxes |
| *"What lives in which Azure subscription?"* | Infrastructure / deployment diagram (next section) |

### Infrastructure / deployment diagrams

Group components by **Azure subscription** in clearly labelled outer boxes. Subscription name + RG names go on the top border. Inside each subscription box, lay components vertically in logical sub-groups (`Services`, `Network`, `AKS`, …) with a blank line between sub-groups.

**Template:**

```text
┌─ Subscription: <name> ─────────────────────────────┐
│  RGs: <rg-1>, <rg-2>                               │
│                                                    │
│  Services                                          │
│   ┌──────────────────┐  ┌──────────────────┐       │
│   │ Container Reg.   │  │ Key Vault        │       │
│   └──────────────────┘  └──────────────────┘       │
│                                                    │
│  Data                                              │
│   ┌──────────────────┐  ┌──────────────────┐       │
│   │ PostgreSQL flex  │  │ Cache for Redis  │       │
│   └──────────────────┘  └──────────────────┘       │
│                                                    │
│  Network: PGI-VNET (10.99.0.0/16)                  │
│   ┌──────────────────────────────────────────┐     │
│   │ Machine Learning Workspace mlw<APP>PROD  │     │
│   └──────────────────────────────────────────┘     │
└────────────────────┬───────────────────────────────┘
                     │ HTTPS, L7
                     ▼
┌─ Subscription: <other-name> ───────────────────────┐
│  RG: <rg>                                          │
│   ┌──────────────────┐                             │
│   │ AKS cluster      │                             │
│   └──────────────────┘                             │
└────────────────────────────────────────────────────┘

┌─ External ─────────────────────────────────────────┐
│  Spyglass   GenAI Platform   Entra ID   App Insights│
└────────────────────────────────────────────────────┘
```

Discipline:

- **Cross-subscription arrows go between outer boxes**, never from inside one box to inside another. Label each arrow with the protocol on a single line (`HTTPS, L7`, `HTTP, REST`, `Private Link`).
- **Externals at the bottom** in their own `External` cluster — one row of names, no tangled arrows. Reference them only where the connection matters.
- **Equal column widths inside a sub-group.** Misaligned right edges immediately make the picture look wrong.
- **No raw GUIDs in box labels.** If the source `.md` lists hash-style IDs (e.g. `898489C85FBF12AA`), summarise as `AI Factory components (3)` and mention the IDs in the prose under the diagram.

## Setup Onboarding Agent

Verify `uvx` is installed by running `uvx --version` in a terminal.

### Install uv (if needed)

**macOS**
```bash
brew install uv
```

**Windows**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux**
```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

### Configure the MCP servers

Edit `.vscode/mcp.json` in this repo and fill in the user/token inputs for `mcp-atlassian`. Generate a Confluence API token with:

1. Log in to Confluence.
2. Click your avatar → **Account Settings**.
3. Open the **Security** tab.
4. Click **Create and manage API tokens**.
5. **Create API token** → name it, pick an expiration.
6. Copy the token into `mcp.json`.

### Start the server

In VS Code, open the command palette (Cmd/Ctrl + Shift + P) → **MCP: Start Server** → select `mcp-atlassian`. Once it's running, the onboarding agent can hit Confluence directly.
