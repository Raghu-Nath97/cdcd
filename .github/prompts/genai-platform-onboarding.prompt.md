---
description: 'GenAI Platform onboarding overview for a new AIE SRE. Run /genai-platform-onboarding when someone asks "what is the GenAI Platform", "how does it work", "External vs Internal Platform", or anything similar in the first couple of weeks. Pulls evidence from three MCP servers (genai-platform AIF docs MCP, mcp-atlassian for the TURING Confluence page, GitHub MCP for the de-cf-genai-platform repo) plus the local diagram analyses, and produces an 8-section briefing with ASCII flow diagrams. No Mermaid.'
mode: 'agent'
tools: ['vscode', 'read', 'search', 'web', 'browser', 'genai-platform/*', 'mcp-atlassian/*', 'com.atlassian/atlassian-mcp-server/*', 'github/*']
---

# GenAI Platform Onboarding Briefing

This prompt produces a single, focused briefing on the AI Factory GenAI Platform for someone brand new to the AIE SRE team. Treat the reader as someone who hasn't yet learned the AI Factory vocabulary (External Platform vs Internal Platform, Shared Services, AIF, APIM, Traffic Manager, AI Provisioner, AI Apps, AI Observability, GuardRails, SDDE).

The briefing is evidence-based: pull from the live MCP servers and the local docs, never from memory.

## Sources to gather

Work through these in order before writing the briefing.

### 1. The onboarding skill
Read [`.github/skills/aie-sre-onboarding/SKILL.md`](.github/skills/aie-sre-onboarding/SKILL.md) — it carries the canonical Confluence/Jira/Repo links and the full diagram-drawing rules referenced throughout this prompt.

### 2. Local diagram analyses
Read all four `.md` files under `.github/skills/aie-sre-onboarding/Docs/GenAI-Platform/`:

| File | What it covers |
|------|----------------|
| `GenAI ... Application Environment Diagram - Reference Architecture.md` | AED reference template — every persona, AI Factory workspace, external AI provider a UC may connect to |
| `GenAI ... Application Environment Diagram.md` | Actual GenAI Platform AED — concrete personas + AI Factory components (APIM, AI Observability, AI Provisioner, AI Apps, Spyglass, GitHub Enterprise Cloud, CICD) |
| `GenAI ... Technical Infrastructure Diagram - Reference Architecture.md` | TID reference template — Cincinnati GO PGI / Global Internet / Azure zones with port + protocol annotations |
| `GenAI ... Technical Infrastructure Diagram.md` | Actual GenAI Platform TID — Global Internet, PGI, GCP, full Azure subscription / RG layout for External + Internal Platform, plus ChatPG, CICD, Spyglass |

These `.md` files are the structural source of truth for every diagram. The matching `.drawio.png` next to each is for human cross-check only.

### 3. AI Factory documentation MCP — `genai-platform`
Fire at least these five queries (in parallel) against the AIF documentation MCP and harvest the `source_url` from every chunk. The URLs feed Section 6's links table — they need to be evidence-backed, not memorised.

1. *GenAI Platform overview architecture external internal platform*
2. *GenAI Platform auth options headers token project-name userid*
3. *GenAI Platform available models providers Azure OpenAI Vertex AI Anthropic*
4. *GenAI Platform network connectivity guide private endpoint APIM GCP*
5. *GenAI Platform PII content filters governance SDDE*

If the MCP errors out, put one line at the top of the briefing — *"AIF documentation MCP unavailable this turn — `developerportal.pg.com` URLs in Section 6 may be stale; verify before sharing"* — and continue.

### 4. Atlassian MCP — Confluence + Rovo
Run these in parallel:

- **Direct fetch** of the canonical TURING page — page ID `4197351513` (*GenAI Platform*). Pull the body for the narrative the diagrams don't carry: governance posture, available-models nuance, recent changes, owning team.
- **Rovo search** — query `GenAI Platform TURING space` to enumerate sub-pages (architecture, SRE framework, Projects List, External deployments, AI Assistant). Capture each page id, title, URL.
- **CQL** — `space = TURING AND title ~ "GenAI Platform"` for the full title list.

If everything errors out, put one line at the top — *"Atlassian MCP unavailable this turn — briefing built from AIF MCP + GitHub MCP + local Docs/GenAI-Platform/ analyses"* — and continue. Don't retry, don't halt.

### 5. GitHub MCP — `procter-gamble/de-cf-genai-platform`
The repo is the code-level anchor. Fetch:

- `path=/` — top-level layout
- `path=README.md` — quickstart, OpenAI versioning, monitoring, tests
- `path=AGENTS.md` — high-level project structure (when accessible)
- `path=src/aif/genai/api/v1` — provider routers (`openai.py`, `vertexai.py`, `anthropic.py`, `opensource.py`, `guardrails.py`, `mcp_redirect.py`, `streaming_tools.py`, `vertexai_veo.py`, `websockets/`, `agents/`, `operations/`, `*_models/`)

If the GitHub MCP errors out, put one line at the top — *"GitHub MCP unavailable / repo access scoped narrower than entitlement — code-level anchors omitted"* — and continue.

### 6. Jira *(optional)*
Only when the user asks an incident-context question — query the TURING Jira project via the Atlassian MCP (e.g. `project = TURING AND component = "GenAI Platform" ORDER BY created DESC`). Skip otherwise.

### Missing source files
If the diagram `.md` files are missing entirely, stop and tell the user to regenerate the analyses before re-running the slash command. Never draw diagrams from generic GenAI Platform knowledge. If just one is missing, say so and skip the section that depended on it.

## Briefing format — 8 sections, in order

The sections are sequential by design. Keep prose tight; the diagrams do the heavy lifting. Target ~220 lines total.

### 1. GenAI Platform in one paragraph
Three or four sentences in plain language: what the GenAI Platform is, who uses it, and why it's more than a wrapper around Azure OpenAI / Vertex AI / Anthropic — it's the governed enterprise layer with auth, audit, content filters, PII handling, GuardRails, project model, and observability. No raw passthrough. Avoid acronyms here.

### 2. Mental model + system integration diagram
Two parts.

**(a)** A small ASCII block showing the three-layer mental model, followed by a short table mapping each layer to one-line responsibilities pulled from the AED + TID `.md` and the AIF MCP results.

```text
┌──────────────────────────────────────────────────────────────────┐
│                       GenAI Platform                             │
│  ┌──────────────┐  ┌────────────────┐  ┌──────────────────────┐  │
│  │ External     │  │ Internal       │  │ AI Factory Shared    │  │
│  │ Platform     │  │ Platform       │  │ Services             │  │
│  │ (3rd-party + │  │ (P&G internal  │  │ (Provisioner, Apps,  │  │
│  │  GCP-hosted) │  │  apps + Teams) │  │  Observability,APIM) │  │
│  └──────────────┘  └────────────────┘  └──────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

**(b)** A top-down system integration diagram following the *system integration diagram* template in `SKILL.md`. Six layers + two side-blocks:

1. **USERS / CLIENTS** — `Web Browser (HTTPS)`, `Microsoft Teams App (WebRTC)`, `Client Application (HTTPS)`, `GCP-hosted Client (HTTPS)`, `IDE (Git, HTTPS)`. Personas above the row: External API User / P&G API User / P&G Admin / Model Developer.
2. **EDGE / GATEWAY** — `Traffic Manager` → `API Gateway` → `Azure APIM`. Note inline: External and GCP traffic enters via Traffic Manager + API Gateway; PGI traffic enters APIM directly.
3. **AUTH / IDENTITY** — fan out into `MSTF EntraID` and `Ping Federate`, then re-merge.
4. **CORE SERVICE** — two side-by-side boxes, *External Platform* (`tenant-genai-platform-ext-{env}`) and *Internal Platform* (`tenant-genai-platform-{env}`). Each lists `- AI Factory General Service`, `- GuardRails AI`, `- Audit Endpoints`, `- AKS`, `- Container Registry`. Internal additionally lists `- Microsoft Teams`.
5. **INTEGRATION / DOWNSTREAM** — model providers + ML stack from the TID `.md` and the *available-models* AIF doc. Group as Azure OpenAI / Vertex AI / Anthropic / Open-source, plus an ML/Data sub-cluster (Azure ML, Cognitive Search, Cosmos DB, Cache for Redis, ADLS Gen2, Event Hub, AI Speech, Databricks). Show the GCP `<<ABSTRACT PROJECT>>` cluster as one labelled child of the External branch.
6. **PERSISTENCE side-block** — `Persistence:` cluster: `Azure SQL DB`, `Azure CoreML (MLFlow & Torch)`, `Container Registry`, `ML Workspace`.
7. **OBSERVABILITY side-block** — `Observability:` cluster: `AI Factory AI Observability (App Insights)`, `Spyglass`, `GenAI SRE Operations Dashboard`.

Caption: *Source: GenAI AED.md + GenAI TID.md + AIF MCP*.

### 3. How a single user request flows
Two views, both required, sharing the same circled-digit step numbers.

**View 1 — Horizontal numbered request-flow diagram.** Follow the *request-flow diagrams* template in `SKILL.md`: main happy path left-to-right on a single line — `User → Web/Teams/Client → Traffic Manager / API Gateway → Azure APIM → GenAI Platform (Ext or Int) → AKS / GenAI Core + GuardRails → Model Provider`. Auth providers (`Ping Federate`, `MSTF EntraID`) sit in one labelled `Auth chain` cluster above the line, joining with one arrow carrying `Bearer access_token + userid + project-name`. Caption: *Source: GenAI TID.md + AIF auth-options doc*. Then 6–8 plain-English numbered sentences underneath.

**View 2 — Vertical narrative step boxes.** Follow the *numbered narrative step boxes* template in `SKILL.md`. Useful sub-fields per box: `Action`, `Headers`, `Payload`, `Result`. Specific guidance per step:

- **STEP 2 (auth)** — fan out into parallel `STEP 2A: PING FEDERATE (SAML assertion)` and `STEP 2B: ENTRA ID (access_token + refresh_token)`, then re-merge.
- **STEP 3 (headers)** — list `Authorization: Bearer <token>`, `userid: <enduser@pg.com>`, `project-name: <project>`, plus the conditional `pii-data: true` and the GCP-only `Ocp-Apim-Subscription-Key`.
- **STEP 4 (APIM routing)** — call out the External vs Internal decision and the four hostnames: `genai-platform.pg.com` (Internal Prod), `genai-platform-dev.pg.com/stg` (Internal Non-Prod), `genai-platform-ext-stg.pg.com` (External Non-Prod), `genai-platform-dr.pg.com` (Internal Prod DR).
- **STEP 5 (GenAI core)** — mention GuardRails AI + Audit inline.
- **STEP 6 (provider call)** — name provider families only (Azure OpenAI / Vertex AI / Anthropic / Open-source). Don't invent specific model names.

### 4. The stack
Seven bullets, one short line each — no parenthetical IDs, hostnames, or tenant GUIDs (those go in deeper-dives):

- **Edge / ingress** — Traffic Manager + API Gateway + Azure APIM
- **Identity** — Ping Federate + MSTF EntraID (SAML → access/refresh tokens)
- **Compute** — AKS clusters for External + Internal Platform across primary + DR resource groups
- **Model providers** — Azure OpenAI, Vertex AI, Anthropic, Open-source / Foundational
- **Persistence + data** — Azure SQL DB, ADLS Gen2, Cosmos DB, Cache for Redis, Cognitive Search, Event Hub, AI Speech, Databricks, ML Workspace
- **Governance** — GuardRails AI + Audit Components, content filters, PII handling, SDDE
- **Observability + delivery** — AI Factory AI Observability + Spyglass + SRE dashboard; GitHub Enterprise + CICD framework + AI Provisioner + AI Apps

### 5. How the GenAI Platform is run in Azure
One infrastructure diagram from the TID `.md`, following the *infrastructure / deployment diagrams* template in `SKILL.md`. Two side-by-side platform boxes — *External Platform* (`tenant-genai-platform-ext-{env}`) and *Internal Platform* (`tenant-genai-platform-{env}`) — each containing `Service`, `Network`, `AKS` (`AZ-RG-AIF-AKS-MT-EastUS2-Prod` primary + `AZ-RG-AIF-AKS-DR-08-CentralUS-Prod` DR), `Container Registry`. One ML / Data sub-cluster underneath (`ML Workspace mlwgenaiplatform / mlwgenaiplatdev`, `Azure SQL DB`, `Azure CoreML (MLFlow & Torch)`). Externals at the bottom: Spyglass, Ping Federate, EntraID, Microsoft Teams, ChatPG, Azure OpenAI, Vertex AI, Anthropic, Open-source, GCP `<<ABSTRACT PROJECT>>`. No raw GUIDs in box labels — summarise as `AI Factory components (N)`. Caption: *Source: GenAI TID.md*.

Then five short bullets:

- **External vs Internal Platform** — entry path, persona, and audit posture differ; the single most operationally important distinction to internalise
- **How releases ship** — IDE → GitHub Enterprise → CICD framework → AI Provisioner (IaC) → AI Apps; provisioning entry path is the *AI Provisioner ServiceNow Request*, not ad hoc
- **Where secrets / keys live** — Azure Key Vault per subscription (private-endpoint pattern)
- **What is monitored** — AI Factory AI Observability → AI Apps → Spyglass; consumption surfaces only the previous 3 months
- **Where incidents are tracked** — TURING Confluence/Jira + GenAI SRE Operations Dashboard; routing matrix split across GenAI Apps / AI Provisioner / Cloud / AI Observability / AI Monitor

### 6. Where to go next
A 6-row table. Every `developerportal.pg.com` URL must be byte-for-byte identical to a `source_url` returned by the AIF MCP this turn — if the AIF MCP failed, mark that row *(unverified — AIF MCP unavailable)* rather than invent a URL. The local diagrams folder is intentionally not in this table; it's listed in Section 7.

| Resource | Link |
|----------|------|
| GenAI Platform Confluence section (TURING) | https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/pages/4197351513/GenAI+Platform |
| GenAI Platform overview (developerportal) | https://developerportal.pg.com/docs/default/component/ai_factory_general/generative/genai_platform/ |
| Auth options | https://developerportal.pg.com/docs/default/component/ai_factory_general/generative/genai_platform/how_tos/auth-options |
| Available models | https://developerportal.pg.com/docs/default/component/ai_factory_general/generative/genai_platform/reference/available-models |
| Prod Swagger (Internal) | https://genai-platform.pg.com/docs |
| GenAI Platform repository | `https://github.com/procter-gamble/de-cf-genai-platform` |

Wrap the GitHub repo URL in backticks so the chat surface keeps the literal URL visible — auto-linked or markdown-link rendering hides it.

### 7. Reference material on disk
List the `.md` files you actually read this turn (full repo-relative paths under `.github/skills/aie-sre-onboarding/Docs/GenAI-Platform/`), the AIF MCP queries you fired, and the Confluence page id you fetched (or the failure note). Five to seven bullets — enough that a new SRE can replay the same calls.

### 8. Want to go deeper?
End with one focused offer, not a menu. For example:

> *"Want me to walk through the auth chain, the External vs Internal Platform split, the AI Provisioner provisioning flow, model-provider routing in `src/aif/genai/api/v1`, or a recent incident playbook? Pick one and I'll dig in."*

One line. No trailing summary.

## Scope

- **All three MCPs are mandatory** — `genai-platform`, `mcp-atlassian`, `github`. If one fails, surface the matching one-line note at the top and continue with the others. Never silently substitute memory for an MCP that errored.
- **ASCII diagrams only** — never Mermaid or PlantUML. All diagram styles are defined in `SKILL.md`; this prompt only specifies which template to use where.
- **Use exact labels from the source `.md` and the AIF docs** in every diagram. If the source says `AZ-RG-AIF-AKS-MT-EastUS2-Prod`, `mlwgenaiplatform`, `tenant-genai-platform-ext-{env}`, `genai-platform-ext-stg.pg.com`, `Ping Federate` — write that, don't paraphrase. Silently correct only obvious typos against canonical Azure service names (e.g. `Cortex for Redis` → `Cache for Redis`).
- **Don't invent specifics** — incident IDs, Azure GUIDs, retention windows, SLAs, APIM timeouts, quotas. They have to come from the local sources, the onboarding skill, the live MCP results, or the live Confluence/GitHub fetch. If asked about something not covered: *"I don't have that in the onboarding overview — check Swagger, the GenAI Platform AI Assistant page, or the developerportal docs in Section 6."*
- **Newbie language**. Expand each acronym the first time it appears (`AKS (Azure Kubernetes Service)`, `APIM (Azure API Management)`, `AIF (AI Factory)`, `IaC (Infrastructure as Code)`, `SDDE (Sensitive Data De-identification Engine)`, `MFA (multi-factor auth)`, `ADLS Gen2 (Azure Data Lake Storage Gen2)`, `RG (Resource Group)`).
- **Never collapse External and Internal Platform into one box** in any diagram. They have distinct namespaces (`tenant-genai-platform-ext-{env}` vs `tenant-genai-platform-{env}`) and distinct hostnames; that distinction is the operational core of the platform.
- **Length cap ~220 lines** including the diagrams. If you go over, cut prose — never the diagrams or the reference table.
- Don't load `/chatpg-onboarding`, the `github-chatpg` skill, or any LeanIX live-fetch skill for this briefing.
