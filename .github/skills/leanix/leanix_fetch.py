#!/usr/bin/env python3
"""
leanix_fetch.py
===============

Fetch architecture diagrams from P&G's LeanIX tenant (https://pg.leanix.net) for
a given application (ChatPG, ImagePG, AskPG, InsightsPG, AIAPPS).

Why this script exists
----------------------
AIE SRE users have **Viewer** role and cannot mint API tokens. LeanIX at P&G is
SSO-federated (Entra ID + PingFederate + PingID MFA), so programmatic
username/password login is not available. The workable path is to reuse the
user's browser session: log in once interactively, save the cookies, then reuse
them for subsequent automated fetches.

What it does
------------
1. Launches Chromium via Playwright.
2. On first run (no saved state), opens a *visible* browser window so the user
   can complete SSO + MFA manually. Once the user is landed on LeanIX, the
   script saves the session state to `state.json`.
3. On later runs, reuses `state.json` silently (headless). If the session has
   expired, it falls back to the visible-login flow automatically.
4. Navigates to the LeanIX Diagrams module, searches for diagrams related to
   the requested application, exports each as PNG, and writes a
   `manifest.json` describing what was fetched.
5. Optionally probes the Pathfinder GraphQL endpoint with the session cookie to
   enrich the manifest with Fact Sheet metadata. GraphQL may be blocked for
   Viewer-role sessions; script degrades gracefully if so.

Output layout
-------------
    .github/skills/leanix/
    ├── state.json                 # saved session (gitignored)
    └── output/
        └── <app>/
            ├── manifest.json      # what was fetched + metadata
            ├── diagram_001.png    # one PNG per matching diagram
            ├── diagram_002.png
            └── ...

Usage
-----
    # First run — Chromium opens, user logs in, diagrams fetched
    python leanix_fetch.py --app ChatPG

    # Later — silent, uses saved session
    python leanix_fetch.py --app ImagePG

    # Force re-login (e.g., after rotating password)
    python leanix_fetch.py --app ChatPG --reauth

    # Use a custom LeanIX URL (other tenants, test environments)
    python leanix_fetch.py --app ChatPG --base-url https://pg.leanix.net

Known limitations
-----------------
- The Diagrams-module selectors are based on LeanIX's current UI (~2025). If
  LeanIX ships a UI redesign, the selectors in ``search_diagrams_ui`` will need
  to be updated. When it fails, the script saves a debug screenshot so the fix
  is easy to eyeball.
- Session lifetime depends on P&G's SSO policy — typically several hours to a
  day. When it expires, the next run will prompt for re-login.
- MFA must be completed by a human; this script cannot be scheduled unattended.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from playwright.async_api import (
        BrowserContext,
        Page,
        Playwright,
        TimeoutError as PlaywrightTimeoutError,
        async_playwright,
    )
except ImportError:
    print(
        "ERROR: playwright is not installed.\n"
        "Run:\n"
        "  pip install -r requirements.txt\n"
        "  python -m playwright install chromium\n",
        file=sys.stderr,
    )
    sys.exit(2)


# --- Configuration ---------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_STATE_FILE = SCRIPT_DIR / "state.json"
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "output"
DEFAULT_BASE_URL = "https://pg.leanix.net"
DEFAULT_WORKSPACE = "pg"  # URL path segment after the host after login

# Known P&G GenAI-ecosystem apps. Extend as siblings come online.
KNOWN_APPS = ["ChatPG", "ImagePG", "AskPG", "InsightsPG", "AIAPPS"]

LOGIN_DETECT_TIMEOUT_MS = 180_000   # 3 min to complete SSO + MFA
PAGE_NAV_TIMEOUT_MS = 45_000
SEARCH_WAIT_MS = 5_000


# --- Data classes ----------------------------------------------------------

@dataclass
class DiagramRecord:
    title: str
    diagram_url: str
    png_path: str
    fetched_at: str
    linked_fact_sheets: list[dict[str, str]] = field(default_factory=list)
    notes: str = ""


@dataclass
class Manifest:
    app: str
    base_url: str
    fetched_at: str
    diagram_count: int
    diagrams: list[DiagramRecord]
    graphql_probe: dict[str, Any]
    warnings: list[str] = field(default_factory=list)


# --- Logging helpers -------------------------------------------------------

def log(msg: str) -> None:
    print(f"[leanix_fetch] {msg}", flush=True)


def warn(msg: str) -> None:
    print(f"[leanix_fetch] WARN: {msg}", file=sys.stderr, flush=True)


def err(msg: str) -> None:
    print(f"[leanix_fetch] ERROR: {msg}", file=sys.stderr, flush=True)


# --- Session handling ------------------------------------------------------

async def new_context(
    pw: Playwright,
    state_file: Path,
    *,
    headful: bool,
) -> BrowserContext:
    """Launch Chromium and build a browser context, loading saved state if present."""
    browser = await pw.chromium.launch(headless=not headful)
    storage_state: str | None = str(state_file) if state_file.exists() else None
    context = await browser.new_context(
        storage_state=storage_state,
        viewport={"width": 1440, "height": 900},
    )
    return context


async def ensure_logged_in(
    pw: Playwright,
    base_url: str,
    state_file: Path,
    *,
    force_reauth: bool,
) -> None:
    """
    Verify we have a working LeanIX session, launching a visible browser for
    manual SSO + MFA if we don't.
    """
    if force_reauth and state_file.exists():
        log(f"--reauth specified; deleting existing {state_file.name}")
        state_file.unlink()

    needs_interactive_login = not state_file.exists()

    if not needs_interactive_login:
        # Validate the saved session by hitting the base URL headlessly.
        log("Validating saved session...")
        context = await new_context(pw, state_file, headful=False)
        page = await context.new_page()
        try:
            await page.goto(base_url, timeout=PAGE_NAV_TIMEOUT_MS)
            # If LeanIX redirected us to the SSO login host, the session is
            # dead and we need to re-auth.
            final_host = _host_of(page.url)
            if "leanix.net" not in final_host:
                warn(f"Saved session looks stale — landed on {page.url}")
                needs_interactive_login = True
        except PlaywrightTimeoutError:
            warn("Timed out validating saved session; will re-auth.")
            needs_interactive_login = True
        finally:
            await context.close()

    if needs_interactive_login:
        log("Opening a visible Chromium window for interactive SSO login.")
        log("Please complete SSO + PingID MFA in the window that just opened.")
        log("The script will save your session once LeanIX loads successfully.")
        context = await new_context(pw, state_file, headful=True)
        page = await context.new_page()
        try:
            await page.goto(base_url, timeout=PAGE_NAV_TIMEOUT_MS)
            # Wait until we land on a LeanIX page (any leanix.net URL is fine).
            try:
                await page.wait_for_url(
                    lambda url: "leanix.net" in _host_of(url),
                    timeout=LOGIN_DETECT_TIMEOUT_MS,
                )
            except PlaywrightTimeoutError:
                err(
                    "Did not detect a successful LeanIX login within the "
                    "allowed window (3 minutes). Close the browser and re-run."
                )
                raise SystemExit(1)
            # Give the app a moment to settle any post-login redirects.
            await page.wait_for_load_state("networkidle", timeout=PAGE_NAV_TIMEOUT_MS)
            await context.storage_state(path=str(state_file))
            log(f"Saved session state to {state_file.name}")
        finally:
            await context.close()


def _host_of(url: str) -> str:
    # Cheap parse to avoid an extra import
    try:
        return url.split("//", 1)[1].split("/", 1)[0]
    except Exception:
        return ""


# --- GraphQL probe (best-effort Fact Sheet enrichment) ---------------------

async def probe_graphql_factsheets(context: BrowserContext, base_url: str, app: str) -> dict[str, Any]:
    """
    Try the Pathfinder GraphQL endpoint with the session cookie. Returns a dict
    describing whether the probe worked and any Fact Sheets found.
    """
    endpoint = f"{base_url}/services/pathfinder/v1/graphql"
    query = {
        "query": """
            query Search($q: String!) {
              allFactSheets(fullTextSearch: $q, first: 20) {
                edges {
                  node {
                    id
                    displayName
                    type
                    description
                  }
                }
              }
            }
        """,
        "variables": {"q": app},
    }
    try:
        response = await context.request.post(
            endpoint,
            data=json.dumps(query),
            headers={"Content-Type": "application/json"},
            timeout=15_000,
        )
        status = response.status
        body_text = await response.text()
        if status != 200:
            return {
                "worked": False,
                "status": status,
                "reason": body_text[:500],
                "fact_sheets": [],
            }
        body = json.loads(body_text)
        edges = (
            body.get("data", {})
            .get("allFactSheets", {})
            .get("edges", [])
            or []
        )
        fact_sheets = [
            {
                "id": edge["node"]["id"],
                "displayName": edge["node"]["displayName"],
                "type": edge["node"]["type"],
                "description": (edge["node"].get("description") or "")[:280],
            }
            for edge in edges
            if edge.get("node")
        ]
        return {"worked": True, "status": 200, "fact_sheets": fact_sheets}
    except Exception as exc:
        return {"worked": False, "status": None, "reason": str(exc), "fact_sheets": []}


# --- Diagram retrieval (UI navigation) -------------------------------------

async def search_diagrams_ui(
    context: BrowserContext,
    base_url: str,
    workspace: str,
    app: str,
    output_dir: Path,
) -> tuple[list[DiagramRecord], list[str]]:
    """
    Navigate the Diagrams module, search for the app, and export each match as
    PNG. Returns (records, warnings).

    This is UI-scraping and is brittle to LeanIX UI changes. On failure, a
    screenshot is saved next to `output_dir` as `debug_<timestamp>.png` so the
    fix is obvious.
    """
    records: list[DiagramRecord] = []
    warnings: list[str] = []
    page = await context.new_page()
    page.set_default_timeout(PAGE_NAV_TIMEOUT_MS)

    diagrams_url = f"{base_url}/{workspace}/diagrams"
    log(f"Navigating to Diagrams module: {diagrams_url}")
    try:
        await page.goto(diagrams_url, wait_until="networkidle")
    except PlaywrightTimeoutError:
        warnings.append(f"Diagrams URL {diagrams_url} did not reach networkidle in time.")
        # Fall back to a lighter wait and continue.
        await page.goto(diagrams_url, wait_until="domcontentloaded")

    # Best-effort search: try common search-input selectors. LeanIX has
    # changed these over time; we try a few and then fall back to typing into
    # whatever looks like a search box.
    search_selectors = [
        'input[type="search"]',
        'input[placeholder*="Search" i]',
        'input[aria-label*="Search" i]',
        '[data-testid*="search" i] input',
    ]
    searched = False
    for selector in search_selectors:
        try:
            loc = page.locator(selector).first
            if await loc.count() > 0 and await loc.is_visible():
                await loc.click()
                await loc.fill(app)
                await page.keyboard.press("Enter")
                searched = True
                log(f"Searched for '{app}' using selector: {selector}")
                break
        except Exception:
            continue

    if not searched:
        warnings.append(
            "Could not find a search input in the Diagrams module. "
            "Continuing — the script will list every diagram visible on the page."
        )

    await page.wait_for_timeout(SEARCH_WAIT_MS)

    # Collect diagram links. LeanIX diagram cards usually render as anchors
    # whose href contains '/diagrams/' and a UUID. Capture distinct hrefs.
    anchors = page.locator('a[href*="/diagrams/"]')
    hrefs: list[str] = []
    titles: list[str] = []
    try:
        anchor_count = await anchors.count()
        for i in range(anchor_count):
            href = await anchors.nth(i).get_attribute("href")
            title = (await anchors.nth(i).inner_text()).strip()
            if href and href not in hrefs and _looks_like_diagram_href(href):
                hrefs.append(href)
                titles.append(title or href)
    except Exception as exc:
        warnings.append(f"Error enumerating diagram cards: {exc}")

    if not hrefs:
        debug_screenshot = output_dir / f"debug_no_results_{_timestamp()}.png"
        debug_screenshot.parent.mkdir(parents=True, exist_ok=True)
        try:
            await page.screenshot(path=str(debug_screenshot), full_page=True)
            warnings.append(
                f"No diagrams matched on the Diagrams page. Saved debug screenshot to "
                f"{debug_screenshot.name} so the DOM state is visible."
            )
        except Exception:
            pass
        await page.close()
        return records, warnings

    log(f"Found {len(hrefs)} candidate diagram link(s) on the page.")

    for index, (href, title) in enumerate(zip(hrefs, titles), start=1):
        full_url = href if href.startswith("http") else f"{base_url}{href}"
        try:
            record = await export_diagram_as_png(
                context=context,
                diagram_url=full_url,
                title=title,
                output_dir=output_dir,
                index=index,
            )
            records.append(record)
        except Exception as exc:
            warnings.append(f"Failed to export diagram {index} ({full_url}): {exc}")

    await page.close()
    return records, warnings


def _looks_like_diagram_href(href: str) -> bool:
    # Filter obvious non-diagram links (menu items, filters, etc.)
    if "/diagrams/" not in href:
        return False
    tail = href.split("/diagrams/", 1)[1]
    # Expect something substantive after /diagrams/
    return len(tail) >= 6


async def export_diagram_as_png(
    context: BrowserContext,
    diagram_url: str,
    title: str,
    output_dir: Path,
    index: int,
) -> DiagramRecord:
    """
    Open the diagram page and capture it as PNG. Prefers a native export if the
    UI exposes one; otherwise falls back to a full-page screenshot.
    """
    page = await context.new_page()
    page.set_default_timeout(PAGE_NAV_TIMEOUT_MS)
    try:
        await page.goto(diagram_url, wait_until="networkidle")
    except PlaywrightTimeoutError:
        await page.goto(diagram_url, wait_until="domcontentloaded")

    # Give canvas-based diagrams a moment to paint.
    await page.wait_for_timeout(3_000)

    # Try clicking a native "Export as PNG" button if one is visible. Selectors
    # kept broad on purpose — LeanIX has used several variants.
    png_download_triggered = False
    export_button_selectors = [
        'button:has-text("Export")',
        'button:has-text("Download")',
        '[aria-label*="Export" i]',
        '[data-testid*="export" i]',
    ]
    for sel in export_button_selectors:
        try:
            btn = page.locator(sel).first
            if await btn.count() > 0 and await btn.is_visible():
                # Wait for a download triggered by the click.
                async with page.expect_download(timeout=15_000) as dl_info:
                    await btn.click()
                    # Some UIs show a second menu; try a PNG option if one appears.
                    try:
                        png_option = page.locator('text=/PNG/i').first
                        if await png_option.count() > 0 and await png_option.is_visible():
                            await png_option.click()
                    except Exception:
                        pass
                download = await dl_info.value
                png_path = output_dir / f"diagram_{index:03d}.png"
                output_dir.mkdir(parents=True, exist_ok=True)
                await download.save_as(str(png_path))
                png_download_triggered = True
                break
        except PlaywrightTimeoutError:
            continue
        except Exception:
            continue

    if not png_download_triggered:
        # Fallback: full-page screenshot. Not as clean as a native export but
        # guarantees we get something visual for the agent to analyze.
        png_path = output_dir / f"diagram_{index:03d}.png"
        output_dir.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(png_path), full_page=True)

    record = DiagramRecord(
        title=title,
        diagram_url=diagram_url,
        png_path=str(png_path),
        fetched_at=_now_iso(),
        notes="" if png_download_triggered else "full-page screenshot (no native PNG export found)",
    )
    await page.close()
    return record


# --- Misc helpers ----------------------------------------------------------

def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# --- Main entry point ------------------------------------------------------

async def run(
    app: str,
    base_url: str,
    workspace: str,
    state_file: Path,
    output_root: Path,
    force_reauth: bool,
) -> int:
    if app not in KNOWN_APPS:
        warn(
            f"'{app}' is not in the known-app list {KNOWN_APPS}. Proceeding anyway, "
            "since LeanIX may have other Fact Sheets. Add it to KNOWN_APPS if this "
            "becomes a regular target."
        )

    async with async_playwright() as pw:
        await ensure_logged_in(pw, base_url, state_file, force_reauth=force_reauth)

        log(f"Fetching diagrams for app='{app}'...")
        context = await new_context(pw, state_file, headful=False)

        try:
            graphql_result = await probe_graphql_factsheets(context, base_url, app)
            if graphql_result.get("worked"):
                log(
                    f"GraphQL probe worked — {len(graphql_result['fact_sheets'])} "
                    "Fact Sheet(s) will be recorded in the manifest."
                )
            else:
                log(
                    "GraphQL probe not available "
                    f"(status={graphql_result.get('status')}). Continuing with UI-only diagram fetch."
                )

            output_dir = output_root / app
            records, warnings = await search_diagrams_ui(
                context, base_url, workspace, app, output_dir
            )
        finally:
            await context.close()

    manifest = Manifest(
        app=app,
        base_url=base_url,
        fetched_at=_now_iso(),
        diagram_count=len(records),
        diagrams=records,
        graphql_probe=graphql_result,
        warnings=warnings,
    )
    output_dir = output_root / app
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    with manifest_path.open("w", encoding="utf-8") as fh:
        json.dump(asdict(manifest), fh, indent=2)

    log(f"Wrote manifest: {manifest_path}")
    log(f"Fetched {len(records)} diagram(s) into {output_dir}")
    if warnings:
        for w in warnings:
            warn(w)

    return 0 if records else 1


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Fetch LeanIX diagrams for a P&G application via interactive SSO.",
    )
    p.add_argument(
        "--app",
        required=True,
        help="Application name (e.g., ChatPG, ImagePG, AskPG, InsightsPG, AIAPPS).",
    )
    p.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"LeanIX base URL (default: {DEFAULT_BASE_URL}).",
    )
    p.add_argument(
        "--workspace",
        default=DEFAULT_WORKSPACE,
        help=f"Workspace path segment (default: {DEFAULT_WORKSPACE}).",
    )
    p.add_argument(
        "--state-file",
        default=str(DEFAULT_STATE_FILE),
        help=f"Path to Playwright storage state (default: {DEFAULT_STATE_FILE}).",
    )
    p.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help=f"Output directory root (default: {DEFAULT_OUTPUT_DIR}).",
    )
    p.add_argument(
        "--reauth",
        action="store_true",
        help="Force re-login even if saved session exists.",
    )
    return p


def main() -> int:
    args = build_arg_parser().parse_args()
    try:
        return asyncio.run(
            run(
                app=args.app,
                base_url=args.base_url.rstrip("/"),
                workspace=args.workspace.strip("/"),
                state_file=Path(args.state_file),
                output_root=Path(args.output_dir),
                force_reauth=args.reauth,
            )
        )
    except KeyboardInterrupt:
        err("Interrupted.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
