# LeanIX Diagram Fetcher — Setup and Usage

A small Python + Playwright utility that fetches architecture diagrams from P&G's LeanIX tenant (`https://pg.leanix.net`) for the AIE SRE Onboarding Agent.

This README is for humans setting up or troubleshooting the tool. For the agent-facing usage spec, see `SKILL.md` in this folder.

---

## Why this tool

Viewer-role LeanIX users at P&G cannot mint API tokens, and the tenant is SSO-federated with PingID MFA, so a traditional API client is not workable. This tool sidesteps the limitation by reusing your *browser* session: you log in once in a Chromium window, the script saves the cookies, and subsequent runs use them silently until the session expires.

---

## One-time setup (per laptop)

1. **Python 3.10+** is required. Check with `python3 --version`.

2. **Install Python dependencies:**
   ```bash
   pip install -r .github/skills/leanix/requirements.txt
   ```

3. **Install the Chromium binary that Playwright controls:**
   ```bash
   python3 -m playwright install chromium
   ```

   This downloads a Chromium build (~150 MB) into Playwright's cache. It does not affect any other browser on your laptop.

4. *(Optional but recommended)* Add `.github/skills/leanix/state.json` and `.github/skills/leanix/output/` to a personal ignore if you are uncertain about your repo's `.gitignore`. The repo-level `.gitignore` in this folder already excludes them.

---

## First run

From the repo root:

```bash
python3 .github/skills/leanix/leanix_fetch.py --app ChatPG
```

What happens:

1. A Chromium window opens and navigates to `https://pg.leanix.net`.
2. Complete the normal P&G SSO flow — email, password, PingID MFA push.
3. Once LeanIX finishes loading the workspace home, the script detects success and closes the window. Your session is saved to `state.json` in this folder.
4. The script then fetches diagrams for the requested app and writes them to `output/ChatPG/`.

You have **three minutes** to complete the SSO + MFA step. If you take longer, the script aborts cleanly and you re-run.

---

## Subsequent runs

Same command — no browser window appears, everything runs headless:

```bash
python3 .github/skills/leanix/leanix_fetch.py --app ImagePG
```

When your session expires (typically several hours to a day, depending on P&G's SSO policy), the script will automatically re-open the visible Chromium window and prompt you to log in again.

---

## Command-line reference

| Flag | Default | Purpose |
|---|---|---|
| `--app` | *(required)* | Application name. Known values: `ChatPG`, `ImagePG`, `AskPG`, `InsightsPG`, `AIAPPS`. Others will warn and proceed. |
| `--base-url` | `https://pg.leanix.net` | LeanIX tenant base URL. |
| `--workspace` | `PGPROD` | Workspace path segment after the host. |
| `--state-file` | `.github/skills/leanix/state.json` | Where to save / load the session. |
| `--output-dir` | `.github/skills/leanix/output` | Root of the output tree. |
| `--reauth` | off | Force re-login even if a session exists. Useful after a password rotation. |

---

## Output

```
.github/skills/leanix/output/ChatPG/
├── manifest.json
├── diagram_001.png
├── diagram_002.png
└── ...
```

`manifest.json` lists each fetched diagram with title, URL, PNG path, fetch timestamp, and any linked Fact Sheets the GraphQL probe returned.

---

## Troubleshooting

**"ERROR: playwright is not installed"**
Run the two setup commands in the One-time setup section.

**"Executable doesn't exist at …/chromium-*/chrome"** (from Playwright)
You ran `pip install` but not `python3 -m playwright install chromium`. Run the second command.

**Chromium opens but you see "This site can't be reached" or a proxy error**
P&G corporate network may require a proxy to reach `pg.leanix.net`. Playwright respects `HTTPS_PROXY` / `HTTP_PROXY` env vars; set them before running:

```bash
export HTTPS_PROXY=http://<corp-proxy>:<port>
export HTTP_PROXY=http://<corp-proxy>:<port>
python3 .github/skills/leanix/leanix_fetch.py --app ChatPG
```

**"Did not detect a successful LeanIX login within 3 minutes"**
You need to finish SSO + MFA faster, or the MFA push got lost. Re-run and keep your phone handy.

**"No diagrams matched on the Diagrams page"** plus a `debug_*.png` file
Open the debug screenshot. If you can see the Diagrams page and it looks normal, the app name simply isn't tagged to any diagrams — try a variant (`ChatPG` vs `Chat PG`). If the page is an error / permission denied, your account likely doesn't have read access to the Diagrams module; ask a LeanIX admin.

**Session stops working mid-day**
Run with `--reauth`:
```bash
python3 .github/skills/leanix/leanix_fetch.py --app ChatPG --reauth
```

**"Chromium exits immediately with no window visible"** (macOS)
If you installed Playwright in a Python virtualenv and run from a shell without the right DISPLAY settings, GUI apps may fail silently. Try running from a plain Terminal.app session, not from inside tmux or a remote shell.

---

## What the script does NOT do (by design)

- **Does not** store your LeanIX password. Only session cookies.
- **Does not** run unattended. MFA must be completed by a human.
- **Does not** modify any LeanIX data. Read-only.
- **Does not** retry forever. Fails fast with clear messages.

---

## Security notes

- `state.json` contains your LeanIX session cookie. Treat it like a password. The repo-level `.gitignore` keeps it out of commits — do not override that.
- If your laptop is shared, delete `state.json` when you're done for the day.
- If you believe the session was leaked, log out of LeanIX in your normal browser; that invalidates the saved cookie too.

---

## Extending the script

See Section 10 of `SKILL.md` for the planned extension path.
