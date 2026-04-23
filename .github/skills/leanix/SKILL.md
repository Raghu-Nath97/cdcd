---
name: leanix
description: 'Fetches and analyzes architecture diagrams from the P&G LeanIX tenant (pg.leanix.net) for AIE SRE applications: ChatPG, ImagePG, AskPG, InsightsPG, AIAPPS. Use whenever the user asks to see, fetch, export, or analyze an architecture diagram from LeanIX, or mentions pg.leanix.net, LeanIX, Fact Sheets, or the Diagrams module. Wraps a local Python and Playwright script (leanix_fetch.py) that runs on the user laptop, reuses their browser SSO session because viewer-role users cannot mint API tokens at P&G, and exports diagrams as PNGs for the agent to read. Typical triggers: show me the ChatPG architecture diagram, pull the LeanIX diagrams for ImagePG, fetch the latest architecture diagrams from LeanIX, what does LeanIX say about this app, compare the LeanIX picture with the Confluence page. Do not use for Confluence pages (use mcp-atlassian), Grafana metrics or logs (use spyglass-mcp), or diagrams already committed to the repo.'
---

# LeanIX — Diagram and Fact Sheet Access Skill

This skill is the single source of truth for how the AIE SRE agent interacts with P&G's LeanIX tenant. Read it before answering any LeanIX-related question.

---

## Table of Contents

0. How to use this skill
1. The constraint: why this is a script, not an MCP
2. The script at a glance
3. When to invoke the script
4. How to invoke the script (exact commands)
5. First-run user experience — what the user will see
6. Reading the output
7. Analyzing fetched diagrams
8. Common failure modes and what to tell the user
9. Combining LeanIX data with other sources
10. Extending the script
11. Reference — file layout, URLs, known apps
12. Confidence discipline

---

## 0. How to use this skill

**Trigger this skill whenever** the user asks for anything that would require reading a LeanIX diagram or Fact Sheet:

- "Show me the ChatPG architecture diagram from LeanIX."
- "Pull the latest ImagePG diagrams."
- "What does LeanIX say about AskPG?"
- "Fetch the architecture diagram and compare it with the Confluence page."
- Anything mentioning `pg.leanix.net`, "Fact Sheet", "LeanIX Diagrams".

**Do not** trigger this skill for:
- Confluence page lookups (use `mcp-atlassian` instead).
- Grafana / Spyglass log or metric queries (use `spyglass-mcp`).
- Diagrams already committed to the repo (read them directly with the Read tool).

---

## 1. The constraint: why this is a script, not an MCP

LeanIX at P&G (`https://pg.leanix.net`) is SSO-federated through Entra ID, PingFederate, and PingID MFA — the same auth chain ChatPG uses. AIE SRE users typically have **Viewer** role, which does not allow personal API-token creation. Admin-created Technical User tokens would be the clean path, but they require a LeanIX admin's time.

**Workaround:** a Python + Playwright script that reuses the user's *browser* session. The user logs in once interactively (including MFA); the script saves the session cookies to `state.json`; subsequent runs use those cookies silently until they expire.

**Consequences to remember:**
- The first run of a given day (or after a session expires) will open a visible Chromium window asking the user to complete SSO + MFA.
- The script cannot run unattended. It is invoked on demand.
- The session cookie lives in `state.json` in this folder — treat it like a password. The `.gitignore` in this folder keeps it out of commits.

---

## 2. The script at a glance

File: `.github/skills/leanix/leanix_fetch.py`

**Inputs:** `--app <name>` (required), plus optional `--base-url`, `--workspace`, `--state-file`, `--output-dir`, `--reauth`.

**Behavior:**
1. Launches Chromium via Playwright.
2. If `state.json` is missing or expired, opens a visible browser window so the user can complete SSO + MFA. On success, saves the session.
3. Silently probes the Pathfinder GraphQL endpoint (`/services/pathfinder/v1/graphql`) to look up Fact Sheets matching the app name. GraphQL may be blocked for Viewer-role sessions; script degrades gracefully.
4. Navigates to the Diagrams module (`/<workspace>/diagrams`), searches for the app name, collects links to matching diagram pages.
5. For each matching diagram: opens it, tries a native "Export as PNG" button first, and if no such button is present, takes a full-page screenshot instead.
6. Writes a `manifest.json` with titles, URLs, linked Fact Sheets (if GraphQL worked), and per-diagram notes.

**Outputs:** `output/<app>/diagram_001.png`, `diagram_002.png`, …, plus `output/<app>/manifest.json`.

---

## 3. When to invoke the script

Invoke the script yourself (via `Bash`) when **all three** of the following hold:

1. The user has asked for something that requires looking at LeanIX content.
2. The content is not already in the repo (check `output/<app>/` first — a recent fetch may already cover it).
3. The user is on their own laptop in VS Code, where Chromium can open and they can respond to the MFA prompt. If the session is running in a remote / headless environment without a visible display, ask the user to run the script locally first and share the output folder.

If the user is just *asking about* LeanIX mechanics (e.g. "how does the LeanIX integration work?") — answer from this skill without running the script.

---

## 4. How to invoke the script (exact commands)

Always run from the repo root. The script handles its own working-directory logic.

**Standard fetch:**
```bash
python3 .github/skills/leanix/leanix_fetch.py --app ChatPG
```

**After a password rotation, or if auth gets sticky:**
```bash
python3 .github/skills/leanix/leanix_fetch.py --app ChatPG --reauth
```

**Custom base URL (rare — other LeanIX tenants):**
```bash
python3 .github/skills/leanix/leanix_fetch.py --app ChatPG --base-url https://pg.leanix.net
```

Known apps: `ChatPG`, `ImagePG`, `AskPG`, `InsightsPG`, `AIAPPS`. Other names will produce a warning but the script will still run.

**First-time setup (run once per laptop):**
```bash
pip install -r .github/skills/leanix/requirements.txt
python3 -m playwright install chromium
```

---

## 5. First-run user experience — what the user will see

Tell the user, *before* running the script the first time, exactly what will happen so they are not surprised:

1. A Chromium window will open and navigate to `https://pg.leanix.net`.
2. They will need to complete the normal P&G SSO flow — email, password, PingID MFA push on their phone.
3. Once LeanIX loads (workspace home), the script will detect success and save the session. The window will then close on its own.
4. The script will continue silently and report how many diagrams it fetched.

If the user does not complete login within **three minutes**, the script will abort cleanly with an instruction to re-run. This is intentional — a stuck MFA step should not leave a zombie Chromium process.

On subsequent runs within the same session window (typically hours), no browser appears; everything runs headless.

---

## 6. Reading the output

After a successful run:

```
.github/skills/leanix/output/<app>/
├── manifest.json
├── diagram_001.png
├── diagram_002.png
└── ...
```

**manifest.json** shape:
```json
{
  "app": "ChatPG",
  "base_url": "https://pg.leanix.net",
  "fetched_at": "2026-04-23T14:22:11+00:00",
  "diagram_count": 3,
  "diagrams": [
    {
      "title": "ChatPG — Technical Infrastructure April 2025",
      "diagram_url": "https://pg.leanix.net/pg/diagrams/<uuid>",
      "png_path": ".../output/ChatPG/diagram_001.png",
      "fetched_at": "2026-04-23T14:22:13+00:00",
      "linked_fact_sheets": [
        {"id": "...", "displayName": "ChatPG", "type": "Application"}
      ],
      "notes": ""
    }
  ],
  "graphql_probe": {"worked": true, "status": 200, "fact_sheets": [...]},
  "warnings": []
}
```

Use the manifest to:
- Pick the right diagram by title.
- Know whether a fetched PNG is a native export (clean) or a full-page screenshot (includes LeanIX UI chrome — still readable but less clean).
- See any warnings from the UI-scraping layer.

---

## 7. Analyzing fetched diagrams

To answer a user's question about a diagram:

1. Read the manifest to find the right PNG.
2. Use the `Read` tool on the PNG path — the agent can view the image natively.
3. Combine what you see in the diagram with what's documented in the ChatPG (or sibling-app) skill.
4. When citing, name the source: "per the LeanIX diagram `diagram_001.png` (fetched 2026-04-23) titled 'ChatPG — Technical Infrastructure April 2025'…".
5. Flag conflicts: if the LeanIX diagram disagrees with the ChatPG skill's Section 9.2 (the disputed DB network access), state it explicitly and recommend live Azure Portal verification.

---

## 8. Common failure modes and what to tell the user

| Symptom in output | What happened | What to tell the user |
|---|---|---|
| Script aborts with "ERROR: playwright is not installed" | First-time setup missing | Run the two setup commands in Section 4. |
| "Did not detect a successful LeanIX login within 3 minutes" | MFA not completed in time, or user closed the browser | Re-run the script and finish the SSO flow within 3 minutes. |
| "GraphQL probe not available (status=401/403)" | Viewer session doesn't have GraphQL access | Benign — the UI-scrape path still works. Mention in the answer that Fact Sheet metadata wasn't available this run. |
| "No diagrams matched on the Diagrams page" + a `debug_*.png` file saved | UI selectors didn't match, or the search produced no results | Read the debug screenshot with the Read tool to confirm. If the Diagrams page looks correct but empty → the app name may not tag any diagrams; try a broader search. If the Diagrams page isn't loading → report to the user and check the base URL. |
| `notes: "full-page screenshot (no native PNG export found)"` | The Diagrams UI didn't offer an export button for that diagram | The PNG is still usable; it just includes LeanIX UI chrome. Mention this in the answer when relevant. |
| "Saved session looks stale" followed by re-login prompt | Previous session expired | Normal — let the user complete SSO again. |

When a `debug_<timestamp>.png` file is present, always read it before giving up — it shows exactly what the script saw, and in most cases the fix is obvious (a UI redesign, a permission error, a blank page).

---

## 9. Combining LeanIX data with other sources

LeanIX is **one of four** architecture sources the agent has access to. Use them together, not interchangeably:

| Source | Strength | Typical question |
|---|---|---|
| **LeanIX** (this skill) | Current, tenant-owned, structured (Fact Sheets + relations) | "What's the current architecture of ChatPG?" |
| **Confluence** (via mcp-atlassian) | Narrative, decisions, procedures, incidents | "How was TURING-896 resolved?" |
| **Repo-committed diagrams + docs** (ChatPG skill) | Version-controlled, curated, annotated | "Explain the auth chain" |
| **GitHub source code** (via `github-chatpg` skill) | Ground truth — what is actually running | "Show me the code that validates the JWT" |

Rules of thumb:
- If sources **agree**, cite all three. This is the strongest answer.
- If sources **disagree**, say so. Present each, mark the newer one, and recommend verification. The Section 9.2 DB network-access discrepancy in the ChatPG skill is a live example.
- If the user asks for **"latest"**, prefer LeanIX — it is where architects update the picture.
- If the user asks **"why"**, prefer Confluence and repo docs — LeanIX rarely carries rationale.

---

## 10. Extending the script

The MVP handles diagrams for one app at a time. Likely next extensions (ordered by value):

1. **Fact Sheet detail fetch** — a new `--factsheet <id>` flag that pulls full attributes and relations. Useful for "what does ChatPG depend on?".
2. **Multi-app batch mode** — `--app ChatPG,ImagePG,AskPG` for onboarding day-one bulk fetch.
3. **Scheduled refresh** — wrap the script in the `schedule` skill so a morning job keeps `output/` warm.
4. **MCP wrapper** — once the script is stable, wrap it as a local MCP server so the agent can call individual operations (`search`, `list_diagrams`, `export_diagram`) as tools rather than a CLI.

Do not extend this before the MVP has been validated in real use for at least two different apps. Premature abstraction here will cost more than it saves.

---

## 11. Reference — file layout, URLs, known apps

### 11.1 File layout

```
.github/skills/leanix/
├── SKILL.md              # this file
├── README.md             # human setup guide
├── leanix_fetch.py       # the Playwright script
├── requirements.txt      # pip dependencies
├── .gitignore            # excludes state.json and output/
├── state.json            # saved session (generated; never committed)
└── output/               # fetched diagrams (generated; never committed)
    └── <app>/
        ├── manifest.json
        ├── diagram_001.png
        └── ...
```

### 11.2 URLs

| Purpose | URL |
|---|---|
| LeanIX tenant base | `https://pg.leanix.net` |
| Workspace landing | `https://pg.leanix.net/pg/` |
| Diagrams module | `https://pg.leanix.net/pg/diagrams` |
| Pathfinder GraphQL | `https://pg.leanix.net/services/pathfinder/v1/graphql` |
| OAuth token exchange (unused with session auth) | `https://pg.leanix.net/services/mtm/v1/oauth2/token` |

### 11.3 Known apps

| App | Expected Fact Sheet name | ChatPG skill cross-ref |
|---|---|---|
| ChatPG | `ChatPG` | `.github/skills/chatpg/SKILL.md` |
| ImagePG | `ImagePG` | — (not yet built) |
| AskPG | `AskPG` | — (not yet built) |
| InsightsPG | `InsightsPG` | — (not yet built) |
| AIAPPS | `AIAPPS` | — (not yet built) |

---

## 12. Confidence discipline

This skill follows the same verified / inferred / disputed pattern as the ChatPG skill.

### Treat as verified
- Everything the script reports in `manifest.json` for the current run, with the caveat that a full-page screenshot (vs native export) may include UI chrome.
- Fact Sheet metadata when `graphql_probe.worked == true`.

### Treat as inferred
- Fact Sheet data when the GraphQL probe failed. Use UI-visible text instead and say so.
- The specific Diagrams-module URL path (`/<workspace>/diagrams`) — correct for current LeanIX builds, but could change. If the script reports it could not reach the Diagrams page, verify the URL in a real browser before blaming the script.

### Treat as actively disputed
- **Any diagram that contradicts the ChatPG skill's Section 9.2 DB network-access discrepancy.** Do not silently adopt either source. Flag the conflict and recommend live Azure Portal verification.

### When a user asks something this skill does not cover
Be honest. Say: "the current LeanIX fetch does not cover that — the script is scoped to diagrams-per-app. To answer this, we would need to extend the script per Section 10, or you can open LeanIX directly at `https://pg.leanix.net/pg/`".

---

**End of skill.** For human setup instructions, see `README.md` in this folder. For day-to-day usage, everything you need is above.
