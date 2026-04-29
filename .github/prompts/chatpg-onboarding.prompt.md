---
description: 'ChatPG onboarding overview — invoke with /chatpg-onboarding when a new AIE SRE asks "what is ChatPG", "explain ChatPG", "how does ChatPG work", or "how is ChatPG managed". Produces a concise 7-section briefing with clean ASCII flow diagrams generated from the markdown analyses of the LeanIX-exported architecture diagrams.'
mode: 'agent'
tools: ['editFiles', 'search', 'codebase']
---

# ChatPG Onboarding Briefing

You are giving a **single, focused onboarding briefing** on ChatPG to a new AIE SRE. Your job is to **read the authoritative source material yourself**, then synthesize a tight overview. Do **not** answer from memory of ChatPG.

---

## Step 1 — Read the source material (mandatory, in this order)

The source of truth for ChatPG architecture is a set of **markdown analysis files** in `.github/skills/aie-sre-onboarding/Docs/ChatPG/`. Each `.md` file is a structured text description of a LeanIX-exported drawio diagram (the matching `.drawio.png` lives alongside it for human reference). The `.md` files exist precisely so this prompt works on any model — vision-capable or text-only.

Before writing a single word of the response, do all of the following:

1. **Read the onboarding skill** at `.github/skills/aie-sre-onboarding/SKILL.md` (canonical Confluence/Jira links and team context).
2. **List the diagrams folder** with `list_dir` on `.github/skills/aie-sre-onboarding/Docs/ChatPG/` and **read every `.md` file** you find with `read_file`. Expected files (names may vary):
   - `ChatPG - AED.md` — Application Environment Diagram (what ChatPG depends on, integrations)
   - `ChatPG - TID.md` — Technical Infrastructure Diagram (subscriptions, resource groups, AKS, networking, identity flow)
   - `ChatPG - Communication Flow Diagram.md` — request flow between components
3. *(Optional, only if the user asked something time-sensitive)* Use `mcp_com_atlassian_getConfluencePage` on the ChatPG Confluence page (ID from the onboarding skill) to confirm narrative facts. Skip if MCP is not configured.

If a specific `.md` file is missing, say so explicitly and only build the diagram(s) for which you have source material — do not invent components for the missing one.

### If the `.md` analysis files are missing entirely

This prompt **requires** the markdown analyses. Do **not** fall back to memory or to drawing diagrams from generic ChatPG knowledge. If `Docs/ChatPG/` contains only `.drawio.png` files and no `.md` files, stop and tell the user:

> *"This prompt needs markdown analyses of the ChatPG diagrams in `.github/skills/aie-sre-onboarding/Docs/ChatPG/`. The folder currently has only the `.drawio.png` exports and no `.md` files. Generate a `.md` analysis for each diagram (component list + connection list) and re-run `/chatpg-onboarding`."*

Do not produce a partial briefing. Refuse cleanly.

---

## Step 2 — Produce the briefing in this exact structure

### 1. What ChatPG is — one short paragraph

3–5 sentences explaining what ChatPG is, who uses it, and why it is more than an LLM wrapper. Ground every claim in the AED `.md` or the onboarding skill.

### 2. The three-layer mental model

Short table mapping the three layers (Core Product / Agent Runtime / Cloud Infrastructure) to their repos (`de-cf-chatpg-core`, `de-cf-chatpg-agents`, `de-cf-chatpg-infra`) with a one-line responsibility each. If the AED `.md` uses different layer names, use those.

### 3. Request flow — generate one ASCII diagram from the Communication Flow `.md`

Render a single, clean ASCII diagram (no Mermaid) in a fenced ` ```text ` block, sourced from `ChatPG - Communication Flow Diagram.md`. Use Unicode box-drawing characters (`┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼ ▶ ◀ ▲ ▼`).

**Layout rules for clarity:**
- Lay the main happy path **left-to-right** in one straight horizontal line. Avoid winding the main flow up and down.
- Branch side-systems (auth providers, MFA, directory lookups) **off the main line as short stubs** — above for one group, below for another — so the eye can follow the request without crossing arrows.
- Keep all boxes the same height. Pad labels with one space inside each box.
- Use `──▶` for one-way calls and `◀──▶` for round-trips. Do **not** mix arrow styles within one diagram.
- No crossing lines. If two arrows would cross, restructure the layout instead of drawing through.
- Group related sub-systems (e.g. `Authle / EntraID / Ping Federate / PingID MFA / MSTF AD`) in a **clearly labeled cluster** rather than as 5 free-floating boxes.
- Add a one-line caption under the diagram naming the source: `Source: ChatPG - Communication Flow Diagram.md`.

Use the **exact component labels from the `.md`** (e.g. if the `.md` says "PingFederate Prod Instance", write that — not "PingFed").

### 4. How it is built — short bullets only

Stack summary by layer (frontend / backend / agent runtime / infra). Source from the onboarding skill and any stack-relevant facts in the AED/TID `.md`. ~6 bullets total.

### 5. How it is managed — generate one ASCII diagram from the TID `.md`

Render a single, clean ASCII diagram (no Mermaid) in a fenced ` ```text ` block, sourced from `ChatPG - TID.md`. Focus on the **deploy + operations** picture: subscriptions, resource groups, AKS clusters, networking, monitoring — whatever the TID `.md` describes.

**Layout rules for clarity:**
- Group components by **subscription** using clearly labeled outer boxes (one box per subscription). The subscription name and resource-group names go on the top border of each box.
- Inside each subscription box, lay components vertically in logical groups (Services Container / Network / AKS / etc.) with a blank line between groups.
- Draw cross-subscription connections as arrows **between the subscription boxes**, with a short edge label naming the protocol (e.g. `HTTPS, L7` or `HTTP, REST`).
- Put external systems (Spyglass, GenAI Platform, PingFederate, Entra ID, Microsoft Teams, Application Insights) in a **separate "External" cluster at the bottom** with arrows back into the relevant subscription boxes.
- No crossing lines. Same arrow-style consistency rule as section 3.
- Add a one-line caption: `Source: ChatPG - TID.md`.

Below the diagram, add 3–4 bullet facts about how releases ship, where secrets live, what is monitored, and where incidents are tracked. Source from the TID `.md` and the onboarding skill.

### 6. Where to go next — one small links table

5–6 rows: Confluence section, the three GitHub repo URLs, the local diagrams folder (`.github/skills/aie-sre-onboarding/Docs/ChatPG/`), Jira location for incidents. Take URLs from the onboarding skill — do not invent URLs.

### 7. Reference material on disk

List the `.md` analysis files you used (full paths under `.github/skills/aie-sre-onboarding/Docs/ChatPG/`) so the user can open the source material.

---

## Step 3 — Hard rules

1. **Never skip Step 1.** Every diagram you draw must come from a `.md` analysis file you actually read in this turn. If the `.md` files are missing, refuse as documented in Step 1 — do not silently guess.
2. **ASCII only — no Mermaid, no PlantUML, no other diagram syntaxes.** Sections 3 and 5 must each contain exactly one ASCII box diagram in a ` ```text ` fenced block. The ASCII version is the only diagram — it must be clean enough to stand on its own.
3. **Do not invent specifics** — no incident IDs, no Azure resource IDs, no CI numbers, no code paths, unless they appear in the source `.md` files or the onboarding skill. If asked about something not covered: *"I don't have that in the onboarding overview — check the ChatPG Confluence page or the relevant repo."*
4. **Use exact labels from the source `.md`** in your diagrams. If the source says `mlwCHATPGPROD`, write that — not "ML Workspace".
5. **End with one focused follow-up offer**, e.g. *"Want me to go deeper on the auth chain, the agent runtime, or the deploy pipeline?"* — not a 6-item menu.
6. **Length cap: ~180 lines total** including the two ASCII diagrams. If you go over, cut prose, never the diagrams.
7. **Do not load the `github-chatpg` or `leanix` skills for this overview.** Those are for code-level questions and live LeanIX fetches respectively. This briefing is grounded in the local `.md` analyses and the onboarding skill — that's it.
