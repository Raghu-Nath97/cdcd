---
name: chatpg
description: 'End-to-end onboarding and reference skill for ChatPG — P&G''s enterprise AI platform built on the GenAI Platform. Use whenever a user asks anything about ChatPG: what it is, how it works, its architecture, repositories, request flow, authentication, infrastructure, databases, integrations (SPOCK, DEPOT, Smart Warehouse, AskPG, GenAI Platform, Azure Search, Teams), observability (Application Insights, Spyglass), deployment discipline, known incidents (TURING-896), open risks, or SRE troubleshooting. Covers the full journey from "what is ChatPG?" at zero-knowledge level all the way to advanced architecture, auth sequence, and incident-response playbooks. Also use when the user mentions any of the canonical names: de-cf-chatpg-core, de-cf-chatpg-agents, de-cf-chatpg-infra, psql-pg-chatpgproddb, mlwCHATPGPROD, aks-aif-mt-prod-12-vnet, AZ-RG-AIP-MLWCHATPGPROD, CI004178244, Authie, Pygentic, IPA, LangGraph flows in ChatPG, or any ChatPG Confluence page (6571458581, 4462051968, 4462053377, 4462052289, etc.).'
---

# ChatPG — End-to-End Onboarding and Reference

This skill is the single source of truth for onboarding and day-to-day reference on **ChatPG**, P&G's enterprise AI platform. It is designed so that a newcomer with zero prior knowledge can read it start-to-finish and come out with a working, operational understanding of ChatPG — and so that an experienced SRE can jump to any section and find the specific fact they need.

Read it in order the first time. After that, use the table of contents to jump.

---

## Table of Contents

0. How to use this skill
1. Part I — Foundations: what ChatPG actually is
2. Part II — The three repositories
3. Part III — The request lifecycle and four execution patterns
4. Part IV — The authentication chain (in detail)
5. Part V — Infrastructure
6. Part VI — Integrations ecosystem
7. Part VII — Observability
8. Part VIII — Deployment discipline
9. Part IX — Known incidents and open items
10. Part X — SRE troubleshooting playbook
11. Part XI — SRE scope vs Operations scope
12. Reference A — Confluence pages
13. Reference B — Repositories
14. Reference C — P&G configuration item (CI) numbers
15. Reference D — Azure resource names
16. Reference E — Key URLs
17. Glossary
18. Confidence discipline (verified vs inferred)

---

## 0. How to use this skill

### When to trigger this skill

Trigger this skill whenever any of the following happen:

- A user asks "what is ChatPG?", "explain ChatPG", "how does ChatPG work?"
- A user asks anything about ChatPG's architecture, repositories, auth, database, infra, deployments, integrations, observability, incidents, or troubleshooting.
- A user mentions any canonical ChatPG name: `de-cf-chatpg-core`, `de-cf-chatpg-agents`, `de-cf-chatpg-infra`, `psql-pg-chatpgproddb`, `mlwCHATPGPROD`, `aks-aif-mt-prod-12-vnet`, Authie, Pygentic, IPA, TURING-896, SPOCK (CI005149570), DEPOT (CI003018365), Smart Warehouse (CI002884484), `CI004178244`.
- A user pastes a ChatPG-related error, log line, or alert.
- A user is working through the AIE SRE onboarding plan and reaches the ChatPG-specific section.

### How to answer

1. Answer from the content in this skill first. Do not go hunting across Confluence, GitHub, or the web for things already covered here.
2. When a user needs to verify something live (for example, "is the DB actually on a private endpoint right now?"), point them to the exact Azure Portal path or Confluence page — see Reference A and Reference D.
3. Respect the confidence discipline in Section 18 — when the user asks about something not confirmed, say so explicitly.
4. Use tables, step lists, and sequence walkthroughs when that helps; use prose when the answer is one idea.
5. If the user is a newcomer, walk them through Part I before diving deeper. If they are advanced, jump straight to the section they asked about.

### Companion skills

- **`github-chatpg` skill** (`.github/skills/github-chatpg/SKILL.md`) — when the user asks for the *actual code*, not the concept. Covers the three ChatPG repos (`de-cf-chatpg-core`, `-agents`, `-infra`) with a map of where auth / routes / flows / overlays / secrets live, plus query recipes. Read this skill's Section 4 first so the code lookup is targeted, then hand off.
- **`leanix` skill** (`.github/skills/leanix/SKILL.md`) — when the user asks to *see* an architecture diagram, fetch the *latest* picture from LeanIX, or cross-check this skill against LeanIX. It wraps a Playwright script that logs into `pg.leanix.net` via SSO and exports diagrams as PNGs. Particularly relevant for Section 9.2 (the disputed DB network access) — a fresh LeanIX diagram may help resolve the discrepancy.
- **Confluence (via `mcp-atlassian`)** — use for narrative, rationale, procedures, and incidents. Page IDs are in Reference A.
- **Spyglass (via `spyglass-mcp`)** — use for logs and traces, not for architecture questions.

**Ordering rule:** concepts → diagrams → code → logs. Answer with this skill first, pull diagrams from LeanIX if the user needs to *see* something, drop into GitHub when the user wants the code, and reach for Spyglass when investigating a live incident.

---

## 1. Part I — Foundations: what ChatPG actually is

### 1.1 The one-minute answer

ChatPG is **P&G's enterprise AI chat platform**. It is the product that P&G employees use to have AI-powered conversations, do deep research, ask questions grounded in internal knowledge, and interact with enterprise data — accessed through a web browser or Microsoft Teams.

Under the hood, ChatPG is **not just a chatbot**. It is an orchestration platform that:

- Authenticates users through the enterprise identity stack (Azure APIM → Entra ID → PingFederate → PingID MFA → Authie JWT).
- Receives a user prompt and decides what kind of request it is (direct answer, retrieval-augmented, structured-data, or agent-workflow).
- Calls supporting systems (Azure Search for retrieval, SPOCK/Smart Warehouse/DEPOT for business data, AskPG for knowledge, the GenAI Platform for model execution).
- Runs advanced workflows (deep research, human-in-the-loop, supervisor/swarm patterns) through a dedicated agent runtime.
- Returns the result to the user and ships telemetry to Application Insights and Spyglass.

ChatPG is **also consumed as a service by other P&G apps** — for example, SPOCK (the Structured Processing of Comments Knowledge app) calls ChatPG's API to execute LLM chat requests from within its own workflow.

### 1.2 What ChatPG is NOT

Common misconceptions worth clearing up early:

- **ChatPG is not a model.** It does not host the LLM. The GenAI Platform is the model execution layer that ChatPG calls.
- **ChatPG is not a single service.** It is a product made of a frontend, a backend, a dedicated agent runtime, and a cloud deployment — each in its own repository.
- **ChatPG is not limited to direct end-user chat.** Other P&G apps consume it as an LLM-as-a-service.
- **ChatPG is not the same as AskPG, ImagePG, InsightsPG, or AIAPPS.** Those are sibling applications in the same GenAI Platform ecosystem. See Reference C.

### 1.3 Who uses ChatPG

Three user personas matter, and they reach the platform through different paths:

| Persona | Entry | Primary use |
|---|---|---|
| **P&G User** (employee) | Web browser, Microsoft Teams (MDM device) | Chat, ask questions, run deep research, get knowledge-grounded answers |
| **P&G Admin / AI Engineer / AI Factory Operations** | Web browser via an admin UI | User and task administration |
| **P&G Model Developer / AI Engineer / Model Ops Engineer** | IDE + Web browser | Source code work against GitHub Enterprise Cloud (P&G Org), CI/CD pipeline execution against AI Factory Azure Workspaces |

Other P&G applications (e.g. SPOCK) also call ChatPG via API.

### 1.4 The three-layer mental model

The cleanest mental model separates ChatPG into **three layers**, each owned by its own repository:

| Layer | What it is | Repository |
|---|---|---|
| **Core Product** | The app users experience — frontend, backend APIs, session, persistence, product features | `de-cf-chatpg-core` |
| **Agent Runtime** | Advanced AI workflows — deep research, human-in-the-loop, supervisor/swarm flows, AskPG agent tool use | `de-cf-chatpg-agents` |
| **Cloud Infrastructure** | Deployment and runtime operations — AKS, GitOps, secrets, routing, multi-environment, DR | `de-cf-chatpg-infra` |

Users see one product. Engineers operate three layers. Keep this picture at the front of your mind — everything else is a detail that slots in somewhere under one of these three.

---

## 2. Part II — The three repositories

### 2.1 de-cf-chatpg-core — the main product application

**Job:** Build the actual ChatPG product that users experience.

**Owns:** Frontend UI, backend APIs, business logic, persistence, feature routing, product integrations, Microsoft Teams packaging.

**Technology stack:**

| Layer | Technologies |
|---|---|
| Frontend | React, TypeScript, Nx (monorepo), Vite, React Router, React Query, Material UI |
| Backend | Python 3.12, FastAPI, Celery, Redis, PostgreSQL |

**What the frontend does:** Renders chat screens, feature pages, navigation, dialogs, forms. Manages authenticated API calls. **Does not** do AI reasoning — it is the delivery layer.

**What the backend does:**
- Receives authenticated requests from the frontend.
- Loads session and conversation context from PostgreSQL.
- Classifies the request (direct / retrieval / structured-data / agentic).
- Chooses the execution path.
- Calls retrieval, structured-data, knowledge, agent, or model execution systems as needed.
- Orchestrates the response and ships telemetry.

**Role of each core technology:**

| Tech | Role |
|---|---|
| FastAPI | Main web API framework — routes, typed request/response models, async handling |
| Celery | Background and async work that should not block the main API thread |
| Redis | Caching, Celery broker, fast runtime coordination |
| PostgreSQL | Durable state — conversation history, session state, user preferences, metadata, analytics records |

### 2.2 de-cf-chatpg-agents — the advanced workflow engine

**Job:** Run AI workflows that are too complex for a single request-response cycle — multi-step, tool-using, stateful, or requiring human review.

**Owns:** LangGraph flows, IPA endpoints, Pygentic agent workflows, deep-research flows, human-in-the-loop flows, AskPG agent flows, A2A / supervisor / swarm execution patterns, Redis-backed checkpointers, Phoenix/Arize observability hooks.

**Technology stack:**

| Component | Purpose |
|---|---|
| **Pygentic** | Enterprise agent framework — agent abstractions, prebuilt patterns, AI service integration helpers, observability utilities |
| **IPA** | Serving and endpoint layer — exposes agent flows as callable services, handles auth-aware endpoint behavior |
| **LangGraph** | Stateful workflow orchestration — models workflows as state + nodes + edges, supports pause/resume |
| **LangChain** | Model/tool building blocks — agent creation primitives, message patterns, runnables |
| **Redis checkpointers** | Persist workflow state so graphs can pause, survive restarts, and resume |
| **Phoenix / Arize** | Observability for agent workflows — traces, evaluations |

**Core mental distinction:** LangChain gives you the building blocks (model, tool, agent). LangGraph gives you the workflow around them (state, nodes, edges, routing).

**Flow types that live here:**

| Flow | What it does |
|---|---|
| General chat agent | Configurable chat-style flow |
| AskPG agent | Agent that uses AskPG as a tool inside a workflow |
| Deep research flow | Multi-stage: detect intent → generate queries → gather info → reflect on gaps → loop → draft → finalize |
| Human-in-the-loop flow | Can pause for human review / edit / accept / ignore / respond |
| Supervisor / swarm / prompt-chaining | Multi-agent orchestration patterns |

### 2.3 de-cf-chatpg-infra — the deployment and operations layer

**Job:** Deploy and operate ChatPG in real cloud environments.

**Owns:** AKS manifests, FluxCD GitOps setup, Kustomize overlays, Istio routing, secrets wiring, environment definitions (dev / sandbox / uat / preprod / prod / dr), operational controls, DR configuration.

**Technology stack:**

| Tech | Role |
|---|---|
| **AKS** (Azure Kubernetes Service) | Runtime platform where workloads actually run |
| **FluxCD** | GitOps reconciliation — watches desired state in Git and aligns the cluster to it |
| **Kustomize** | Base manifests plus per-environment overlays |
| **Istio** | Traffic, routing, ingress, maintenance-mode patterns |
| **Azure Key Vault + External Secrets** | Secure secret storage and delivery into pods |
| **Azure Container Registry (ACR)** | Image repository for AKS pulls |

**Environments:** `dev`, `sandbox`, `uat`, `preprod`, `prod`, `dr` — each as a Kustomize overlay on a shared base.

### 2.4 How the three repositories work together

**Normal product request:**

```
User → UI → Core backend → Context + classification → Integrations / AI path → Response → User
```

**Advanced workflow request:**

```
User → UI → Core backend → Core delegates to Agents runtime → LangGraph workflow → Result → Core → User
```

**Runtime in all cases:**

```
Infra repo deploys Core and Agents to AKS, wires Redis + PostgreSQL + Key Vault + ingress + routing
```

Memorize this one line: **Core owns product behavior. Agents owns advanced workflow behavior. Infra owns runtime behavior.**

---

## 3. Part III — The request lifecycle and four execution patterns

### 3.1 The twelve-step lifecycle

Every request goes through this sequence. Keep it in your head.

1. User types a prompt in the ChatPG UI (web browser or Microsoft Teams).
2. Frontend captures the input and sends it to the backend API.
3. Enterprise entry and identity — Application Gateway → Azure APIM → Entra ID → PingFederate → PingID MFA → Authie JWT. The backend only sees authenticated requests.
4. Core backend receives the authenticated request.
5. Core backend loads session / conversation context from PostgreSQL.
6. Core backend classifies the request (direct / retrieval / structured-data / agentic).
7. Core backend chooses the execution path.
8. Supporting systems are called as needed — Azure Search, SPOCK, Smart Warehouse, DEPOT, AskPG, the Agents runtime, the GenAI Platform.
9. Prompt assembly and/or workflow execution happens.
10. Result is formatted, traced, and telemetry is shipped to Application Insights and Spyglass.
11. Response is returned to the frontend.
12. Frontend renders it for the user.

### 3.2 The four execution patterns

Not every request goes through every system. Based on the classification at step 6, the backend picks one of four paths.

#### Pattern A — Direct product answer

For simple explanation-style prompts: "What is ChatPG?", "Explain this feature".

```
Frontend → Core Backend → Load Context → Build Prompt → GenAI Platform → Return Answer
```

No retrieval, no tools. Core backend handles it with its own logic and a direct model call.

#### Pattern B — Retrieval-augmented (RAG)

For knowledge-grounded prompts: "Find the deployment architecture details", "What do the docs say about X?".

```
Frontend → Core Backend → Retrieve (Azure Search / AskPG) → Add Context → GenAI Platform → Return Answer
```

The system fetches supporting context first, then answers — avoids model guessing.

#### Pattern C — Structured business data

For business questions: "What were our Q1 sales?", "Show performance metrics for this site".

```
Frontend → Core Backend → Structured Data Services (SPOCK / Smart Warehouse / DEPOT) → Structured Results → GenAI Platform (for explanation) → Return Answer
```

The **model does not invent the numbers**. It explains retrieved data.

#### Pattern D — Agentic workflow

For complex, multi-step, tool-using, or human-in-the-loop requests: deep research, AskPG agent flows, supervisor/swarm orchestration.

```
Frontend → Core Backend → Agents Runtime (LangGraph) → Multi-Step Workflow (may loop, may pause for HIL) → Result → Core → User
```

This is where the `de-cf-chatpg-agents` repo is engaged. Inside the agent runtime:

1. Create or load workflow state (Redis checkpointer).
2. Decide which graph node runs next.
3. Call tools or knowledge sources.
4. Reflect, request more info, continue research as needed.
5. Pause for human review if configured.
6. Finalize and return.

### 3.3 Key runtime facts

- The **model call is usually not the first step.** It is one step inside a broader orchestration.
- **Tools and integrations run before the model** in retrieval, structured-data, and many agent patterns.
- **PostgreSQL and Redis serve different roles:** PostgreSQL is durable product memory (conversations, sessions, preferences, analytics). Redis is fast operational memory and coordination (cache, Celery broker, agent checkpointers).
- **Celery exists** because not every piece of work should block the API response thread — it handles background processing.

---

## 4. Part IV — The authentication chain (in detail)

This is the single most important operational sequence to understand. Get this right and most "ChatPG won't let me in" incidents are triage-able in minutes.

### 4.1 Why ChatPG uses federated auth

ChatPG uses **Entra ID federated with PingFederate**. The reason, called out on the official flow diagram, is:

> "Auth is done with Entra ID and Federated with Ping because of lack of generation of token on behalf of user."

In practice: Microsoft Entra ID cannot produce on-behalf-of tokens for Ping-federated users in this setup, so an internal trust broker — **Authie** — is used to mint a JWT that ChatPG services trust.

### 4.2 The components in the auth chain

| Component | Role |
|---|---|
| **Application Gateway** | First Azure-side entry point |
| **Azure APIM** | API management, policy enforcement, redirect handling |
| **MSFT Entra ID** | Primary identity provider for P&G |
| **Ping Federate** | Federated identity provider; supports SAML handoff |
| **PingID MFA** | Multi-factor authentication step |
| **ChatPG Frontend** | Receives the authenticated user, asks backend to validate |
| **ChatPG Backend** | Validates JWT signature via public key from Authie |
| **Authie** | P&G's internal token broker — stores access/refresh tokens, resolves user groups against MSFT Active Directory, issues JWTs for ChatPG |
| **MSFT Active Directory** | Source of truth for user group membership |
| **GenAI Platform** | The model execution target — ChatPG authenticates to it with *app* credentials, not user tokens |

### 4.3 The sequence (first visit)

1. `WebBrowser/Teams App` → `call chatPG service()` → Application Gateway → APIM → ChatPG Frontend.
2. Frontend sees the user is unauthenticated. Returns a redirect to `security/v1/auth/authorize`.
3. Browser follows the redirect, hits Entra ID's login page.
4. User provides email → Entra ID redirects to the login form.
5. User authenticates with credentials.
6. Entra ID issues a redirection to PingID with an authorisation_code.
7. **PingID MFA** step.
8. PingID returns a **SAML assertion** carrying the authorisation_code back to Entra ID.
9. Authie receives `send authorisation_code` → exchanges it for `access_token` + `refresh_token` + `login`.
10. Authie **saves** access_token and refresh_token.
11. Authie calls Entra ID: `check_user_groups(access_token)` → validation_result.
12. Authie calls MSFT AD: `get_user_groups(login)` → `user_groups`.
13. Authie **generates a JWT token** with `(login, user_groups)` as its claims.
14. JWT token flows back to the browser.
15. Browser now calls ChatPG with the JWT: `call chatPG service(JWT_token)`.
16. ChatPG Frontend asks Backend: `check_access(JWT_token)`.
17. Backend calls Authie: `get_public_key()` → receives Authie's public key.
18. Backend validates the JWT signature against that public key.
19. On success, the application page is served.
20. The user sends their first prompt: `call chatPG from client side(JWT_token, prompt)`.
21. Backend authenticates to the GenAI Platform using `chatPG_app_credentials` (**app-to-app** credentials — not the user's token).
22. GenAI Platform executes the prompt and returns results.
23. Results flow back through Backend → Frontend → Browser.

### 4.4 Returning requests

Once the user has a valid JWT, subsequent requests skip steps 2–14. The browser just sends `(JWT_token, prompt)` and the Backend validates the signature (steps 16–18) before processing.

### 4.5 Practical consequences for SRE

- **A user who "can't log in"** — check steps 2–14: APIM policy, Entra ID reachability, PingFederate availability, PingID MFA, Authie reachability, MSFT AD query for `get_user_groups`.
- **A user who logs in but sees errors on every chat** — check steps 16–22: Backend JWT validation (is Authie's public key endpoint reachable?), `chatPG_app_credentials` validity (has the secret expired or rotated?), GenAI Platform health.
- **JWT signature failures** → Backend's cached public key may be stale, or Authie rotated keys.
- **App-credentials failures to GenAI Platform** → check Key Vault; the service principal credentials are stored there and pulled via External Secrets.

---

## 5. Part V — Infrastructure

### 5.1 Subscription layout (from the April 2025 Technical Infrastructure Diagram)

ChatPG's infrastructure spans **three subscription groups**:

| Subscription | Resource Groups | Purpose |
|---|---|---|
| **PG-NA-External-<Prod/NonProd>-08** | `AZ-RG-AIP-MLWCHATPGPROD`, `AZ-RG-AIP-MLWCHATPGPROD-DR` | Services container — PostgreSQL, Redis, Key Vault, Blob, Container Registry, Application Insights, Machine Learning Workspace |
| **PG-NA-External-Prod-04** | `AZ-RG-CICDFramework-DA-AKS-Agent-Prod-01` | **Shared AKS cluster for the GHA (GitHub Actions) Runner** — CI/CD only |
| **AZ-RG-AIF-AKS-MT-EastUS2-[Prod/NonProd/Dev/QA]**, **AZ-RG-AIF-AKS-MT-12-EastUS2-[Prod/NonProd]**, **AZ-RG-AIF-AKS-DR-08-CentralUS-Prod** | — | **Shared AKS clusters for AI Factory Shared Services applications** — where ChatPG's actual workload pods run |

Important mental correction: the cluster `AZ-RG-CICDFramework-DA-AKS-Agent-Prod-01` is the **GHA runner cluster**, not the cluster where ChatPG pods run. ChatPG's workload runs on the `AZ-RG-AIF-AKS-MT-*` and `…-DR-*` clusters.

### 5.2 The AKS clusters

| Cluster VNet | Role |
|---|---|
| `aks-cicd-da-eastus2-prod` | GHA Runner cluster (CI/CD) |
| `aks-aif-mt-prod-vnet` | AIF Shared Services — main production workload |
| `aks-aif-mt-prod-12-vnet` | AIF Shared Services — production variant |
| `aks-aif-mt-nonprod-vnet` | AIF Shared Services — non-prod |
| `aks-aif-mt-np-12-vnet` | AIF Shared Services — non-prod variant |
| `aks-aif-mt-devqa-vnet` | AIF Shared Services — dev / QA |
| `aks-aif-dr-prod-08-9b5b-vnet` | AIF Shared Services — DR (CentralUS) |

**Network:**
- AKS VNets are on `10.99.0.0/16`.
- Private endpoints subnet is on `10.99.144.0/20`.
- Traffic path: `Private Endpoint → Private Link Service → Load Balancer → AKS Pod (ML & Application Containers)`. HTTPS / L7 end to end.

**Note about cluster shape:** ChatPG does not own a dedicated cluster — it shares the AI Factory Shared Services AKS clusters with other apps (ImagePG, AskPG, InsightsPG, AIAPPS).

### 5.3 The Machine Learning Workspace

`mlwCHATPGPROD` — an Azure Machine Learning Workspace in `AZ-RG-AIP-MLWCHATPGPROD`. The infrastructure diagram labels this:

> "Solution is based on AIF Azure ML Blueprint."
> "Service outside of AIF Azure Workspace blueprint" (on the services container)

Pipeline execution into the ML workspace runs over HTTP / REST and HTTPS / L7. The workspace is fronted by its own private endpoints.

### 5.4 PostgreSQL Flexible Server (psql-pg-chatpgproddb)

Canonical production database. From the ChatPG Assessment page (Confluence 6571458581):

| Setting | Value |
|---|---|
| Server name | `psql-pg-chatpgproddb` |
| Compute | `Standard_E32ds_v4` (32 vCores, 128 GB RAM) |
| Storage | 512 GB P30 (5,000 IOPS) |
| PostgreSQL version | 15 |
| AutoGrow | Enabled |
| Backup retention | 30 days |
| **High Availability** | **DISABLED** |
| **Geo-redundant backup** | **DISABLED** |
| **Entra ID authentication** | **DISABLED** (password-only) |
| **Public network access** | **ENABLED** *per Feb 2026 Confluence — but both infra diagrams (Dec 2023 and April 2025) show Private Endpoints. See Section 9.2.* |
| VNet integration | **NONE per Feb 2026 Confluence — but diagrams show Service Endpoints. See Section 9.2.** |

**DR server:**
- Name: `psql-pg-chatpgproddb-dr`
- Compute: `Standard_E32ds_v4` (same as primary)
- Role: `GeoAsyncReplica`

**Non-production databases:**

| Name | Compute |
|---|---|
| `chatpgdev` | E8ds_v4 (8 vCores) |
| `chatpguat` | E4ds_v4 (4 vCores) |
| `chatpguat-replica` | E4ds_v4 (UAT replica) |

### 5.5 Other PaaS services

| Service | Resource Group | Role |
|---|---|---|
| Cache for Redis | `AZ-RG-AIP-MLWCHATPGPROD` | Caching, Celery broker, agent checkpointer store |
| Blob Storage | `AZ-RG-AIP-MLWCHATPGPROD` | Object storage |
| Key Vault | `AZ-RG-AIP-MLWCHATPGPROD` | Secrets — OpenAI API key, DB connection strings, Storage creds, ACR creds, encryption keys, `chatPG_app_credentials` |
| Container Registry | `AZ-RG-AIP-MLWCHATPGPROD` | Image repository (ACR; also referenced as "CVM Proxy" in the legacy diagram) |
| Application Insights | `AZ-RG-AIP-MLWCHATPGPROD` | Application telemetry |

### 5.6 Multi-region strategy (per the April 2025 Technical Infrastructure Diagram)

- **Primary region:** Azure US East (EastUS2).
- **DR region:** Central US (`AZ-RG-AIF-AKS-DR-08-CentralUS-Prod`).
- The services-container services (`AZ-RG-AIP-MLWCHATPGPROD`) have a matching `-DR` resource group.

Note: the Dec 2023 "Legacy" diagram showed five regions (US East, France Central, UK South, South Central US, West Europe). The April 2025 diagram supersedes it with a simpler two-region EastUS2 / CentralUS layout. Treat the April 2025 diagram as current.

### 5.7 Network architecture

The current architecture design is:

```
Internet → Application Gateway → Azure APIM
                ↓
        AKS workload VNet (10.99.0.0/16)
                ↓ Private Endpoint (10.99.144.0/20)
        Private Link Service → Load Balancer → AKS Pod (ML & Application Containers)
                ↓ Private Endpoints
        PostgreSQL flex / Redis / Key Vault / Blob / ACR / App Insights (services container subscription)
                ↓ HTTPS, L7
        GenAI Platform / Azure Search / AskPG / SPOCK / Smart Warehouse / DEPOT
```

**WebRTC ports for Microsoft Teams integration:** 443, 3478, 19302, 5004, 16384-32768.

**Protocols:**
- User → AG: HTTPS, WebRTC (Teams conversation streaming)
- AG → APIM → AKS: HTTPS, L7, TCP/UDP for WebRTC
- AKS ↔ PaaS: HTTPS L7, Private Link
- AKS → Spyglass: HTTPS (send logs)
- AKS → App Insights: REST, Parquet
- AKS → GenAI Platform: HTTPS (generate embeddings, register prompts, model execution)
- CICD → ACR, ACR → AKS: HTTPS for source code deployments

---

## 6. Part VI — Integrations ecosystem

### 6.1 GenAI Platform — the model execution backbone

- The actual AI inference layer. ChatPG prepares prompts and calls GenAI Platform for model execution.
- Authentication: **app-to-app** via `chatPG_app_credentials` stored in Key Vault.
- Use cases: embedding generation, prompt registration, chat completions, model execution.
- Interface: HTTPS.
- Sibling apps in the GenAI Platform parent (Confluence page 6571491335): ChatPG (6571458581), ImagePG (6571393082), AskPG (6580928943), InsightsPG (6582468631), AIAPPS (6582468616).

### 6.2 AskPG — knowledge integration with a dual role

AskPG is the enterprise knowledge integration, and it shows up in two different ways:

1. **In the core product (`de-cf-chatpg-core`)** — AskPG is a product-level integration that can enrich regular chat answers with trusted internal knowledge.
2. **In the agent layer (`de-cf-chatpg-agents`)** — AskPG becomes a **tool** inside LangGraph workflows. Agent flows can discover knowledge bases, query AskPG mid-flow, and reason over the results.

This dual role is important: AskPG is not a side dependency; it is a first-class ChatPG capability.

### 6.3 Azure Search — retrieval / RAG

- Used for retrieval and RAG context.
- Likely hosts vector embeddings used for semantic search.
- Invoked before the model call in Pattern B (retrieval-augmented).

### 6.4 SPOCK — structured business data entry point

**Full name:** Structured Processing of Comments Knowledge.
**CI:** `CI005149570`.

SPOCK is a standalone client application used by P&G Site Line Leaders. It connects to ChatPG from the outside — SPOCK is a **consumer** of ChatPG, not a component of it.

**SPOCK → ChatPG integration:** `Execute LLM chat requests from within SPOCK [API/Manual Chat Interface]`. SPOCK calls ChatPG's API to run LLM chat inside SPOCK's own context.

**SPOCK → DEPOT / Smart Warehouse:** Direct DB authentication with username and site code, based on a White List. Retrieves Site Line Data specific to Stops and User Comments.

### 6.5 DEPOT and Smart Warehouse

**DEPOT — Digital Expert Platform Of Technologies**
- CI: `CI003018365`
- Expert-context platform for domain-specific interpretation.
- Contains the Smart Warehouse.

**Smart Warehouse**
- CI: `CI002884484`
- Structured enterprise data store. Source fact views: `GPOS_CD`, `GPOS_CP`, `GPOS_DO`, `GPOS_CM`.
- Accessed directly by SPOCK (whitelisted) and usable by ChatPG for Pattern C (structured business data) answers.

### 6.6 Microsoft Teams integration

- Teams app uses WebRTC for conversation streaming and HTTPS for prompt send.
- Ports 443, 3478, 19302, 5004, 16384-32768 must be reachable.
- Teams auth flows through Entra ID.

### 6.7 ChatPG's own CI number

**`CI004178244`** — ChatPG.

Use this for ServiceNow tickets, CMDB lookups, or whenever another team asks for ChatPG's CI.

---

## 7. Part VII — Observability

ChatPG has **three observability surfaces**, each with a distinct purpose:

### 7.1 Application Insights

- Telemetry: request/response tracing, dependency tracking (calls to GenAI Platform, Azure Search, PostgreSQL, Redis, etc.), performance metrics, errors, exceptions.
- Ingestion format: REST + Parquet.
- Lives in the services-container resource group (`AZ-RG-AIP-MLWCHATPGPROD`).
- This is your first stop for "what does the trace look like for this user's request?"

### 7.2 Spyglass

- Send Logs, Monitoring Insights, Traces — over HTTPS.
- The logs-and-traces sink, distinct from App Insights.
- `.vscode/settings.json` has `humioctl` auto-approved, suggesting Spyglass is backed by Humio / CrowdStrike LogScale.
- This is your first stop for "show me all logs for this session" or "what error signatures appeared in the last hour?"

### 7.3 Grafana / Prometheus (SRE Monitoring Dashboards)

- Per the SRE Monitoring and Observability Dashboards page (Confluence 4462052289): visual interfaces for performance monitoring, real-time metric insights, latency, error rates, resource utilization, KPIs, system behavior tracking.
- Use for trending and alerting rather than single-request debugging.
- Specific dashboard names/URLs are not in the documentation set — request them from the team.

### 7.4 Agent-layer observability

- The agents repo uses **Phoenix / Arize** hooks for agent workflow traces and evaluations.
- Use when debugging deep research flows, HIL decisions, LangGraph state transitions, checkpointer behavior.

### 7.5 Which to reach for

| Symptom | First stop |
|---|---|
| Specific user request failed — need full trace | Application Insights |
| Need to search raw logs by signature | Spyglass (humioctl) |
| Latency / error-rate trend | Grafana dashboards |
| Agent flow misbehaved mid-workflow | Phoenix / Arize |

---

## 8. Part VIII — Deployment discipline

From the Deployment Procedures page (Confluence 4462051968):

### 8.1 Deployment windows

| Rule | Value |
|---|---|
| **Allowed days** | Monday through Thursday only |
| **Blocked** | Friday, Saturday, Sunday (except critical fixes) |
| **Minimum advance notice** | 1 day to Operations |
| **Post-deployment support** | 3 hours minimum coverage |

### 8.2 Deployment requirements

- Test execution complete before approval.
- Product Owner / Decision-maker approval required.
- Release notes documented.
- **Docker image captured for rollback** — a deployment is not considered complete until a rollback image exists.
- Hotfix / rollback decision-maker must be designated *before* deployment starts.

### 8.3 Support team coordination

- At least one contact per functional area required.
- Contact must be available and reachable for the entire 3-hour post-deployment window.

### 8.4 Environment promotion

Per the infra repo overlays: `dev → sandbox → uat → preprod → prod → dr`. Each stage catches different failure modes (config errors, secret wiring, dependency mismatches, routing, scale). Do not skip stages.

### 8.5 GitOps

- Deployments are reconciled by **FluxCD**.
- Git is the source of truth for desired cluster state.
- Manual cluster edits will drift and be overwritten — do not bypass GitOps.

---

## 9. Part IX — Known incidents and open items

This is the SRE memory of ChatPG. Before investigating something new, check whether it is a known issue.

### 9.1 TURING-896 — OpenAI streaming schema change (Nov 2023)

**Incident ID:** TURING-896 (Confluence 4462053377).

**What happened:** OpenAI removed the `usage` parameter from the streaming response for `POST stream=True`. ChatPG's token usage tracking depends on that parameter.

**Discovery lag:** Approximately **2 months** after the change was released. The platform discovered it from a Microsoft notification, **not from internal monitoring** — an important observability gap.

**Impact:**
- Token usage tracking broken for streaming responses.
- `usage` parameter no longer present in response JSON.

**Status:** The workaround status is **unclear** per the review sources. Ask the team before quoting a fix.

**Operational lesson:** ChatPG does not have automated detection for upstream API schema changes. Treat any "tokens suddenly zero / null" symptom as possibly related.

### 9.2 Database network access — unresolved discrepancy

Two pieces of documentation disagree and this is unresolved as of April 2026:

| Source | Date | Claim |
|---|---|---|
| Feb 2026 Confluence assessment | Feb 2026 | "Public Network Access: ENABLED", "VNet Integration: NONE", "No delegated subnet" |
| Dec 2023 "Legacy" infrastructure diagram | Dec 2023 | Private Endpoints + Service Endpoints for PostgreSQL and other PaaS |
| April 2025 Technical Infrastructure Diagram | Apr 2025 | Private Endpoints + Private Link Service + PrivateLink subnet |

Two design artifacts (the Dec 2023 and April 2025 diagrams) agree on a private-link architecture. One assessment (Feb 2026) claims public access. The diagrams are more recent than 2023 but older than the assessment.

**Required action:** Verify live in Azure Portal.

**Verification steps:**
1. Azure Portal → `psql-pg-chatpgproddb` → Networking tab.
2. Check: "Public endpoint" toggle state.
3. Check: "Private endpoints" list — if entries exist, the diagrams are correct.
4. Check: Firewall rules — empty or restrictive means private-link-only.
5. Check: Delegated subnet — if set, VNet integration is present.

**Security implication:** If public access is truly enabled, this is a high-priority remediation. If not, the Feb 2026 assessment needs correction.

### 9.3 High Availability (HA) is disabled

- HA mode on `psql-pg-chatpgproddb` is **DISABLED**.
- Estimated enablement cost: **~$2,850/month** (per the ChatPG Documentation Index review).
- Geo-redundant backup is also **DISABLED**.

**Risk:** A zone-level incident on the primary PostgreSQL means downtime until failover to `psql-pg-chatpgproddb-dr` (GeoAsyncReplica). There is no automatic HA within-zone.

### 9.4 Entra ID authentication on the DB is disabled

The production PostgreSQL uses **password-only** auth. No Entra ID integration. This is a documented gap in the assessment.

### 9.5 Items flagged as NOT CONFIRMED

From `CHATPG_REVIEW_SOURCES.md`, treat these as **not directly sourced from Confluence** — do not state them as facts without verification:

- Specific OpenAI model (gpt-4 vs gpt-3.5-turbo) — not specified in docs.
- pgvector for embeddings — logical assumption, not confirmed.
- LangGraph/LangChain usage confirmed as framework docs in the workspace; specific ReAct agent pattern is standard practice assumption, not documented.
- Fallback LLM strategy — assumed missing, not confirmed.
- Token usage tracking workaround status — unclear.
- Distributed tracing implementation — not documented.
- SLO/SLA targets — not published.
- Conversation volume metrics — not provided.
- Knowledge base size — not documented.
- Deployment frequency details — vague in docs.
- Data retention policy — not documented.
- Row-level security implementation — not documented.
- Cost estimates — calculated from SKU, not actual billing data.
- Performance characteristics — estimated, not measured.
- Permission model details — not documented.
- RAG pipeline implementation details — not documented.
- Request flow details — reconstructed from patterns, not documented.

When a user asks about any of these, **say so explicitly** and suggest the right verification path.

---

## 10. Part X — SRE troubleshooting playbook

### 10.1 The mindset shift

A developer asks "what code does this feature use?". An SRE asks:
- What does this request depend on?
- Where can it fail?
- What changed recently?
- What should healthy behavior look like?
- How do I isolate the failing layer quickly?

**A user-visible problem in ChatPG may come from any layer in the request path, not only from application code.**

### 10.2 The seven-layer diagnosis order

When something is broken, inspect in this order — do not jump ahead:

1. **Authentication and authorization** — is Entra ID / PingFederate / PingID / Authie reachable? Are tokens being rejected?
2. **Entry and routing** — is APIM / Application Gateway / Istio routing correctly? Any path mismatches? Maintenance mode engaged?
3. **AKS runtime health** — pods healthy? Restarts? Readiness/liveness passing? Recent rollout failed?
4. **State and coordination** — PostgreSQL reachable and responsive? Redis reachable? Workflow checkpointers persisting?
5. **Integration dependencies** — AskPG, Azure Search, SPOCK, Smart Warehouse, DEPOT, GenAI Platform — any degraded?
6. **Recent changes** — deployment? Config change? Secret rotation? Routing change? Overlay diff?
7. **Telemetry and logs** — App Insights trace, Spyglass logs, Grafana trends, Phoenix/Arize for agent flows.

### 10.3 Incident patterns by layer

| Symptom | Most likely layer | Where to look first |
|---|---|---|
| Users cannot log in | Auth | Entra ID, PingFederate, PingID, Authie |
| Login works but every request 401s | Backend JWT validation | Authie public key endpoint, Backend logs |
| Login works but chat fails with 5xx | GenAI Platform app auth | Key Vault (`chatPG_app_credentials`), GenAI Platform status |
| Service unreachable / bad gateway | Entry/routing | APIM, Application Gateway, Istio |
| Pod crash-looping | Runtime | AKS events, recent rollout, ConfigMap/Secret changes |
| Missing conversation context | State | PostgreSQL, Redis |
| Deep research flow stuck | Agent runtime | Phoenix/Arize, Redis checkpointer, IPA logs |
| Simple chat works, business-data questions fail | Integrations | SPOCK / Smart Warehouse / DEPOT |
| Chat works, retrieval-heavy answers weak | Integrations | Azure Search, AskPG |
| Responses uniformly slow | Downstream latency | GenAI Platform latency, DB/Redis timing, runtime saturation |
| Token usage field null / missing | Known: TURING-896 signature | Check streaming response handling code |

### 10.4 Common error signatures to remember

- **JWT signature invalid** → Backend's cached public key is stale, or Authie rotated keys.
- **`chatPG_app_credentials` invalid** → Key Vault secret expired, not rotated, or pulled stale by External Secrets.
- **`usage` field null in streaming response** → TURING-896 still biting.
- **External Secrets sync errors** → Key Vault access-policy or RBAC drift.
- **PostgreSQL connection refused** → Check firewall rules; also validate the Section 9.2 private-endpoint discrepancy.
- **Celery tasks stuck** → Redis broker reachability, worker pod health.

### 10.5 Recent-change triage

Before deep debugging, always ask:

- Was there a deployment today? (Check FluxCD reconciliation logs, ACR image tags, Git history on `de-cf-chatpg-*` repos.)
- Was there a config or overlay change? (Git history on `de-cf-chatpg-infra`.)
- Was a secret rotated? (Key Vault audit log.)
- Was a route or maintenance mode toggled? (Istio config.)

"If it worked yesterday and fails today, a recent change is often a strong lead."

---

## 11. Part XI — SRE scope vs Operations scope

From the Engineering and Operations Scope page (Confluence 4311253151). Knowing this boundary prevents an SRE from accidentally owning Ops work (and vice versa).

### 11.1 SRE Engineering responsibilities

- Software engineering (extensions, code modification).
- Data quality checks and technical debt.
- Tests and testing frameworks.
- Supportability design.
- Systems engineering.
- Cost management.
- Security and audit compliance.

### 11.2 Operations Team responsibilities

- ServiceNow ticket handling (Incidents, Bugs).
- Manual operations execution.
- Manual runs and status checks.
- Report generation.
- Release coordination and approval.
- Credentials and secrets rotation.

### 11.3 Boundary rule

If the work is **code, design, or systems engineering** → SRE.
If the work is **ticket handling, manual execution, rotation, or coordination** → Operations.

When in doubt, check the page above or ask before taking on the work.

---

## 12. Reference A — Confluence pages

Base URL: `https://jira-pg-ds.atlassian.net/wiki`. Space ID: `3893985353`. Access format: `/spaces/3893985353/pages/{PAGE_ID}`.

### 12.1 Verified and fetched (9 pages)

| Page | Page ID | Purpose |
|---|---|---|
| ChatPG (Main) | `6571458581` | Primary ChatPG assessment and reference |
| Deployment Procedures | `4462051968` | Windows, requirements, support coordination |
| Deployment Summary | `4462051740` | Summary / overview |
| Schema Change Incident (TURING-896) | `4462053377` | OpenAI streaming `usage` removal |
| Engineering and Operations Scope | `4311253151` | SRE vs Ops responsibility split |
| Operational Procedures | `3611525123` | Adding new retailer, data integration details |
| SRE Monitoring Dashboards | `4462052289` | Dashboard inventory |
| GenAI Platform (Parent) | `6571491335` | Ecosystem parent — ChatPG, ImagePG, AIAPPS, AskPG, InsightsPG |
| Databases Infrastructure | `6569787420` | SRE infra for database apps |

### 12.2 Onboarding landing pages

| Page | URL |
|---|---|
| New Hire's onboarding - AI SRE Operation Body of Knowledge | `/spaces/AAA/pages/5845614708/` |
| Turing Project (space overview) | `/spaces/TURING/overview?homepageId=4197417170` |
| GenAI Platform (TURING space) | `/spaces/TURING/pages/4197351513/GenAI+Platform` |
| AskPG (TURING space) | `/spaces/TURING/pages/4345495562/AskPG` |
| ChatPG (TURING space) | `/spaces/TURING/pages/4354081339/ChatPG` |
| ImagePG (TURING space) | `/spaces/TURING/pages/4400185560/ImagePG` |
| InsightsPG (TURING space) | `/spaces/TURING/pages/5045616664/InsightsPG` |

### 12.3 Mentioned but not fetched

Treat as leads, not sources:
- ChatPG SDDE (`4437412797`)
- Deployment Template - Successful (`4462053531`)
- Deployment Template - Unsuccessful (`4462053565`)
- SDDE General (`4462051523`)
- Handover to Operations (`3893952624`)
- Documentation requirements (`4319477846`)

---

## 13. Reference B — Repositories

| Repo | Owner | Contents |
|---|---|---|
| `de-cf-chatpg-core` | Core product team | React/TS/Nx/Vite/MUI frontend + Python 3.12/FastAPI/Celery/Redis/PostgreSQL backend |
| `de-cf-chatpg-agents` | Agent platform team | Pygentic, IPA, LangGraph, LangChain flows, Redis checkpointers, Phoenix/Arize |
| `de-cf-chatpg-infra` | Infra / platform team | AKS manifests, FluxCD, Kustomize overlays (dev/sandbox/uat/preprod/prod/dr), Istio, Key Vault + External Secrets, ACR |

Source location: GitHub Enterprise Cloud — P&G Organization. Access is granted via the onboarding access-request process (AD groups per environment).

---

## 14. Reference C — P&G configuration item (CI) numbers

| System | CI |
|---|---|
| **ChatPG** | `CI004178244` |
| **SPOCK** (Structured Processing of Comments Knowledge) | `CI005149570` |
| **DEPOT** (Digital Expert Platform Of Technologies) | `CI003018365` |
| **Smart Warehouse** | `CI002884484` |

Sibling applications in the GenAI Platform ecosystem — confirm their CIs separately before use in tickets:

| System | Confluence page ID |
|---|---|
| ChatPG | `6571458581` |
| ImagePG | `6571393082` |
| AIAPPS | `6582468616` |
| AskPG | `6580928943` |
| InsightsPG | `6582468631` |
| GenAI Platform (parent) | `6571491335` |

---

## 15. Reference D — Azure resource names

### 15.1 Subscriptions

- `PG-NA-External-<Prod/NonProd>-08` — services container (DB, Redis, Key Vault, Blob, ACR, ML Workspace, App Insights)
- `PG-NA-External-Prod-04` — GHA Runner AKS
- `AZ-RG-AIF-AKS-MT-EastUS2-[Prod/NonProd/Dev/QA]` — primary shared AKS for AI Factory services
- `AZ-RG-AIF-AKS-MT-12-EastUS2-[Prod/NonProd]` — secondary shared AKS variant
- `AZ-RG-AIF-AKS-DR-08-CentralUS-Prod` — DR region

### 15.2 Resource groups

- `AZ-RG-AIP-MLWCHATPGPROD` — production services container
- `AZ-RG-AIP-MLWCHATPGPROD-DR` — DR services container
- `AZ-RG-CICDFramework-DA-AKS-Agent-Prod-01` — GHA Runner RG

### 15.3 AKS clusters and VNets

- `aks-cicd-da-eastus2-prod` — GHA Runner
- `aks-aif-mt-prod-vnet`, `aks-aif-mt-prod-12-vnet` — prod workload
- `aks-aif-mt-nonprod-vnet`, `aks-aif-mt-np-12-vnet` — non-prod
- `aks-aif-mt-devqa-vnet` — dev / QA
- `aks-aif-dr-prod-08-9b5b-vnet` — DR

### 15.4 Databases and services

- PostgreSQL primary: `psql-pg-chatpgproddb`
- PostgreSQL DR: `psql-pg-chatpgproddb-dr`
- PostgreSQL dev: `chatpgdev`
- PostgreSQL UAT: `chatpguat`
- PostgreSQL UAT replica: `chatpguat-replica`
- Azure ML Workspace: `mlwCHATPGPROD`

### 15.5 AI Factory component IDs

`898489C85FBF12AA`, `684868C360770857` (in AED diagram) / `30F53140632C417A` (in Apr 2025 infra diagram), `1B581B8D65450ECA`. The difference between the two diagrams on the middle ID suggests the component set changed between Dec 2023 and April 2025 — verify current state with the AI Factory team before quoting.

### 15.6 Network ranges

- AKS workload VNets: `10.99.0.0/16`
- Private endpoints subnet: `10.99.144.0/20`

### 15.7 WebRTC ports (Teams integration)

`443, 3478, 19302, 5004, 16384-32768`

---

## 16. Reference E — Key URLs

| Purpose | URL |
|---|---|
| Confluence base | `https://jira-pg-ds.atlassian.net/wiki` |
| GenAI Platform dev MCP | `https://genai-platform-dev.pg.com/stg/mcp/v1/` |
| LeanIX tenant | `https://pg.leanix.net` |
| LeanIX Diagrams module | `https://pg.leanix.net/pg/diagrams` |
| SRE onboarding landing page | `https://jira-pg-ds.atlassian.net/wiki/spaces/AAA/pages/5845614708/New+Hire+s+onboarding+AI+SRE+Operation+Body+of+Knowledge` |
| Turing Project (space home) | `https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/overview?homepageId=4197417170` |

---

## 17. Glossary

| Term | Meaning |
|---|---|
| **AED** | Application Environment Diagram — one of the canonical ChatPG design artifacts |
| **AIF** | AI Factory — P&G's internal AI platform umbrella |
| **AKS** | Azure Kubernetes Service |
| **APIM** | Azure API Management |
| **Authie** | P&G's internal JWT broker service — exchanges auth codes for tokens, looks up user groups, issues JWTs for ChatPG |
| **CI (P&G)** | Configuration Item — P&G's ServiceNow CMDB ID for a system |
| **CI/CD Framework** | The P&G continuous integration / delivery pipeline, running on the GHA Runner AKS |
| **DEPOT** | Digital Expert Platform Of Technologies — expert-context platform (CI003018365) |
| **External Secrets** | Kubernetes operator that pulls secrets from Key Vault into pods |
| **FluxCD** | GitOps reconciliation operator |
| **GenAI Platform** | P&G's shared model-execution platform — the AI inference layer that ChatPG calls |
| **GHA** | GitHub Actions (the runner AKS cluster is dedicated to CI/CD) |
| **GPOS_CD/CP/DO/CM** | Source fact views in the Smart Warehouse |
| **HIL** | Human-in-the-loop — agent workflow pattern that can pause for human review |
| **IPA** | The agents-repo serving/endpoint layer — exposes flows as callable services |
| **Istio** | Service mesh — traffic, routing, ingress |
| **Kustomize** | Kubernetes manifest customization (base + overlays) |
| **LangChain** | Agent/model/tool building blocks |
| **LangGraph** | Stateful workflow orchestration — state/nodes/edges, pause/resume |
| **mlwCHATPGPROD** | The ChatPG Azure Machine Learning Workspace |
| **Pygentic** | P&G's internal enterprise agent framework — sits above LangGraph/LangChain |
| **PingFederate** | P&G's federated identity provider — trusted by Entra ID |
| **PingID MFA** | Multi-factor authentication step between PingFederate and Entra ID |
| **psql-pg-chatpgproddb** | The production PostgreSQL Flexible Server for ChatPG |
| **Pygentic IPA** | The runtime combination that serves agent flows |
| **SAML assertion** | The token format used in the Entra ID ↔ PingFederate federation handshake |
| **SPOCK** | Structured Processing of Comments Knowledge — an app that calls ChatPG (CI005149570) |
| **Spyglass** | P&G's log/trace sink (Humio / CrowdStrike LogScale-based) |
| **TURING-896** | The Nov 2023 OpenAI streaming `usage` parameter incident |

---

## 18. Confidence discipline — verified vs inferred

This skill follows the same discipline as `CHATPG_REVIEW_SOURCES.md`. When answering a user, apply it.

### 18.1 Treat as verified (cite the source)

Facts that are present in:
- A Confluence page listed in Section 12.1 (with its page ID), or
- The canonical ChatPG diagrams (AED Apr 2025, Flow Jul 2025, Technical Infrastructure Apr 2025, SPOCK integration diagram).

When citing, name the source. Example: "per ChatPG Assessment page 6571458581, compute is Standard_E32ds_v4".

### 18.2 Treat as inferred (flag explicitly)

Anything from the "NOT CONFIRMED" list in Section 9.5, and anything outside the verified sources above.

Preface these with language like "not directly confirmed in the docs but consistent with…" or "inferred from patterns — verify with the team".

### 18.3 Treat as actively disputed

The database network access question (Section 9.2). Two diagrams disagree with one assessment. **Always** flag this as needing live Azure Portal verification until the discrepancy is resolved. Never state the current network posture as fact without that verification.

### 18.4 When a user asks something this skill does not cover

Be honest. Say: "that specific detail is not documented in the sources I have — the best places to verify would be [specific Confluence page / specific Azure resource / specific repo / the team]".

Do not guess.

---

**End of skill.** If you have read this top to bottom, you now hold the full ChatPG picture — user personas, three-layer model, three repositories, request lifecycle and four patterns, auth chain, infrastructure, integrations, observability, deployment discipline, known incidents, troubleshooting playbook, scope boundary, and the canonical references.
