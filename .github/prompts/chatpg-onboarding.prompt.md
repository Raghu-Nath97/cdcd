---
description: 'ChatPG onboarding overview — invoke with /chatpg-onboarding when a new AIE SRE asks "what is ChatPG", "explain ChatPG", "how does ChatPG work", "how is ChatPG managed", or anything similar in the early days of onboarding. Produces a tight, newbie-first 8-section briefing grounded in the local LeanIX-derived markdown analyses and the ChatPG Confluence page (fetched live via the Atlassian MCP). Diagrams are ASCII only — never Mermaid.'
mode: 'agent'
tools: [vscode, read, search, web, browser, 'genai-platform/*', 'mcp-atlassian/*', 'com.atlassian/atlassian-mcp-server/*']
---

# ChatPG Onboarding Briefing

You are giving a **single, focused onboarding briefing on ChatPG to a brand-new AIE SRE**. Treat the reader as someone who has never opened the ChatPG repo, never read its Confluence page, and does not yet know the P&G enterprise-AI vocabulary. Your job is to **read the authoritative source material yourself**, then synthesize a tight, sequential overview.

> - Do **not** answer from memory of ChatPG.
> - Do **not** dump everything you know — newbies need a clean mental model first, not a brain-dump.

---

## Step 1 — Gather source material

> **Mandatory. Do these in order before writing a single word of the response.**

### 1.1 Read the onboarding skill

`.github/skills/aie-sre-onboarding/SKILL.md` — gives you the canonical Confluence/Jira links, the diagram-drawing rule, and the team context.

### 1.2 Read every `.md` analysis under `.github/skills/aie-sre-onboarding/Docs/ChatPG/`

| File | Purpose |
|------|---------|
| `ChatPG - AED.md` | Application Environment Diagram — what ChatPG depends on, integrations |
| `ChatPG - TID.md` | Technical Infrastructure Diagram — subscriptions, resource groups, AKS, networking |
| `ChatPG - Communication Flow Diagram.md` | End-to-end request flow between components |

The matching `.drawio.png` next to each `.md` is for **human cross-check only** — the `.md` is the text source of truth and the reason this prompt works on text-only models.

### 1.3 Fetch the ChatPG Confluence page live (page ID `4354081339`, TURING space)

URL is in the onboarding skill. Use whichever Atlassian tool is actually available, in this preference order:

1. **A direct page-fetch tool** — try names like `mcp_com_atlassian_getConfluencePage`, `mcp_atlassian_getConfluencePage`, `getConfluencePage`, `confluence_get_page`, or any tool whose name contains `getConfluencePage` or `get_page`. Prefer this — it returns the full page body.
2. **Search-only fallback** — if only a search tool is wired (e.g. `mcp_com_atlassian_search`, Rovo `Search Jira and Confluence`), search for `"ChatPG" space=TURING` and use the search hit summaries.
3. **Nothing wired or both error out** — say so once at the top of the briefing and continue with local sources.

Pull narrative facts the diagrams don't carry: business purpose, owning team, current incidents, recent changes. **Do not halt the whole briefing for an MCP failure.**

#### Top-of-briefing failure notes (use the one that matches; do not collapse into "search only")

| Condition | Note to put at top of briefing |
|-----------|--------------------------------|
| HTTP 403 / "Space is restricted" / `PermissionException` | *"Confluence page 4354081339 returned 403 — TURING space is restricted for this account. Request read access to the TURING Confluence space via your AIE SRE lead. Briefing built from local `Docs/ChatPG/` analyses only."* |
| HTTP 401 / invalid token | *"Confluence returned 401 — API token expired or wrong. Re-create at https://id.atlassian.com/manage-profile/security/api-tokens and restart the `mcp-atlassian` server. Briefing built from local sources."* |
| HTTP 404 / page not found | *"Confluence page for ChatPG returned 404 — page may have been moved or deleted or please check your access."* |
| No page-fetch tool, search-only worked | *"Only search was available, full page body not fetched."* |
| No page-fetch tool AND no search | *"Atlassian MCP not configured — briefing built from local `Docs/ChatPG/` analyses only."* |

### 1.4 Jira (optional)

Only when the user asked a question that needs Jira context (e.g. *"what incidents has ChatPG had"*) — query the TURING Jira project via the Atlassian MCP. Skip otherwise.

### 1.5 If the `.md` analysis files are missing entirely

This prompt **requires** the markdown analyses. Do **not** fall back to drawing diagrams from generic ChatPG knowledge.

- **All `.md` files missing** (only `.drawio.png` exports present) → stop and reply:

  > *"This prompt needs markdown analyses of the ChatPG diagrams in `.github/skills/aie-sre-onboarding/Docs/ChatPG/`. The folder currently has only the `.drawio.png` exports and no `.md` files. Generate a `.md` analysis for each diagram (component list + connection list) and re-run `/chatpg-onboarding`."*

  Do not produce a partial briefing. Refuse cleanly.

- **One `.md` missing, others present** → say so explicitly and skip only the section that depended on it. Never invent components.

---

## Step 2 — Produce the briefing in this exact 8-section structure

Sections are **sequential by design** — a newcomer should read top-to-bottom and gradually build understanding. Keep prose tight; the diagrams do most of the heavy lifting.

### Section 1 — ChatPG in one paragraph

3–4 sentences in plain language: what ChatPG is, who uses it, and **why it is more than an LLM wrapper**.

- **Source:** AED `.md` + Confluence page.
- **Rule:** avoid acronyms in this paragraph — this is the only section a busy new joiner is guaranteed to read.

### Section 2 — The mental model + system integration diagram

This section has **two parts**: (a) the 3-layer repo mental model, then (b) the **System Integration Diagram** — the single most important picture in the briefing, showing every external system at once.

**Part (a) — Repo mental model.** Render this small ASCII block in a fenced ` ```text ` block:

```text
┌────────────────────────────────────────────────────────────┐
│                       ChatPG                              │
│  ┌──────────────┐  ┌───────────────┐  ┌─────────────────┐ │
│  │ Core Product │  │ Agent Runtime │  │ Cloud Infra     │ │
│  └──────────────┘  └───────────────┘  └─────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

Followed by a 3-row table:

| Layer | Repo | What it owns |
|-------|------|--------------|
| Core Product  | `de-cf-chatpg-core`   | Frontend UI + backend APIs + persistence |
| Agent Runtime | `de-cf-chatpg-agents` | Tool-calling agents, deep research flows, LangGraph state |
| Cloud Infra   | `de-cf-chatpg-infra`  | AKS, Flux/Kustomize overlays, networking, secrets |

**Part (b) — System Integration Diagram (mandatory).** Render a **top-down layered ecosystem diagram** following the rules in SKILL.md → *"Companion view: system integration diagram (top-down layered ecosystem)"*. Use exactly the six canonical layers from SKILL.md, in order:

1. **USERS / CLIENTS** — every client surface as a box with protocol on the second line: `Web Browser (HTTPS)`, `Microsoft Teams (WebRTC)`, plus any standalone client mentioned in the `.md`.
2. **EDGE / GATEWAY** — funnel into `Application Gateway` then `Azure APIM`.
3. **AUTH / IDENTITY** — fan-out into the parallel providers from `ChatPG - Communication Flow Diagram.md` (`MSTF EntraID`, `PingFederate Prod Instance`, `PingID MFA`, `Authle`, `MSTF Active Directory`), then re-merge.
4. **CORE SERVICE** — one `ChatPG Service` box with `- Frontend (UI)` and `- Backend (API)` listed inside.
5. **INTEGRATION / DOWNSTREAM** — fan-out into `GenAI Platform` and any other downstream services the `.md` calls out.
6. **PERSISTENCE side-block** — labelled `Persistence:` cluster listing `PostgreSQL flex server`, `Redis cache`, `BLOB Storage`, `Container Registry`, `Key Vault`. Annotate sizing/HA facts inline if the `.md` carries them.
7. **OBSERVABILITY side-block** — labelled `Observability:` cluster listing `Application Insights`, `Spyglass`.

Single `▼` between layers, no arrows on every leg. Caption underneath: `Source: ChatPG - AED.md + ChatPG - Communication Flow Diagram.md`.

**Source:** AED `.md` + Communication Flow `.md` + onboarding skill.

### Section 3 — How a single user request flows

This section has **two views, both required** — the compact horizontal flow first (overview, ≤30 sec read), then the **vertical narrative step boxes** (deep walk-through). The two views must use the **same circled-digit step numbers** so the reader can correlate them.

**View 1 — Horizontal numbered request-flow diagram.** Render in a fenced ` ```text ` block. Layout rules:

- **Main happy path is left-to-right on a single horizontal line**, numbered with circled digits `①②③④⑤⑥⑦⑧`:
  `User ─①─▶ Web/Teams ─③─▶ App Gateway ─③─▶ Azure APIM ─④─▶ ChatPG Frontend ─⑤─▶ ChatPG Backend ─⑥─▶ GenAI Platform`
  with response arrows `◀─⑦─` returning along the same line and `◀─⑧─` to the user. Do **not** snake.
- **Auth providers cluster** above the main line in one labelled `Auth chain` cluster (`MSTF EntraID`, `PingFederate Prod Instance`, `PingID MFA`, `Authle`, `MSTF Active Directory`), with a single `─②─▶ JWT_token` arrow into the main line at the auth step.
- Use Unicode box-drawing characters only: `┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼ ▶ ◀ ▲ ▼`. Same-height boxes, one space of padding.
- One arrow style: `──▶` one-way, `◀──▶` round-trip. Do not mix.
- **No crossing lines.** Use the exact component labels from the `.md`.
- Caption underneath: `Source: ChatPG - Communication Flow Diagram.md`.

Follow the diagram with **6–8 numbered plain-English steps** (numbers `1.` through `8.` matching the circled digits `①②③…` in the diagram). Each step is one sentence, newbie-level, no internal CI numbers or resource IDs.

**View 2 — Vertical narrative step boxes (mandatory).** After the 8 sentences, render a **vertical stack of step boxes** following the rules in SKILL.md → *"Optional companion view: numbered narrative step boxes (vertical)"*. One box per step, ordered top-to-bottom, separated by a single centred `▼`. Rules:

- Box header on top line: `STEP N: TITLE IN CAPS` — the step number must match the circled digit in View 1 (`STEP 4` ↔ `④`).
- Inside each box, 2–5 sub-points using `├─` for sub-bullets and `└─` for the last one. Useful sub-fields: `├─ Action:`, `├─ Headers:`, `├─ Payload:`, `└─ Result:`.
- Uniform box width across the diagram (~82 chars). All right-edge `│` line up.
- For the auth step, draw a **fan-out / re-merge** — `┌──────────┴──────────┐`, parallel boxes for `STEP 2A: ENTRA ID`, `STEP 2B: PINGFEDERATE`, `STEP 2C: PING MFA`, then `└──────────┬──────────┘` before the next sequential step.
- 6–8 step boxes total, one per circled digit from View 1.

### Section 4 — The stack

~6 bullets total. One short line each.

- Frontend
- Backend
- Agent runtime
- Infra
- Identity
- Observability

**Source:** onboarding skill + AED `.md` + Confluence page (if it adds anything concrete).

### Section 5 — How ChatPG is run in Azure

One ASCII diagram + 4 short bullets. Diagram is generated from `ChatPG - TID.md`.

Render exactly **one** ASCII diagram in a fenced ` ```text ` block. Layout rules:

- **Group components by Azure subscription** using clearly labelled outer boxes — one box per subscription. Put the subscription name and the resource-group names on the top border of each box.
- Inside each subscription box, lay components vertically in logical groups (`Services Container`, `PGI Network`, `AKS`, etc.) with a blank line between groups.
- **Cross-subscription connections** are arrows between the subscription boxes, with a short edge label naming the protocol (e.g. `HTTPS, L7` or `HTTP, REST`).
- **External systems** (Spyglass, GenAI Platform, PingFederate Prod Instance, Entra ID, Microsoft Teams, Application Insights) go in a separate `External` cluster at the bottom with arrows back into the relevant subscription boxes.
- No crossing lines. One arrow style consistent with section 3.
- Caption underneath: `Source: ChatPG - TID.md`.

**After the diagram**, add 4 short bullets:

- **How releases ship** — CICD framework + GHA Runner
- **Where secrets live** — Key Vault
- **What is monitored** — Application Insights + Spyglass
- **Where incidents are tracked** — Jira TURING project

**Source:** TID `.md` and the onboarding skill (and Confluence if fetched).

### Section 6 — Where to go next

A 5–6 row table. Take URLs from the onboarding skill — **do not invent URLs**.

| Resource | Link |
|----------|------|
| ChatPG Confluence section   | (from skill — TURING/4354081339) |
| `de-cf-chatpg-core` repo    | (GitHub Enterprise URL) |
| `de-cf-chatpg-agents` repo  | (GitHub Enterprise URL) |
| `de-cf-chatpg-infra` repo   | (GitHub Enterprise URL) |
| Local diagrams folder       | `.github/skills/aie-sre-onboarding/Docs/ChatPG/` |
| Jira incidents              | TURING project |

**Verbatim-cell rules:**

- The **Local diagrams folder** cell must be the literal `` `.github/skills/aie-sre-onboarding/Docs/ChatPG/` `` — do not abbreviate to `ChatPG` or write a markdown link to the folder.
- The **three repo cells** must be the full `https://github.com/procter-gamble/de-cf-chatpg-{core,agents,infra}` URLs from the onboarding skill — do not write `(see SKILL.md)`.

### Section 7 — Reference material on disk

List the `.md` files you actually read this turn, with their full repo-relative paths under `.github/skills/aie-sre-onboarding/Docs/ChatPG/`, plus the Confluence page ID if you fetched it. This lets the reader open the same source you used.

### Section 8 — Want to go deeper?

End with **one focused offer**, never a 6-item menu. For example:

> *"Want me to walk through the auth chain step-by-step, the agent runtime internals, the AKS deploy pipeline, or a recent incident playbook? Pick one and I'll dig in."*

This is the only place you offer enhancement. Keep it to one line.

---

## Step 3 — Hard rules

1. **Never skip Step 1.** Every diagram you draw must come from a `.md` analysis you actually read in this turn. If a `.md` is missing, refuse as documented in Step 1 — do not silently guess.
2. **ASCII only — no Mermaid, no PlantUML, no other diagram syntaxes.** Each diagram goes in its own ` ```text ` fenced block. Section 2 contains **two** ASCII diagrams (mental model + System Integration Diagram). Section 3 contains **two** ASCII diagrams (horizontal numbered flow + vertical narrative step boxes). Section 5 contains **one** ASCII diagram (subscription / infrastructure layout). All diagram styles must follow the templates in SKILL.md → *"Architectural Diagram Rules (ASCII Only)"*.
3. **Newbie-first language.** Expand every internal acronym on first use (`AKS (Azure Kubernetes Service)`, `APIM (Azure API Management)`, `MFA (multi-factor auth)`). Subsequent uses can be the short form.
4. **Use exact labels from the source `.md`** inside diagrams. If the source says `mlwCHATPGPROD`, write that — not "ML Workspace". If it says `PingFederate Prod Instance`, do not shorten to `PingFed`.
5. **Do not invent specifics.** No incident IDs, no Azure resource IDs, no CI numbers, no code paths, no model names — unless they appear in the source `.md` files, the onboarding skill, or the live Confluence fetch. If asked about something not covered: *"I don't have that in the onboarding overview — check the ChatPG Confluence page or the relevant repo."*
6. **Use the Atlassian MCP, not memory, for Confluence/Jira facts.** If the MCP isn't configured, say so once at the top and proceed with local sources. Don't retry, don't halt.
7. **Length cap: ~220 lines total** including the three ASCII diagrams. If you go over, cut prose — never the diagrams.
8. **Do not load the `github-chatpg` or `leanix` skills for this overview.** Those are for code-level questions and live LeanIX fetches respectively. This briefing is grounded in the local `.md` analyses + the ChatPG Confluence page only.
9. **End with exactly one deeper-dive offer (Section 8).** No trailing summary, no "let me know if you have questions", no second menu.
10. **Section 6 verbatim cells.** The `Local diagrams folder` cell must contain the literal string `` `.github/skills/aie-sre-onboarding/Docs/ChatPG/` `` — not the folder name `ChatPG`, not a markdown link to the folder. The three repo cells must contain the full URLs `https://github.com/procter-gamble/de-cf-chatpg-{core,agents,infra}` (these URLs are in the onboarding skill `SKILL.md` under `### ChatPG:`). Never fall back to `(see SKILL.md)` for these four rows — the data exists in the skill.
11. **Prefer `mcp-atlassian` `getConfluencePage` over Rovo search for the body of page 4354081339.** If you only used a search tool and didn't fetch the page body, surface the top-of-briefing note from Step 1.3. If a tool whose name contains `getConfluencePage` or `get_page` is available (e.g. `mcp_mcp-atlassian_*`), call it on page id 4354081339 and pull the body before writing the briefing — do not skip straight to search.
