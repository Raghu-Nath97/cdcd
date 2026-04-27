# AIE SRE Onboarding — Day-One Prerequisites

**Read this first.** Every credential the onboarding agent needs is listed here. Create all of them in one sitting, paste each into the VS Code prompt the first time you start an MCP server, and you won't get blocked mid-conversation later.

Estimated time end-to-end: **25–35 minutes** if everything goes smoothly.

---

## What you will create

| # | Credential | Where it goes | Roughly how long |
|---|---|---|---|
| 1 | Confluence username + API token | `mcp-atlassian` MCP server | 3 min |
| 2 | Spyglass Basic-auth key | `spyglass-mcp` MCP server | 2 min |
| 3 | Spyglass APIM subscription key | `spyglass-mcp` MCP server | Ask your lead |
| 4 | LeanIX — *(no token; interactive SSO)* | `leanix_fetch.py` script on first run | 3 min |
| 5 | GitHub fine-grained PAT | `github` MCP server | 5–10 min |

Plus two one-time tool installs:

| Tool | Purpose |
|---|---|
| `uvx` (for `mcp-atlassian`) | See `SKILL.md` → "Setup Onboarding Agent" section |
| `playwright` + Chromium (for LeanIX) | See `.github/skills/leanix/README.md` |
| `github-mcp-server` binary | See section 5 below |

---

## 1. Confluence — API token

**URL:** `https://jira-pg-ds.atlassian.net`

Confluence API tokens are personal and tied to your P&G email. They do not expire unless you revoke them.

1. Open `https://id.atlassian.com/manage-profile/security/api-tokens` while logged in as your P&G account.
2. Click **Create API token**.
3. **Label:** `aie-sre-onboarding-agent`.
4. (Optional) **Expiration:** 1 year is the Atlassian default; shorter is fine.
5. Click **Create** and **Copy** the token — it is shown once.
6. Save it in your password manager.

**Paste into VS Code when prompted:**

- `confluence-username` → your P&G email (e.g., `firstname.lastname@pg.com`)
- `confluence-api-token` → the value you just copied

**Verify it works (optional but nice):**

```bash
curl -u "$YOUR_EMAIL:$YOUR_TOKEN" \
  "https://jira-pg-ds.atlassian.net/wiki/rest/api/content?limit=1" | head -c 200
```

You should see JSON starting with `{"results":[...]}`. A 401 means the token or email is wrong.

---

## 2 & 3. Spyglass — Basic-auth key and subscription key

Spyglass is fronted by P&G's internal APIM instance. It needs **two** secrets:

**Basic-auth key** — you build this yourself from a username and password the AIE SRE team owns. Base64-encode the combined string:

```bash
printf 'user:pass' | base64
```

Replace `user:pass` with the real credentials (ask your AIE SRE lead — these are not your personal credentials; they are the shared service account for Spyglass access).

**Subscription key** — issued by P&G's APIM team. Your AIE SRE lead either has it or can request it from the APIM portal. It is *not* your personal API key.

**Paste into VS Code when prompted:**

- `mcp-spyglass-auth-key` → the base64 output above
- `mcp-spyglass-subscription-key` → the APIM subscription key

**Gotcha:** both are prompted with `password: true` in `mcp.json`, so they won't be visible as you type. Double-check by copying from your password manager, not by typing.

---

## 4. LeanIX — no token, interactive SSO

P&G's LeanIX tenant (`https://pg.leanix.net`) does not let Viewer-role users mint API tokens. Instead the onboarding agent uses a Python + Playwright script that reuses your browser session.

There is **nothing to paste into VS Code** for LeanIX. Instead, on the first run of the script:

1. The script opens a visible Chromium window.
2. You log in with your P&G SSO — email, password, PingID MFA push on your phone.
3. Once LeanIX's workspace home loads, the script saves your session to `state.json` in `.github/skills/leanix/` and closes the browser.
4. Subsequent runs are silent until your SSO session expires (several hours to a day).

Full details and troubleshooting live in [`.github/skills/leanix/README.md`](../leanix/README.md).

**Install first-time:**

```bash
pip install -r .github/skills/leanix/requirements.txt
python3 -m playwright install chromium
```

---

## 5. GitHub — fine-grained Personal Access Token

This is the one with the most steps, because GitHub Enterprise Cloud orgs are SSO-protected. Miss the SSO authorization step and nothing works — every API call returns 403.

### 5.1 Create the token

1. Open `https://github.com/settings/tokens?type=beta` (fine-grained tokens tab).
2. Click **Generate new token**.
3. **Token name:** `aie-sre-onboarding-agent`.
4. **Expiration:** 90 days (or 1 year if your org allows it — shorter is better; rotate when it expires).
5. **Resource owner:** select `procter-gamble` from the dropdown.
6. **Repository access:** choose **Only select repositories**, and add exactly these three:
   - `de-cf-chatpg-core`
   - `de-cf-chatpg-agents`
   - `de-cf-chatpg-infra`
7. **Repository permissions** — set each of these to **Read-only**, leave everything else as **No access**:

   | Permission | Level |
   |---|---|
   | Contents | Read |
   | Metadata | Read *(mandatory; auto-selected)* |
   | Pull requests | Read |
   | Issues | Read |
   | Actions | Read *(for CI status)* |
   | Commit statuses | Read |

8. **Account permissions:** leave all as **No access**.
9. Click **Generate token**, copy the value (`github_pat_…`) immediately into your password manager — it is shown once.

### 5.2 Authorize SSO — **do not skip this step**

Immediately after creating the token:

1. You are returned to the token list.
2. Find your token and click **Configure SSO**.
3. Find the `procter-gamble` org in the SSO list and click **Authorize**.
4. Complete any SAML redirect GitHub sends you through.

Without step 5.2, the token exists but is rejected on every request with `403 Resource not accessible by personal access token`.

### 5.3 Install the MCP server binary

**Homebrew (macOS, cleanest):**

```bash
brew install github-mcp-server
```

**Fallback — direct binary (macOS Apple Silicon):**

```bash
curl -L -o /tmp/gh-mcp.tar.gz \
  https://github.com/github/github-mcp-server/releases/latest/download/github-mcp-server_Darwin_arm64.tar.gz
tar -xzf /tmp/gh-mcp.tar.gz -C /tmp
sudo mv /tmp/github-mcp-server /usr/local/bin/
sudo chmod +x /usr/local/bin/github-mcp-server
```

For Intel Macs, swap `arm64` → `x86_64` in the URL. For Linux, swap `Darwin` → `Linux`. For Windows, download the `Windows_x86_64.zip`, extract `github-mcp-server.exe`, and put it on `PATH`.

**Verify:**

```bash
github-mcp-server --help
```

### 5.4 Sanity-check the token and SSO

```bash
curl -H "Authorization: Bearer $YOUR_PAT" \
     -H "Accept: application/vnd.github+json" \
     https://api.github.com/repos/procter-gamble/de-cf-chatpg-core | head -c 300
```

You should see JSON with `"name": "de-cf-chatpg-core"`. A 401 means the token is wrong. A 403 usually means SSO is not authorized — go back to step 5.2.

### 5.5 Paste into VS Code when prompted

- `github-pat` → the value starting with `github_pat_…`

---

## After everything is pasted — how to start the servers

In VS Code:

1. Open the command palette (`Ctrl+Shift+P` / `Cmd+Shift+P`).
2. Run **MCP: List Servers**.
3. For each of `mcp-atlassian`, `spyglass-mcp`, `github` — click **Start Server**. The first time, VS Code will prompt you for the inputs; paste from your password manager.
4. `genai-platform` is an HTTP endpoint that does not need any prompts.

LeanIX is invoked as a script, not an MCP server — the agent will run it via Bash when needed.

---

## Security hygiene

- All secrets are prompted via VS Code and stored in its secret storage — not in any file in this repo.
- `state.json` (LeanIX) and any `output/` folders are in `.gitignore`. Do not force-commit them.
- If your laptop is lost, stolen, or left unattended in a public place, rotate:
  - The Confluence API token in your Atlassian profile.
  - The GitHub PAT at `https://github.com/settings/tokens`.
  - The Spyglass shared credentials — tell your AIE SRE lead so the whole team rotates together.
  - Log out of LeanIX in your browser — this invalidates the saved `state.json` cookie.

---

## Rotation schedule

| Credential | Recommended rotation |
|---|---|
| Confluence API token | Annually, or on team handover |
| Spyglass keys | Team-managed; follow AIE SRE team's rotation cadence |
| LeanIX session | Automatic — re-login when expired |
| GitHub PAT | Every 90 days if you picked the 90-day expiry; else annually |

The agent will remind you if a server returns 401 — that's usually an expired credential, not a code bug.

---

## Troubleshooting first-run issues

| Symptom | Likely cause | Fix |
|---|---|---|
| MCP server won't start, says "command not found" | Binary not on PATH | Re-run the install for that tool, or check `echo $PATH`. |
| `mcp-atlassian` returns 401 on every call | Username or API token wrong | Re-check the value in VS Code's secret store; regenerate if unsure. |
| `github` MCP returns 403 on every call | SSO not authorized on the PAT | Go to `https://github.com/settings/tokens`, click Configure SSO, authorize `procter-gamble`. |
| `github` MCP returns 401 | PAT wrong or expired | Regenerate per section 5. |
| `spyglass-mcp` returns 401 or 403 | Auth key or subscription key wrong | Re-check both; the subscription key is especially easy to paste with a trailing space. |
| LeanIX script opens Chromium and hangs | MFA push not received | Check your phone for the PingID prompt; re-run if timed out. |

If any of these persist after two attempts, copy the exact error into a chat with the agent — it has the context to help debug.
