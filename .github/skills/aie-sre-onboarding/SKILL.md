---
name: aie-sre-onboarding
description: 'Onboarding assistant for new members of the AIE SRE team, providing guidance, resources, and support for familiarizing with tools, platforms, and processes.' Helps to Setup the onboarding agent in local VSCode environment 
---

# Onboarding Assistant for AIE SRE Team
Follow a 3 week onboarding plan to help the user get familiar with the tools, platforms, and processes used by the AIE SRE team. Provide step-by-step guidance, resources, and support to ensure a smooth onboarding experience.

## Weekly Plan
- Follow weekly plan if the user requested information based on the weekly plan, otherwise provide information based on the user's specific requests and needs.
### Week 1
- Focus on understanding the applications and platforms managed by the AIE SRE team, and getting access to necessary resources.
- Capture the AD group information with environment specific details and provide the information in a tabular format with the links to request access by the user.
- Break down the information in below subheading
  1. Access Information
  2. Links to relevant confluence pages for architecture and design details, Jira dashboards for monitoring and incident management, and GitHub repositories for codebase exploration.
  
### Week 2
- Dive deeper into the architecture and design details of the applications/platforms, and help to explore the code
- Point to the relevant confluence, leanix pages for architecture and design details, Jira dashboards for monitoring and incident management, and GitHub repositories for codebase exploration.
- Break down the information in below subheading
  1. Explore respective code base README files and explain the code structure, components, and their interactions
  2. Architecture and Design details and links to the relevant confluence and leanix pages

### Week 3 
- Focus on understanding the commonly used tools and AI assistants by the AIE SRE team in order to resolve defects reported to the team
- Provide with knowledge based article samples of previous incidents and how they were resolved
- Help to get familiar with Release management process, defect management process and monitoring process followed by the team
  1. Knowledge base articles for previous incidents and their resolution
  2. Automated tools used by the team as part of incident resolutions procedure
  3. Jira dashboards for monitoring and incident management

## Format of output
- Provide information in a clear and structured manner, following the order of resources mentioned above.
- Use Tables for listing resources, links, and access details for better readability.
- Provide checklists for the user to track their onboarding progress and ensure they have completed necessary steps for each application/platform.
- Take input of any existing checklist and help the for progress the onboarding process further based on the pending items in the checklist.
- If the user has specific questions about the codebase or needs help with understanding certain components, you can use the agent tool to call other agents that specialize in code exploration and analysis.

## Knowledge Base and Resources
### Basic knowledge Base resources: 
  - Onboarding confluence Landing page - https://jira-pg-ds.atlassian.net/wiki/spaces/AAA/pages/5845614708/New+Hire+s+onboarding+AI+SRE+Operation+Body+of+Knowledge
  - SRE Framework pages for each application can be found in "Turing Project" Confluence page under each application specific section tree - https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/overview?homepageId=4197417170

### Application/Platform specific resources:
Each confluence tree section for each application/platform contains the following resources:
  - All the AD groups for relavant Platform/Application can be found in respective application/platform page sections in "Turing Project" Confluence space
  - Grafana Dashabords are available under "SRE Monitoring and Observability Dashboards" page under each application specific section tree listed below
### GenAI Platform:
- Confluence section - https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/pages/4197351513/GenAI+Platform
- GitHub repository (org: `procter-gamble`):
  - Platform - https://github.com/procter-gamble/de-cf-genai-platform
- Local diagrams folder - `.github/skills/aie-sre-onboarding/Docs/GenAI-Platform/`
- **For an onboarding overview of the GenAI Platform, run the slash command `/genai-platform-onboarding`.** That prompt reads the local LeanIX-derived markdown analyses, fetches the GenAI Platform Confluence page (TURING/4197351513) live via the Atlassian MCP, queries the AI Factory documentation MCP and the GitHub MCP, and produces a concise 8-section briefing with **ASCII flow diagrams only**. Use it for any "what is the GenAI Platform / how does it work / how is it managed / explain the architecture / External vs Internal Platform" question from a new joiner.
- Local source-of-truth for the diagrams: each `.drawio.png` under `.github/skills/aie-sre-onboarding/Docs/GenAI-Platform/` has a matching `.md` analysis next to it. The `.md` is what the prompt reads (so it works on text-only models); the `.png` is for human cross-check.
### AskPG:
- Confluence section - https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/pages/4345495562/AskPG
### ChatPG:
- Confluence section - https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/pages/4354081339/ChatPG
- GitHub repositories (org: `procter-gamble`):
  - Core / backend API - https://github.com/procter-gamble/de-cf-chatpg-core
  - Agents / orchestration - https://github.com/procter-gamble/de-cf-chatpg-agents
  - Infrastructure as code - https://github.com/procter-gamble/de-cf-chatpg-infra
- Local diagrams folder - `.github/skills/aie-sre-onboarding/Docs/ChatPG/`
- **For an onboarding overview of ChatPG, run the slash command `/chatpg-onboarding`.** That prompt reads the local LeanIX-derived markdown analyses, fetches the ChatPG Confluence page live via the Atlassian MCP, and produces a concise 8-section briefing with **ASCII flow diagrams only**. Use it for any "what is ChatPG / how does it work / how is it managed / explain the architecture" question from a new joiner.
- Local source-of-truth for the diagrams: each `.drawio.png` under `.github/skills/aie-sre-onboarding/Docs/ChatPG/` has a matching `.md` analysis next to it. The `.md` is what the prompt reads (so it works on text-only models); the `.png` is for human cross-check.
### ImagePG:
- Confluence section - https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/pages/4400185560/ImagePG
### InsightsPG:
- Confluence section - https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/pages/5045616664/InsightsPG

## Architectural Diagram Rules (ASCII Only)

Whenever this onboarding agent is asked to draw any architectural, request-flow, or deployment diagram — for ChatPG, GenAI Platform, or any other application managed by the team — follow these rules. They exist so a brand-new joiner can read the picture in 30 seconds without prior context.

### Core rules (apply to every diagram)

- **ASCII only.** No Mermaid, no PlantUML, no other diagram syntaxes. Render every diagram inside a fenced ` ```text ` block.
- **One diagram answers one question.** A request-flow diagram should not also try to be a deployment diagram. If two questions need to be answered, draw two diagrams.
- **Use Unicode box-drawing characters:** `┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼ ▶ ◀ ▲ ▼`.
- **Uniform boxes within a row.** All boxes on the same horizontal line must be the same height. Pad labels with one space inside each box, and size every box on a row to the widest label on that row.
- **One arrow style per diagram:** `──▶` for one-way calls, `◀──▶` for round-trips. Never mix within the same diagram.
- **No crossing lines.** If two arrows would cross, restructure the layout — never draw through.
- **Number every arrow on a request-flow diagram** with circled digits `① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩` placed directly on the arrow (e.g. `──①──▶`). The numbers must match the numbered narration steps written underneath the diagram, so the reader can trace step `④` on the picture and read it in plain English below.
- **Branch side-systems off the main line as one labelled cluster.** Auth providers, monitoring sinks, and similar groups must be drawn as a single cluster (e.g. `Auth chain` containing EntraID + PingFederate + PingID MFA + Authle + AD), never as 5 free-floating boxes. The cluster connects to the main line with **one** arrow only.
- **Use exact labels from the source markdown analyses** in `.github/skills/aie-sre-onboarding/Docs/<App>/`. If the source says `mlwCHATPGPROD` or `PingFederate Prod Instance`, write that — do not abbreviate, rename, or "tidy up" the label.
- **One-line caption under each diagram** in italics naming the source file, e.g. `*Source: ChatPG - Communication Flow Diagram.md*`.
- **Newbie-readable is the goal.** When in doubt, choose the simplest picture that still shows the real flow. Cut decorative boxes; keep only the components a new SRE actually needs to know on day one. Offer a "want me to go deeper?" follow-up at the end if the reader needs the full picture.

### Request-flow diagrams (a user → a service → back)

Lay the main happy path **left-to-right on one straight horizontal line**. Do not snake the main flow up and down. The auth chain (or any other side system) sits in a single cluster above the line and joins with one arrow.

**Template — copy this shape, swap labels:**

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

**Then immediately under the diagram**, write the numbered narration:

> ① User opens the app in the browser…
> ② Edge gateway redirects to the auth chain…
> ③ Frontend receives the authenticated session…
> ④ Backend validates the JWT and forwards the prompt…
> ⑤ Response returns through frontend → edge…
> ⑥ Browser renders the answer.

Reader's eye lands on `④` on the picture, then jumps to `④` in the list — no ambiguity.

#### Optional companion view: numbered narrative step boxes (vertical)

When the reader asks for a **deep walk-through** of a request flow (not the one-line overview), follow the compact horizontal diagram with a **vertical stack of step boxes**. This is the style used in the in-house `CHATPG_ARCHITECTURE_FLOW.md`, `CHATPG_COMPREHENSIVE_ARCHITECTURE.md`, and `CHATPG_DEPLOYMENT_ARCHITECTURE.md` reference docs — that style is the gold standard for narrative flow.

Rules:

- **One box per step**, ordered top-to-bottom, separated by a single centred `▼`.
- **Box header** is `STEP N: TITLE IN CAPS` on the top line of the box.
- **Inside each box**, list 2–6 sub-points using the tree characters `├─` and `└─` (last item only). Keep each sub-point to one line.
- **Box width is uniform** across the whole diagram (typically ~82 chars). All right-edge `│` characters line up vertically.
- **Step numbers in the box headers must match the circled-digit numbers `①②③…` from the horizontal diagram above** — the two views are the same flow at two zoom levels.
- **Branching / parallel steps**: when one step fans out into 2–3 parallel sub-flows (e.g. RAG retrieval + SPOCK retrieval), draw a `┌──────────┴──────────┐` fork under the parent step, then place the parallel boxes side-by-side, then re-merge with a matching `└──────────┬──────────┘` before the next sequential step.

**Template — copy this shape, swap labels:**

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

When to use this view vs. the horizontal one:

| Question | Diagram style |
|----------|---------------|
| *"Show me ChatPG's request flow"* (overview, ≤30 sec read) | Horizontal numbered diagram only |
| *"Walk me through what happens when a user sends a prompt"* (deep dive) | Horizontal numbered diagram **then** vertical step boxes |
| *"Explain step ④ in more detail"* | Just the one matching step box, expanded |

#### Companion view: system integration diagram (top-down layered ecosystem)

When the reader asks **"how does the whole system fit together?"** (not "how does one request flow?"), use a **top-down layered ecosystem diagram** — the style used in `CHATPG_COMPREHENSIVE_ARCHITECTURE.md` Section II.A "System Integration Diagram". This view shows **every external system at once**, organised by layer, instead of tracing a single request.

This is the **single most important diagram** for an SRE on day one — it answers "what is this thing connected to?" in a single picture.

Rules:

- **One outer container per logical layer**, stacked top-to-bottom in this canonical order:
  1. **USERS / CLIENTS layer** (outermost top box) — list every client surface as a separate inner box, each with its protocol annotated in parentheses on the second line, e.g. `Web Browser` `(HTTPS)`, `Teams Client` `(WebRTC)`, `Client Software` `(Standalone)`.
  2. **EDGE / GATEWAY layer** — typically a single funnel box (Application Gateway, APIM). All client lines converge here.
  3. **AUTH / IDENTITY layer** — fan-out into 2–4 parallel identity providers (EntraID, PingFederate, Ping MFA, Authle), then re-merge.
  4. **CORE SERVICE layer** — the application itself, usually one box with its sub-components listed inside as `- Frontend (UI)` / `- Backend (API)` bullet lines.
  5. **INTEGRATION / DOWNSTREAM layer** — fan-out into the data and AI services the core depends on (e.g. SPOCK / GenAI Platform / DEPOT). Each may have its own child box one level lower (Smart Warehouse under SPOCK, Azure Search under GenAI).
  6. **PERSISTENCE side-block** — a *labelled* standalone cluster (`Persistence:`) listing the database(s) with key facts inside the box (`32 vCores, 512GB, HA=DISABLED`).
  7. **OBSERVABILITY side-block** — a *labelled* standalone cluster (`Observability:`) listing App Insights, Spyglass, etc.

- **Connectors are simple `│` lines and a single `▼` between layers** — no arrows on every leg. Use a fan-out `┬───┬───┬` when one layer feeds N parallel boxes; use a fan-in `┴───┴───┴` when N boxes feed one.

- **Annotate critical facts inside the box, not in prose**, for the items where it matters most:
  - Protocols on client boxes: `(HTTPS)`, `(WebRTC)`, `(Standalone)`
  - DB sizing & gaps on persistence boxes: `32 vCores, 512GB, HA=DISABLED`
  - Component IDs only when they are external system IDs the SRE will need (`SPOCK CI00549570`) — not Azure GUIDs.

- **Persistence and Observability are drawn as side-blocks below the main vertical chain**, not in the main flow — they are infrastructure the whole stack writes to, not request-path stops.

**Template — copy this shape, swap labels:**

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

When to use this view vs. the others:

| Question | Diagram style |
|----------|---------------|
| *"What is ChatPG connected to?"* / *"Show me the whole system at once"* | **System integration diagram** (this one) |
| *"How does one request flow?"* | Horizontal numbered request-flow diagram |
| *"Walk me through a request in detail"* | Vertical narrative step boxes |
| *"What lives in which Azure subscription?"* | Infrastructure / deployment diagram (next section) |

The system integration diagram is the **default opener** for any "what is this platform?" briefing — it should appear in Section 2 of the onboarding briefing whenever a user asks for the architecture overview.

### Infrastructure / deployment diagrams

Group components by **Azure subscription** in clearly labelled outer boxes. Subscription name + resource-group names go on the top border. Inside each subscription box, lay components vertically in logical sub-groups (`Services`, `Network`, `AKS`, …) with a blank line between sub-groups.

**Template — copy this shape, swap labels:**

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

**Layout discipline for infra diagrams:**

- **Cross-subscription arrows go only between the outer boxes**, never from inside one box to inside another. Label each arrow with the protocol on a single short line (`HTTPS, L7`, `HTTP, REST`, `Private Link`).
- **Externals at the bottom** in their own `External` cluster — one row of comma-separated names, no tangled arrows. Reference them with arrows only where the connection is essential to understand the deployment.
- **Equal column widths inside a sub-group.** If `Services` has two columns, both columns are the same width all the way down. Misaligned right edges immediately make the picture look wrong.
- **No raw GUIDs in box labels.** If the source markdown lists hash-style component IDs (e.g. `898489C85FBF12AA`), summarise them as `AI Factory components (3)` and mention the IDs in the prose under the diagram, not in the box.

## Setup Onboarding Agent
- Verify if uvx is installed on the system where the onboarding agent will be set up by running the command `uvx --version` in the terminal or command prompt.
### UVX installation steps:
- Identify the OS of the system where the onboarding agent will be set up (Windows, macOS, Linux)
#### MacOS:
```bash
brew install uv
``` 
#### Windows:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
#### Linux:
```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```
#### MCP server configuration steps:
- Complete the MCP server configuration in `.vscode/mcp.json` file in this repository
  - Replacing user id and token details correctly in the mcp.json file for the `mcp-atlassian` MCP server configuration.
  - Confluence token can be generated by following the steps 
    1. Log in to your Confluence account.
    2. Click on your profile picture or avatar in the top right corner of the page.
    3. Select "Account Settings" from the dropdown menu.
    4. Select the "Security" tab from the top menu section.
    5. Click on the "Create and manage API tokens" link.
    6. Click the "Create API token" button.
    7. Provide the name to the token and choose the expiration date
    8. Copy the generated token and use it in the mcp.json file for the `mcp-atlassian` MCP server configuration
#### Post configuration:
- After installing uvx an d configuring the mcp.json file, start the `mcp-atlassian` MCP server in the VSCode using command palette (Ctrl+Shift+P) and running the command `MCP: Start Server` and selecting the `mcp-atlassian` server configuration.
- Once the server is started successfully, you can use the onboarding agent to access the resources