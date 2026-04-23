---
name: github-chatpg
description: 'Code-level access to the three ChatPG repos on GitHub Enterprise Cloud (procter-gamble org): de-cf-chatpg-core (React/TS frontend plus Python/FastAPI backend), de-cf-chatpg-agents (Pygentic, IPA, LangGraph flows), de-cf-chatpg-infra (AKS, FluxCD, Kustomize, Istio). Use whenever the user asks to read, search, or explain ChatPG code: find a function, locate a FastAPI route, check a Kustomize overlay, look at a recent commit or PR, see JWT validation code, find a LangGraph flow. Teaches the agent where to look in each repo and which query patterns work. Trigger on: show me the code for, find the function, where is this defined, show the LangGraph flow, which Kustomize overlay, recent commits on, open PRs for ChatPG, CI status, what is in the Flux config. Also on direct mentions of the three repos by name. Do not use for Confluence narrative (use mcp-atlassian), LeanIX diagrams (use leanix skill), or runtime logs and metrics (use spyglass-mcp).'
---

# github-chatpg — Code-Level Access Skill

Teaches the agent how to use the `github` MCP server to answer code-level questions about the three ChatPG repositories. This skill is the code companion to the `chatpg` skill (concepts, architecture) and the `leanix` skill (diagrams).

---

## Table of Contents

0. How to use this skill
1. The three repositories at a glance
2. Tools the GitHub MCP exposes (and when to use each)
3. The three repos — what is in each, where to look, how to query
4. Cross-repo query recipes
5. How to answer typical questions
6. Common failure modes
7. Scope discipline — what this skill does NOT cover
8. Confidence discipline

---

## 0. How to use this skill

**Trigger this skill when** the user asks a code-level question about ChatPG that requires reading real source, not a concept summary. Typical shapes:

- "Show me the code for the JWT validation."
- "Where is the retrieval classifier in the backend?"
- "What does the deep research LangGraph flow look like?"
- "Which Kustomize overlay sets the PostgreSQL connection string?"
- "Show me recent commits on `de-cf-chatpg-agents`."
- "Are there any open PRs touching the auth chain?"

**Do not trigger this skill for:**

- "Explain how JWT validation works in ChatPG." → use the `chatpg` skill first; only call GitHub if the user then asks for *the code*.
- "Show me the architecture diagram." → use `leanix`.
- "What incidents hit ChatPG in April?" → use `mcp-atlassian` (Confluence / Jira).
- "Show me recent errors in ChatPG prod." → use `spyglass-mcp`.

The ordering matters: concepts → code. The agent should read the `chatpg` skill's relevant section first so the code lookup is targeted, not exploratory.

---

## 1. The three repositories at a glance

All three live under the `procter-gamble` organization on GitHub Enterprise Cloud. PAT access must be authorized for SSO (see `.github/skills/aie-sre-onboarding/PREREQUISITES.md` section 5).

| Repo | Layer | Languages | What it owns |
|---|---|---|---|
| `procter-gamble/de-cf-chatpg-core` | Product | TypeScript, Python 3.12 | Frontend UI, backend APIs, session/persistence, business logic, Teams packaging |
| `procter-gamble/de-cf-chatpg-agents` | Agent Runtime | Python 3.12 | LangGraph flows, IPA endpoints, Pygentic agent definitions, deep-research / HIL flows |
| `procter-gamble/de-cf-chatpg-infra` | Deployment | YAML, possibly Helm | AKS manifests, FluxCD GitOps, Kustomize overlays, Istio routing, External Secrets |

Memorize: **core is product, agents is flows, infra is deploy.**

---

## 2. Tools the GitHub MCP exposes (and when to use each)

The official `github-mcp-server` with the toolsets configured in `mcp.json` (`context,repos,issues,pull_requests,actions`) provides these tools. Use the right one — a targeted tool is faster than listing-and-scanning.

| Tool | When to use |
|---|---|
| `get_file_contents` | You already know the path. Fetch one file. |
| `search_code` | You don't know the path. Search by string or regex across one repo. |
| `list_commits` | "What changed recently?" — scoped to a repo or path. |
| `get_commit` | Full diff and metadata for one commit. |
| `list_pull_requests` | Open / recently-closed PRs. |
| `get_pull_request` / `list_pull_request_files` | Dive into one PR's diff. |
| `list_issues` / `get_issue` | Bug / task tracking. |
| `list_workflow_runs` | CI status — is the latest build green? |
| `get_workflow_run_logs` | Failing CI — pull the logs. |

**Rule of thumb:**

- Direct file lookup known by path → `get_file_contents`.
- Search for a symbol or string → `search_code` with a specific term.
- "What's the latest state of…" → `list_commits` first, then `get_commit` on the head.
- "What's in flight" → `list_pull_requests` with `state: "open"`.
- CI / release health → `list_workflow_runs`.

---

## 3. The three repos — what is in each, where to look, how to query

**Important caveat:** the file paths below are the *likely* shape based on the frameworks each repo uses (Nx monorepo, FastAPI, LangGraph, Kustomize) and the ChatPG concept documentation. They are **not verified** — when you first look at a repo, the first thing to do is `get_file_contents` on its `README.md` to confirm the layout. If it differs, update this skill by opening a PR.

### 3.1 `de-cf-chatpg-core`

**Stack:** React + TypeScript + Nx + Vite + MUI frontend; Python 3.12 + FastAPI + Celery + Redis + PostgreSQL backend.

**First files to read:**

- `README.md` — start here.
- `apps/*/` or `frontend/` — frontend app (Nx layout usually nests apps here).
- `packages/*` or `libs/*` — shared frontend libs.
- `backend/` or `services/api/` — FastAPI app.
- `pyproject.toml` or `requirements*.txt` — Python dependency surface.
- `.github/workflows/*.yml` — CI.

**Where key concepts likely live (backend):**

| Concept | Likely location patterns |
|---|---|
| FastAPI app entry | `main.py`, `app.py`, `api/main.py`, `src/**/main.py` |
| Route definitions | `api/routes/*.py`, `routers/*.py` |
| Request classification (direct / retrieval / structured / agentic) | `classifier.py`, `router.py`, search `search_code` for `"classify"` or `"pattern"` |
| JWT validation (from `chatpg` skill section 4) | search for `get_public_key`, `check_access`, `validate_jwt`, `Authie` |
| GenAI Platform client | search for `GENAI_PLATFORM`, `genai_platform`, `chatPG_app_credentials` |
| PostgreSQL models | `models/*.py`, `db/models.py`, SQLAlchemy declarations |
| Celery tasks | `tasks/*.py`, `celery_app.py`, `@celery_app.task` decorators |
| Integration clients (SPOCK, Smart Warehouse, DEPOT, AskPG) | `integrations/*`, `clients/*` |
| Azure Search client | `search/*`, `azure_search*`, `index_client` |

**Where key concepts likely live (frontend):**

| Concept | Likely location patterns |
|---|---|
| App shell / routing | `apps/web/src/App.tsx`, `router.tsx` |
| Chat screen | `chat/`, `conversation/`, `messages/` component folders |
| API client | `api.ts`, `client.ts`, `useApi.ts` |
| Auth handling | `auth/`, `AuthContext.tsx`, `useAuth.ts` |
| Teams packaging | `teams/`, `manifest.json` |

**Good first queries:**

```
search_code  repo=procter-gamble/de-cf-chatpg-core  query="FastAPI" language="python"
search_code  repo=procter-gamble/de-cf-chatpg-core  query="get_public_key"
get_file_contents  repo=procter-gamble/de-cf-chatpg-core  path="README.md"
list_commits  repo=procter-gamble/de-cf-chatpg-core  per_page=10
```

### 3.2 `de-cf-chatpg-agents`

**Stack:** Pygentic (P&G's agent framework) + IPA (serving layer) + LangGraph + LangChain, with Redis checkpointers and Phoenix/Arize observability.

**First files to read:**

- `README.md`.
- `pyproject.toml` — confirms which Pygentic / LangGraph / LangChain versions.
- `flows/` or `graphs/` or `agents/` — one folder per flow.
- `ipa/` or `serving/` — endpoint definitions.

**Where key concepts likely live:**

| Concept | Likely location patterns |
|---|---|
| General chat agent | `flows/chat/`, `agents/chat_agent.py` |
| AskPG agent flow | `flows/askpg/`, `askpg_agent.py` |
| Deep research flow | `flows/deep_research/`, `deep_research.py`, search for `"detect_intent"` / `"reflect"` |
| Human-in-the-loop flow | `flows/hil/`, search for `"interrupt"`, `"HIL"` |
| Supervisor / swarm / prompt chaining | `patterns/`, `orchestration/` |
| LangGraph graph definitions | search for `StateGraph`, `add_node`, `add_edge` |
| Tool definitions | `tools/*.py`, search for `@tool` decorator |
| Redis checkpointer wiring | search for `RedisSaver`, `checkpointer` |
| Phoenix/Arize hooks | search for `"phoenix"`, `"arize"`, `"trace"` |
| IPA endpoints | search for `"IPAEndpoint"`, `"IPAApp"`, or the Pygentic serving decorator |

**Good first queries:**

```
search_code  repo=procter-gamble/de-cf-chatpg-agents  query="StateGraph" language="python"
search_code  repo=procter-gamble/de-cf-chatpg-agents  query="deep_research"
get_file_contents  repo=procter-gamble/de-cf-chatpg-agents  path="README.md"
```

### 3.3 `de-cf-chatpg-infra`

**Stack:** AKS, FluxCD, Kustomize (base + overlays), Istio, External Secrets with Key Vault, ACR.

**First files to read:**

- `README.md`.
- `kustomize/base/` or `base/` — base manifests shared across envs.
- `kustomize/overlays/{dev,sandbox,uat,preprod,prod,dr}/` — per-environment diffs.
- `flux/` or `fluxcd/` — Flux HelmRelease / Kustomization resources.
- `istio/` — VirtualService, DestinationRule, Gateway.
- `secrets/` or `external-secrets/` — External Secrets resources referencing Key Vault.

**Where key concepts likely live:**

| Concept | Likely location patterns |
|---|---|
| Deployment (Core backend) | `base/deployment-core-backend.yaml` or similar |
| Deployment (Core frontend) | `base/deployment-core-frontend.yaml` |
| Deployment (Agents runtime) | `base/deployment-agents.yaml` |
| ConfigMaps | `base/configmap-*.yaml` |
| Secrets | NOT in Git — look at `externalsecret-*.yaml` and trace back to Key Vault by secret name |
| Ingress / Virtual Services | `istio/virtualservice-*.yaml` |
| Environment-specific overrides | `overlays/<env>/kustomization.yaml` and its patched resources |
| FluxCD reconciliation | `flux/kustomization.yaml`, `flux/helmrelease-*.yaml` |
| Image tags (rollback reference) | per-environment `overlays/<env>/images.yaml` or in the kustomization |
| Maintenance mode switch | Istio `VirtualService` with a `match` on a custom header, or a dedicated `maintenance-mode.yaml` |

**Good first queries:**

```
get_file_contents  repo=procter-gamble/de-cf-chatpg-infra  path="README.md"
search_code  repo=procter-gamble/de-cf-chatpg-infra  query="externalsecret"
search_code  repo=procter-gamble/de-cf-chatpg-infra  query="psql-pg-chatpgproddb"
list_commits  repo=procter-gamble/de-cf-chatpg-infra  path="overlays/prod" per_page=20
```

---

## 4. Cross-repo query recipes

Common SRE questions span all three repos. Here are the patterns.

### 4.1 "What changed that might explain this incident?"

```
list_commits  repo=procter-gamble/de-cf-chatpg-core   since=<T-24h>
list_commits  repo=procter-gamble/de-cf-chatpg-agents since=<T-24h>
list_commits  repo=procter-gamble/de-cf-chatpg-infra  since=<T-24h>
```

Then scan titles and decide which repo to dive into with `get_commit`. Pair this with the `chatpg` skill's section 10.5 "Recent-change triage".

### 4.2 "Show the full story of a PR — infra + backend together"

```
list_pull_requests  repo=procter-gamble/de-cf-chatpg-core  state=open
list_pull_requests  repo=procter-gamble/de-cf-chatpg-agents state=open
list_pull_requests  repo=procter-gamble/de-cf-chatpg-infra  state=open
```

Then for each interesting PR: `get_pull_request` + `list_pull_request_files`.

### 4.3 "Is the latest build green?"

```
list_workflow_runs  repo=procter-gamble/de-cf-chatpg-core   branch=main  per_page=5
list_workflow_runs  repo=procter-gamble/de-cf-chatpg-agents branch=main  per_page=5
list_workflow_runs  repo=procter-gamble/de-cf-chatpg-infra  branch=main  per_page=5
```

If any show `conclusion: failure`, pull its `get_workflow_run_logs`.

### 4.4 "Trace a secret from code to Key Vault"

1. In `de-cf-chatpg-core`, `search_code` for the secret's env-var name (e.g., `CHATPG_APP_CREDENTIALS`).
2. In `de-cf-chatpg-infra`, `search_code` for the same env-var name — it will be in a ConfigMap or a secretRef.
3. If it's a `secretRef`, `search_code` for the secret name in `externalsecret-*.yaml` to find the Key Vault key name.
4. Verify live in Azure Portal → Key Vault.

### 4.5 "Find the authentication code from the chatpg skill's section 4"

The chatpg skill's auth chain is conceptual; the code lives in core:

```
search_code  repo=procter-gamble/de-cf-chatpg-core  query="Authie"
search_code  repo=procter-gamble/de-cf-chatpg-core  query="check_access"
search_code  repo=procter-gamble/de-cf-chatpg-core  query="get_public_key"
```

---

## 5. How to answer typical questions

### 5.1 "Show me the code for X"

1. If you know the file path from the chatpg skill → `get_file_contents`.
2. If you don't → `search_code` with a narrow query term first. If too many results, narrow the query (add `language:python`, specific identifier, etc.).
3. Quote the relevant function or class, not the whole file, unless the user asked for it verbatim.
4. Cite the source: `procter-gamble/de-cf-chatpg-core:<path>@<branch-or-sha>`.

### 5.2 "What is the current state of X?"

1. `list_commits` scoped to the relevant path, limit 5–10.
2. `get_commit` on the most recent.
3. State: "As of commit `<sha>` on `<branch>` (`<date>`), X is defined as…".

### 5.3 "What's in flight?"

1. `list_pull_requests` with `state: "open"`.
2. For each: `get_pull_request` for title, author, merge readiness; `list_pull_request_files` for scope.
3. Summarize: "N open PRs across the three repos; the most relevant to your question are…".

### 5.4 "Compare the code against what the chatpg skill says"

1. Pull the relevant code.
2. Compare the behavior you see in code to the conceptual description in the `chatpg` skill's corresponding section.
3. If they agree, cite both and note the agreement.
4. If they disagree, flag it explicitly — the skill may be stale, or the code may have drifted from the design intent. Recommend updating the skill.

---

## 6. Common failure modes

| Symptom | Likely cause | What to do |
|---|---|---|
| Every tool call returns 403 | SSO not authorized on the PAT | Tell the user: visit `https://github.com/settings/tokens` → Configure SSO → authorize `procter-gamble`. See PREREQUISITES.md section 5.2. |
| Every tool call returns 401 | PAT expired or revoked | Rotate per PREREQUISITES.md section 5.1. |
| `search_code` returns zero results when you expect matches | Query too narrow, wrong repo, or the string genuinely isn't there | Broaden the query; check repo name; try `get_file_contents` on the README to see if the layout differs from what's documented here. |
| `get_file_contents` 404 on an expected path | Layout differs from this skill's map | Read the README first; update this skill once the real layout is known. |
| Rate limit errors (`X-RateLimit-Remaining: 0`) | Too many calls in a short window | Batch queries; use `search_code` once instead of ten `get_file_contents` calls; wait a few minutes. |

---

## 7. Scope discipline — what this skill does NOT cover

- **Writing code.** The PAT is read-only on purpose. Do not attempt PR creation, branch pushes, or file edits from the agent.
- **Secrets.** Secrets live in Azure Key Vault, referenced from `de-cf-chatpg-infra` via `ExternalSecret`. The agent can see the *reference name*; the value is not in Git and must be read in Azure Portal.
- **Other ChatPG-ecosystem repos** (ImagePG, AskPG, InsightsPG, AIAPPS). The PAT is scoped to ChatPG only; when Phase 5 adds sibling-app skills, they will need their own PAT scope or a broader token.
- **Non-GitHub sources.** Jenkins, Azure DevOps, or any non-GitHub pipeline — not covered by the GitHub MCP.

---

## 8. Confidence discipline

### Treat as verified

Anything directly fetched via the GitHub MCP in the current conversation: file contents, commit metadata, PR diffs. Cite with repo + path + commit sha.

### Treat as inferred

The likely file paths in Section 3. They are based on framework conventions and the `chatpg` skill's description, not a direct repo read. When you first open a repo, verify against its README and adjust.

### Treat as actively disputed

Any code finding that disagrees with the `chatpg` skill. Do not silently adopt either source:
- Flag the conflict.
- State what the code shows and what the skill says.
- Recommend an update to whichever is stale.

### When this skill does not cover something

Be honest. Say: "the repos may have that, but I don't have a documented path for it — let me `search_code` for `<term>` and see what comes back".

---

**End of skill.** Pair with the `chatpg` skill for concepts, the `leanix` skill for diagrams, and `mcp-atlassian` for narrative context.
