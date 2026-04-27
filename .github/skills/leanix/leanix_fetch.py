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
DEFAULT_WORKSPACE = "PGPROD"  # URL path segment after the host after login

# Known P&G GenAI-ecosystem apps. Extend as siblings come online.
KNOWN_APPS = ["ChatPG", "ImagePG", "AskPG", "InsightsPG", "AIAPPS"]

LOGIN_DETECT_TIMEOUT_MS = 180_000   # 3 min to complete SSO + MFA
PAGE_NAV_TIMEOUT_MS = 45_000
SEARCH_WAIT_MS = 5_000
DIAGRAM_RENDER_WAIT_MS = 6_000   # let canvas paint before screenshot
MAX_DIAGRAMS_PER_RUN = 30        # safety: don't grind for an hour
BLANK_PNG_SIZES = {92615}        # known size of LeanIX 'no access / not found' PNG


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
    """Launch Chrome and build a browser context, loading saved state if present.

    Uses channel="chrome" (the user's installed Google Chrome) instead of
    Playwright's bundled Chromium. LeanIX's UI5 Web Components fail to fully
    register in bundled Chromium, breaking the export-as-PNG dialog handler.
    Falls back to bundled Chromium if Chrome is not installed.
    """
    try:
        browser = await pw.chromium.launch(channel="chrome", headless=not headful)
    except Exception:
        browser = await pw.chromium.launch(headless=not headful)
    storage_state: str | None = str(state_file) if state_file.exists() else None
    context = await browser.new_context(
        storage_state=storage_state,
        viewport={"width": 1440, "height": 900},
        accept_downloads=True,
    )
    return context

async def ensure_logged_in(
    pw: Playwright,
    base_url: str,
    workspace: str,
    state_file: Path,
    *,
    force_reauth: bool,
) -> None:
    """
    Verify we have a working LeanIX session, launching a visible browser for
    manual SSO + MFA if we don't.
 
    IMPORTANT: LeanIX tenants are multi-workspace and the IDP binding is on the
    workspace, not the host. Hitting the bare host (e.g. https://pg.leanix.net)
    during SSO produces the server-side error "No active Identity Provider (IDP)
    found" because LeanIX has no way to route you to the right IDP. We always
    navigate to the workspace-scoped URL (e.g. https://pg.leanix.net/PGPROD/)
    so the IDP dance resolves correctly. The workspace slug is case-sensitive.
    """
    login_url = f"{base_url.rstrip('/')}/{workspace.strip('/')}/"
 
    if force_reauth and state_file.exists():
        log(f"--reauth specified; deleting existing {state_file.name}")
        state_file.unlink()
 
    needs_interactive_login = not state_file.exists()
 
    if not needs_interactive_login:
        # Validate the saved session by hitting the workspace URL headlessly.
        log("Validating saved session...")
        context = await new_context(pw, state_file, headful=False)
        page = await context.new_page()
        try:
            await page.goto(login_url, timeout=PAGE_NAV_TIMEOUT_MS)
            # If LeanIX redirected us off leanix.net (to the SSO host) or back
            # to a login page, the session is dead and we need to re-auth.
            final_host = _host_of(page.url)
            if "leanix.net" not in final_host or "/login" in page.url.lower():
                warn(f"Saved session looks stale — landed on {page.url}")
                needs_interactive_login = True
        except PlaywrightTimeoutError:
            warn("Timed out validating saved session; will re-auth.")
            needs_interactive_login = True
        finally:
            await context.close()
 
    if needs_interactive_login:
        context = await new_context(pw, state_file, headful=True)
        page = await context.new_page()
        try:
            await page.goto(login_url, timeout=PAGE_NAV_TIMEOUT_MS)
 
            # User-driven completion signal. Guessing "logged in" from URL
            # patterns is unreliable across SSO + MFA flows — intermediate
            # callback URLs can match any "looks like LeanIX" heuristic and
            # cause us to close the browser mid-MFA. The user knows when the
            # workspace is actually loaded; let them tell us.
            print("", flush=True)
            print("=" * 72, flush=True)
            print(" LeanIX first-time login", flush=True)
            print("-" * 72, flush=True)
            print(" 1. A Chromium window is now open.", flush=True)
            print(" 2. Complete the full P&G SSO flow in that window:", flush=True)
            print("    - enter your P&G email + password", flush=True)
            print("    - approve the PingID push on your phone", flush=True)
            print("    - wait for the LeanIX workspace dashboard to load", flush=True)
            print(" 3. When you can see the LeanIX workspace home / inventory,", flush=True)
            print("    come back here and press ENTER to save the session.", flush=True)
            print("", flush=True)
            print(" Do NOT press ENTER until the LeanIX page is fully loaded —", flush=True)
            print(" pressing too early saves an incomplete session and the next", flush=True)
            print(" run will fail.", flush=True)
            print("=" * 72, flush=True)
            print("", flush=True)
 
            # Block on input() without freezing the event loop. Playwright's
            # browser stays responsive while we wait for the user.
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                input,
                "Press ENTER once LeanIX is fully loaded in the Chromium window: ",
            )
 
            # Best-effort sanity check — warn if we're clearly still on a login
            # or error page, but save the state regardless so the user can
            # decide whether to re-run with --reauth.
            current_url = page.url
            final_host = _host_of(current_url)
            url_lower = current_url.lower()
            looks_wrong = (
                "leanix.net" not in final_host
                or "/login" in url_lower
                or "error" in url_lower
                or "sso" in url_lower
            )
            if looks_wrong:
                warn(
                    f"Current page is {current_url} — this does not look like "
                    "the LeanIX workspace. Saving session state anyway; if the "
                    "diagram fetch fails, re-run with --reauth."
                )
            else:
                log(f"Current page: {current_url}")
 
            # Give any post-login XHRs a chance to settle before we snapshot.
            try:
                await page.wait_for_load_state("networkidle", timeout=15_000)
            except PlaywrightTimeoutError:
                pass
 
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

def _walk_for_titles(node: Any, out: dict[str, str]) -> None:
    """
    Walk a parsed JSON structure and record `id -> name/displayName/title`
    pairs for every object that looks like a diagram entity. Used to label
    UUIDs harvested from network responses.
    """
    if isinstance(node, dict):
        node_id = node.get("id")
        if isinstance(node_id, str) and len(node_id) == 36 and node_id.count("-") == 4:
            for key in ("name", "displayName", "title", "label"):
                val = node.get(key)
                if isinstance(val, str) and val.strip():
                    out.setdefault(node_id, val.strip())
                    break
        for v in node.values():
            _walk_for_titles(v, out)
    elif isinstance(node, list):
        for item in node:
            _walk_for_titles(item, out)


async def search_diagrams_ui(
    context: BrowserContext,
    base_url: str,
    workspace: str,
    app: str,
    output_dir: Path,
    write_manifest_partial=None,
) -> tuple[list[DiagramRecord], list[str]]:
    """
    Navigate the Diagrams module, type the app name into the in-page filter,
    then iterate over the rendered diagram tiles, opening each in turn and
    capturing a PNG. Returns (records, warnings).

    Approach: do exactly what a human does. The Diagrams overview filters
    its tile grid as you type. After filtering, we collect the visible tile
    elements via several candidate selectors, click each one to navigate to
    its detail page, screenshot the rendered diagram. We do NOT harvest UUIDs
    from network responses or HTML — that approach grabs Fact Sheets,
    dashboards, and other unrelated entities and produces dozens of blank
    "no access" screenshots.

    Safety:
      - Hard cap MAX_DIAGRAMS_PER_RUN to bound wall time.
      - Skip screenshots with sizes matching known-blank pages.
      - Dedup by screenshot SHA — if the same image lands twice, the URL
        pattern is wrong; abort the loop.
      - If write_manifest_partial is provided, call it after each diagram
        so a Ctrl-C still leaves a useful manifest.
    """
    import hashlib

    records: list[DiagramRecord] = []
    warnings: list[str] = []
    page = await context.new_page()
    page.set_default_timeout(PAGE_NAV_TIMEOUT_MS)

    # ----- Navigate to the Diagrams module ------------------------------
    diagrams_url = f"{base_url}/{workspace}/diagrams/overview/all-diagrams"
    log(f"Navigating to Diagrams module: {diagrams_url}")
    try:
        await page.goto(diagrams_url, wait_until="networkidle")
    except PlaywrightTimeoutError:
        warnings.append("Diagrams URL did not reach networkidle in time.")
        await page.goto(diagrams_url, wait_until="domcontentloaded")
    await page.wait_for_timeout(8_000)  # SPA bootstrap

    # ----- Type the search term into the in-page filter -----------------
    search_selectors = [
        'main input[type="search"]',
        'main input[placeholder*="Search" i]',
        'main input[placeholder*="Filter" i]',
        '[class*="diagram" i] input[type="search"]',
        'input[type="search"]',
    ]
    searched = False
    for selector in search_selectors:
        try:
            loc = page.locator(selector).first
            if await loc.count() > 0 and await loc.is_visible():
                await loc.click()
                await loc.fill("")
                await loc.fill(app)
                await page.wait_for_timeout(2_000)  # debounce
                searched = True
                log(f"Typed '{app}' into selector: {selector}")
                break
        except Exception:
            continue
    if not searched:
        warnings.append("No in-page search input found; will iterate the unfiltered list (capped).")

    try:
        await page.wait_for_load_state("networkidle", timeout=15_000)
    except PlaywrightTimeoutError:
        pass
    await page.wait_for_timeout(2_000)

    # ----- Find clickable diagram tiles in the filtered DOM -------------
    # Try several selectors and pick the smallest plausible tile count
    # (between 1 and 100). Anything larger is almost certainly catching
    # the wrong elements (sidebar, nav, etc.).
    tile_selectors = [
        '[data-testid*="diagram-card" i]',
        '[data-testid*="diagram" i] a[href*="/diagrams/"]',
        '[class*="diagram-card" i] a[href*="/diagrams/"]',
        '[class*="DiagramCard" i] a[href*="/diagrams/"]',
        'main a[href*="/diagrams/"]',
        'a[href*="/diagrams/"]:not([href*="/overview"]):not([href*="/free-draw"]):not([href*="/templates"])',
    ]
    chosen = None  # (selector, count, locator)
    for sel in tile_selectors:
        try:
            loc = page.locator(sel)
            count = await loc.count()
            if 1 <= count <= 100:
                if chosen is None or count < chosen[1]:
                    chosen = (sel, count, loc)
        except Exception:
            continue

    if chosen is None:
        ts = _timestamp()
        debug_screenshot = output_dir / f"debug_no_tiles_{ts}.png"
        debug_html = output_dir / f"debug_no_tiles_{ts}.html"
        output_dir.mkdir(parents=True, exist_ok=True)
        try:
            await page.screenshot(path=str(debug_screenshot), full_page=True)
        except Exception:
            pass
        try:
            html = await page.content()
            debug_html.write_text(html, encoding="utf-8")
        except Exception:
            pass
        warnings.append(
            f"No diagram tiles found in DOM after filtering on '{app}'. "
            f"Saved {debug_screenshot.name} + {debug_html.name} for selector inspection."
        )
        warnings.append(
            "WORKAROUND: open one diagram in your browser, copy its URL, and "
            "re-run with --diagram-url <url> (repeatable)."
        )
        await page.close()
        return records, warnings

    chosen_selector, chosen_count, tiles = chosen
    log(f"Selected tile selector '{chosen_selector}' with {chosen_count} match(es).")
    if chosen_count > MAX_DIAGRAMS_PER_RUN:
        warnings.append(
            f"{chosen_count} tiles found, capping at MAX_DIAGRAMS_PER_RUN={MAX_DIAGRAMS_PER_RUN}."
        )
        chosen_count = MAX_DIAGRAMS_PER_RUN

    # Capture stable URLs BEFORE clicking, since the DOM gets replaced on
    # navigation. We collect href + visible text up front, then iterate by URL.
    targets: list[tuple[str, str]] = []
    seen_urls: set[str] = set()
    raw_hrefs_seen: list[str] = []  # for debugging when filter rejects everything
    for i in range(chosen_count):
        try:
            tile = tiles.nth(i)
            href = await tile.get_attribute("href")
            if not href:
                inner_a = tile.locator('a[href*="/diagrams/"]').first
                if await inner_a.count() > 0:
                    href = await inner_a.get_attribute("href")
            if not href:
                continue
            raw_hrefs_seen.append(href)
            if not _looks_like_diagram_href(href):
                continue
            full_url = href if href.startswith("http") else f"{base_url}{href}"
            if full_url in seen_urls:
                continue
            seen_urls.add(full_url)
            title = (await tile.inner_text() or "").strip().split("\n")[0][:120]
            targets.append((full_url, title or f"diagram-{i+1}"))
        except Exception as exc:
            warnings.append(f"Could not read tile #{i+1}: {exc}")

    if not targets:
        if raw_hrefs_seen:
            log(f"DEBUG: tiles had hrefs but all were rejected by filter. Examples:")
            for h in raw_hrefs_seen[:10]:
                log(f"  {h}")
            warnings.append(
                f"All {len(raw_hrefs_seen)} tile hrefs were rejected by _looks_like_diagram_href. "
                f"First few: {raw_hrefs_seen[:5]}. Filter likely too strict for current LeanIX URL shape."
            )
        else:
            warnings.append("Tiles were detected but none had readable diagram href attributes.")
        await page.close()
        return records, warnings

    log(f"Will export {len(targets)} unique diagram(s).")
    await page.close()

    # ----- Export each diagram -------------------------------------------
    seen_hashes: set[str] = set()
    for index, (full_url, title) in enumerate(targets, start=1):
        try:
            record = await export_diagram_as_png(
                context=context,
                diagram_url=full_url,
                title=title,
                output_dir=output_dir,
                index=index,
            )
        except Exception as exc:
            warnings.append(f"Failed to export diagram {index} ({full_url}): {exc}")
            continue

        # Validate the screenshot
        # Empty png_path means the export failed (no fallback screenshot
        # is written per user requirement). Keep the record for the
        # manifest so the failure is visible, but don't try to dedupe.
        if not record.png_path:
            warnings.append(
                f"Diagram {index} ({title}): native PNG export failed — see debug folder."
            )
            records.append(record)
            log(f"Export FAILED for diagram {index}/{len(targets)}: {title}")
            if write_manifest_partial:
                try:
                    write_manifest_partial(records, warnings)
                except Exception:
                    pass
            continue

        png_path = Path(record.png_path)
        if png_path.exists():
            size = png_path.stat().st_size
            if size in BLANK_PNG_SIZES:
                warnings.append(
                    f"Skipped diagram {index}: PNG size {size} matches known-blank page."
                )
                png_path.unlink(missing_ok=True)
                continue
            digest = hashlib.sha256(png_path.read_bytes()).hexdigest()
            if digest in seen_hashes:
                warnings.append(
                    f"Diagram {index} screenshot duplicates an earlier one. "
                    f"URL pattern likely wrong; aborting remaining exports."
                )
                png_path.unlink(missing_ok=True)
                break
            seen_hashes.add(digest)

        records.append(record)
        log(f"Exported diagram {index}/{len(targets)}: {title}")
        if write_manifest_partial:
            try:
                write_manifest_partial(records, warnings)
            except Exception:
                pass

    return records, warnings

def _looks_like_diagram_href(href: str) -> bool:
    """
    Return True iff the href points at a specific diagram detail page
    (any path under /<workspace>/diagrams/ that is NOT one of the known
    chrome routes like /overview, /free-draw, /templates).

    Examples:
      TRUE  /PGPROD/diagrams/75861387-8ae2-4af3-93d0-f8e47880748c
      TRUE  /PGPROD/diagrams/some-slug-or-id
      FALSE /PGPROD/diagrams/overview/all-diagrams
      FALSE /PGPROD/diagrams/free-draw
      FALSE /PGPROD/diagrams/templates
    """
    if "/diagrams/" not in href:
        return False

    BAD_SEGMENTS = ("/overview", "/free-draw", "/templates", "/personal", "/favorites", "/recent", "/shared")
    for bad in BAD_SEGMENTS:
        if f"/diagrams{bad}" in href:
            return False

    tail = href.split("/diagrams/", 1)[1]
    first_segment = tail.split("?", 1)[0].split("#", 1)[0].split("/", 1)[0]

    # Reject empty path (just /diagrams/) and obvious nav segments.
    if not first_segment or first_segment in ("new", "create", "edit"):
        return False
    return True

async def export_diagram_as_png(
    context: BrowserContext,
    diagram_url: str,
    title: str,
    output_dir: Path,
    index: int,
) -> DiagramRecord:
    """
    Open the diagram page, wait for the canvas to fully render, then use
    LeanIX's native export menu (3-dot kebab → "Export as PNG") to download
    a clean image. Falls back to a full-page screenshot only if the native
    export is not available.

    LeanIX render flow:
      1. Page loads with chrome (toolbar, sidebar) but empty canvas.
      2. Diagram data fetched via XHR.
      3. SVG/canvas elements injected into the diagram pane.
      4. Once visible, the kebab menu's Export options become functional.

    We poll for the diagram pane to actually contain rendered content
    (SVG/canvas children) before attempting export, then bound the wait.
    """
    import re
    output_dir.mkdir(parents=True, exist_ok=True)
    png_path = output_dir / f"diagram_{index:03d}.png"
    page = await context.new_page()
    page.set_default_timeout(PAGE_NAV_TIMEOUT_MS)

    try:
        await page.goto(diagram_url, wait_until="networkidle")
    except PlaywrightTimeoutError:
        await page.goto(diagram_url, wait_until="domcontentloaded")

    # ----- Wait for the diagram canvas to actually contain content ------
    # Try several selectors that typically host rendered diagrams.
    diagram_ready = False
    canvas_selectors = [
        'svg[class*="diagram" i]',
        'svg g[class*="node" i]',  # rendered shapes
        'canvas[class*="diagram" i]',
        '[class*="diagram-canvas" i] svg',
        '[class*="canvas" i] svg g',
        'main svg g',  # LeanIX renders SVG with <g> children once loaded
    ]
    for sel in canvas_selectors:
        try:
            await page.locator(sel).first.wait_for(state="visible", timeout=20_000)
            # Give it a bit more so layout/animation finishes.
            await page.wait_for_timeout(2_000)
            diagram_ready = True
            log(f"  diagram pane ready (matched: {sel})")
            break
        except PlaywrightTimeoutError:
            continue
        except Exception:
            continue
    if not diagram_ready:
        # Last-resort: just wait a longer fixed time.
        await page.wait_for_timeout(DIAGRAM_RENDER_WAIT_MS * 2)

    # ----- Native export: exact LeanIX flow -----------------------------
    # Confirmed sequence (per user, 2026-04-24):
    #   1. Click 3 HORIZONTAL dots (⋯) kebab in the diagram's TOOLBAR
    #      (same row as the diagram title, top of the canvas pane).
    #   2. Click "Export" in the kebab menu.
    #   3. Click "PNG Image" in the submenu.
    #   4. A LeanIX dialog opens with options (Image Zoom, Border Width,
    #      Size, Transparent Background, Appearance, Shadow, Grid, etc.)
    #      and a "Cancel" + "Export" button pair at the bottom.
    #      Click "Export" — NOT "Cancel".
    #   5. After 15-30s, browser download triggers (Playwright intercepts
    #      it; the native OS save dialog is bypassed by accept_downloads).
    png_download_triggered = False
    export_note = ""

    # Set up debug screenshot directory next to the diagram output.
    debug_dir = output_dir / "debug" / f"diagram_{index:03d}"
    debug_dir.mkdir(parents=True, exist_ok=True)

    async def _debug_snap(label: str) -> None:
        """Save a full-page screenshot and an HTML dump for diagnosis."""
        try:
            await page.screenshot(path=str(debug_dir / f"{label}.png"), full_page=True)
        except Exception:
            pass
        try:
            html = await page.content()
            (debug_dir / f"{label}.html").write_text(html, encoding="utf-8")
        except Exception:
            pass

    await _debug_snap("00_loaded")

    # Dismiss any toast notifications that may intercept clicks (e.g.
    # "Image Load Error"). LeanIX puts them in #toast-container.
    try:
        toasts = page.locator('#toast-container .toast-close-button')
        n = await toasts.count()
        for i in range(n):
            try:
                await toasts.nth(i).click(timeout=1_000)
            except Exception:
                pass
        if n:
            log(f"  dismissed {n} toast notification(s)")
            await page.wait_for_timeout(300)
    except Exception:
        pass

    # ---------- Step 1: open the diagram-toolbar kebab (3 horizontal dots) -----
    # CONFIRMED via DOM inspection (debug/diagram_001/00_loaded.html):
    # The button is `<button id="tourMoreButton" icon="overflow"
    #   class="moreButton lx-wsl square withIcon ...">`.
    # It opens a listbox (aria-controls="listbox1").
    kebab_selectors = [
        # Highest-confidence: exact LeanIX id and class.
        'button#tourMoreButton',
        'button.moreButton[icon="overflow"]',
        'button.moreButton',
        'button[icon="overflow"][aria-haspopup="listbox"]',
        # Generic LeanIX overflow icon button as fallback.
        'button[icon="overflow"]',
    ]

    async def _find_diagram_kebab() -> "Optional[Locator]":
        """Find the kebab in the diagram toolbar by:
        1. Trying each selector
        2. For each match, picking the one closest to the top of the
           diagram pane (small y-coordinate, large x-coordinate = top-right).
        """
        candidates = []
        for sel in kebab_selectors:
            try:
                loc = page.locator(sel)
                count = await loc.count()
                for i in range(min(count, 10)):
                    el = loc.nth(i)
                    if not await el.is_visible():
                        continue
                    box = await el.bounding_box()
                    if not box:
                        continue
                    candidates.append((sel, i, box))
            except Exception:
                continue
        if not candidates:
            return None
        # Prefer top-right buttons (small y, large x). Sort by y ascending,
        # then x descending. The diagram toolbar kebab should win.
        candidates.sort(key=lambda c: (c[2]["y"], -c[2]["x"]))
        sel, idx, box = candidates[0]
        log(f"  kebab candidate: selector={sel} idx={idx} pos=({box['x']:.0f},{box['y']:.0f})")
        return page.locator(sel).nth(idx)

    kebab = await _find_diagram_kebab()
    if kebab is None:
        log("  ✗ could not locate diagram kebab menu (3 horizontal dots)")
        await _debug_snap("01_no_kebab_found")
    else:
        await kebab.click()
        await page.wait_for_timeout(800)
        await _debug_snap("01_kebab_open")
        log("  ✓ kebab menu opened")

        # ---------- Step 2: HOVER "Export" in the kebab menu ----------
        # The Export item has class "hasSubdropdown" — hovering opens the
        # submenu which contains "PNG Image", "PDF File", "SVG File", etc.
        # We must KEEP the cursor on a path that doesn't dismiss the
        # submenu while moving to the PNG Image item.
        export_item = page.locator('li.option.hasSubdropdown:has-text("Export")').first
        try:
            await export_item.wait_for(state="visible", timeout=5_000)
            await export_item.hover()
            await page.wait_for_timeout(700)
            await _debug_snap("02_export_hovered")
            log("  ✓ hovered 'Export' in kebab menu (submenu should now be open)")
        except Exception as exc:
            log(f"  ✗ could not hover 'Export' menu item: {exc}")
            await _debug_snap("02_export_not_found")
            export_item = None

        if export_item is not None:
            # ---------- Step 3: click "PNG Image" in submenu ----------
            # With channel="chrome" (real Google Chrome) the UI5 Web
            # Components register correctly and the standard Playwright
            # click on the <li> works. We hover the submenu item first
            # to keep the sub-dropdown open during the click.
            try:
                png_li = page.locator('lx-options-sub-dropdown li.option:has-text("PNG Image")').first
                await png_li.wait_for(state="visible", timeout=5_000)
                await png_li.hover()
                await page.wait_for_timeout(300)
                await png_li.click()
                log("  ✓ clicked 'PNG Image' in submenu")
                await page.wait_for_timeout(1_500)
                await _debug_snap("03_png_image_clicked")

                # ---------- Step 4: dialog Export button ----------
                # The export dialog is an lx-modal with size="dialog" containing
                # form fields (Image Zoom, Border Width, etc.) and footer
                # buttons including "Export" and "Cancel". Cast a wide net.
                dialog_btn = page.locator(
                    'lx-modal button:has-text("Export"):visible, '
                    '.cdk-overlay-pane button:has-text("Export"):visible, '
                    '.modal-footer button:has-text("Export"):visible, '
                    'button.btn-primary:has-text("Export"):visible'
                ).first
                await dialog_btn.wait_for(state="visible", timeout=20_000)
                await _debug_snap("04_dialog_visible")
                log("  ✓ export dialog visible (found dialog Export button)")

                # Step 5: Click Export, expect download (Playwright auto-handles
                # the OS save dialog because accept_downloads=True is set on the
                # browser context).
                async with page.expect_download(timeout=90_000) as dl_info:
                    await dialog_btn.click()
                    log("  ✓ clicked dialog Export button — waiting for download (up to 90s)")
                download = await dl_info.value
                await download.save_as(str(png_path))
                png_download_triggered = True
                export_note = "native PNG via kebab → Export → PNG Image → dialog Export"
                log(f"  ✓ saved PNG: {png_path.name}")
                await _debug_snap("05_after_download")
            except PlaywrightTimeoutError as exc:
                log(f"  ✗ timeout in PNG export flow: {exc}")
                await _debug_snap("xx_flow_timeout")
            except Exception as exc:
                log(f"  ✗ PNG export flow error: {exc}")
                await _debug_snap("xx_flow_error")

    # Per user requirement: NO screenshot fallback. If the native PNG export
    # failed we leave no PNG file behind — the manifest will record the
    # failure and debug/ has the diagnostic info.
    if not png_download_triggered:
        export_note = (
            "EXPORT FAILED — native PNG export did not complete. "
            f"See debug folder for screenshots/HTML at each step: {debug_dir}"
        )
        # Do NOT save a fallback screenshot — user explicitly rejects this.
        png_path_str = ""  # signal failure to caller via empty path in manifest
        log(f"  ✗ export failed; debug artifacts in {debug_dir}")
    else:
        png_path_str = str(png_path)

    record = DiagramRecord(
        title=title,
        diagram_url=diagram_url,
        png_path=png_path_str,
        fetched_at=_now_iso(),
        notes=export_note,
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
    diagram_urls: list[str] | None = None,
) -> int:
    if app not in KNOWN_APPS:
        warn(
            f"'{app}' is not in the known-app list {KNOWN_APPS}. Proceeding anyway, "
            "since LeanIX may have other Fact Sheets. Add it to KNOWN_APPS if this "
            "becomes a regular target."
        )

    async with async_playwright() as pw:
        await ensure_logged_in(pw, base_url, workspace, state_file, force_reauth=force_reauth)

        log(f"Fetching diagrams for app='{app}'...")
        context = await new_context(pw, state_file, headful=False)
        warnings: list[str] = []
        records: list[DiagramRecord] = []
        graphql_result: dict[str, Any] = {"worked": False, "status": None, "fact_sheets": []}

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
            output_dir.mkdir(parents=True, exist_ok=True)
            manifest_path = output_dir / "manifest.json"

            def _write_partial(recs: list[DiagramRecord], warns: list[str]) -> None:
                """Snapshot manifest after each diagram so Ctrl-C is safe."""
                m = Manifest(
                    app=app,
                    base_url=base_url,
                    fetched_at=_now_iso(),
                    diagram_count=len(recs),
                    diagrams=recs,
                    graphql_probe=graphql_result,
                    warnings=list(warns),
                )
                with manifest_path.open("w", encoding="utf-8") as fh:
                    json.dump(asdict(m), fh, indent=2)

            if diagram_urls:
                # Manual mode: skip search entirely, export each URL directly.
                log(f"Manual mode: exporting {len(diagram_urls)} URL(s) provided via --diagram-url.")
                for index, url in enumerate(diagram_urls, start=1):
                    full_url = url if url.startswith("http") else f"{base_url}{url}"
                    try:
                        record = await export_diagram_as_png(
                            context=context,
                            diagram_url=full_url,
                            title=f"manual-{index}",
                            output_dir=output_dir,
                            index=index,
                        )
                        records.append(record)
                        _write_partial(records, warnings)
                    except Exception as exc:
                        warnings.append(f"Failed to export manual URL {full_url}: {exc}")
            else:
                records, warnings = await search_diagrams_ui(
                    context, base_url, workspace, app, output_dir,
                    write_manifest_partial=_write_partial,
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
    p.add_argument(
        "--diagram-url",
        action="append",
        default=[],
        metavar="URL",
        help=(
            "Skip search and export this diagram URL directly. Repeatable. "
            "Use when the search heuristic fails — copy URLs from your browser. "
            "Accepts either an absolute URL or a path like /PGPROD/diagrams/<uuid>."
        ),
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
                diagram_urls=args.diagram_url or None,
            )
        )
    except KeyboardInterrupt:
        err("Interrupted.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
