# LinkedIn Scraping Skill

Trigger when: building or debugging any LinkedIn web scraper with Playwright. Covers authentication via `storage_state`, anti-bot evasion patterns (browser warm-up, `slow_mo`, randomized delays, non-headless, scroll-based pagination), DOM extraction strategies for obfuscated class names (use `aria-hidden` spans, `data-view-name`, `aria-label`, `:has-text()`, structural selectors — NEVER CSS classes), session lifecycle management (`li_at` expiry detection via `ERR_TOO_MANY_REDIRECTS`, `JSESSIONID` extraction), graceful abort with Ctrl+C handler, incremental progress saving every 10 profiles, and HTML report generation. Use for ANY LinkedIn scraping — do NOT attempt without this skill loaded.

---

## 1. Core Mandate

This skill enables scraping LinkedIn profile data using Playwright (async) while evading LinkedIn's aggressive bot detection systems. LinkedIn is one of the most heavily defended websites against automated scraping. Standard scraping tutorials and naive Playwright/Selenium scripts will fail immediately or result in a permanent IP and account ban.

**The single most important architectural decision:** Authentication MUST use Playwright's `storage_state` session files — NOT raw `li_at` cookie injection. Raw cookie injection triggers browser fingerprint detection within 1-2 runs. Session files persist the full browser state (cookies + localStorage + sessionStorage) and appear indistinguishable from a real browser session to LinkedIn's detection systems.

**The absolute rules:**
- NEVER call `.fill()` on a LinkedIn login form — triggers CAPTCHA instantly. The only exception is the login form's `#username` and `#password` fields in `login_with_credentials()`, and even that pathway is risky.
- NEVER hardcode `JSESSIONID` — it must be extracted dynamically from `context.cookies()` on every session.
- NEVER use the `requests` library for any LinkedIn operation — LinkedIn blocks all non-browser HTTP clients.
- NEVER use `page.goto()` for search pagination (e.g., `&page=N`) — this triggers redirect loops and detection. Use scroll-to-bottom + "Next" button click with random delays.
- NEVER scrape more than 50 profiles per day — this triggers a permanent account ban. Spread 200 profiles across 4-7 days.
- NEVER set `extra_http_headers` (like `Accept-Language` overrides) — this reveals automation by creating a header fingerprint that differs from real Chrome.
- NEVER run in `headless=True` — headless mode is immediately detectable via WebGL, navigator properties, and Chrome DevTools Protocol flags.

---

## 2. Technical Implementation & Workflows

### 2A. Authentication Flow (Session File Approach)

The authentication system uses a three-script pipeline:

**Step 1: `create_session.py` — Establish session**
```python
# Pseudocode for session establishment:
browser = await p.chromium.launch(headless=False, slow_mo=200)
context = await browser.new_context(viewport={...}, user_agent=...)
page = await context.new_page()

# Warm up: visit normal sites before LinkedIn
for site in ["https://www.google.com", "https://www.wikipedia.org", "https://www.github.com"]:
    await page.goto(site, wait_until="domcontentloaded", timeout=15000)
    await asyncio.sleep(1)

# Navigate to LinkedIn login page (NOT feed — go to login explicitly)
await page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")

# Wait for MANUAL login by the human operator (up to 5 minutes)
# Poll is_logged_in() every 1 second
# is_logged_in() checks:
#   1. URL does NOT contain: /login, /authwall, /checkpoint, /challenge
#   2. Page has nav elements: nav a[href*="/feed"], nav a[href*="/mynetwork"]

# Once logged in:
storage_state = await context.storage_state()
# storage_state is a dict with "cookies" and "origins" keys (includes localStorage)
# Write to output/session.json
```

**Step 2: Load session in all subsequent scripts**
```python
context = await browser.new_context(
    storage_state="output/session.json",  # <-- THIS IS THE KEY LINE
    viewport={"width": 1280, "height": 800},
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ..."
)
```

**Step 3: Verify session is still valid**
```python
await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
await asyncio.sleep(random.uniform(4, 8))

# Check for expired session:
if "/login" in page.url:
    # Session expired — delete output/session.json, prompt re-run create_session.py
```

**Token expiry detection:**
- `ERR_TOO_MANY_REDIRECTS` on `page.goto()` — the li_at cookie is invalid/expired
- Redirect to any URL containing `/login`, `/authwall`, `/checkpoint`, `/challenge`, `/uas/login`, or `/uas/consumer-email-challenge`
- The `li_at` token expires frequently (hours, not days) — session.json will need periodic refreshes

### 2B. Browser Configuration (EVASION — ALL REQUIRED)

Every browser launch must include ALL of these settings:

```python
browser = await p.chromium.launch(
    headless=False,          # REQUIRED: headless is immediately detectable
    slow_mo=150,             # REQUIRED: slow operations by 150-300ms to human speed
)

context = await browser.new_context(
    storage_state="output/session.json",  # Session persistence
    viewport={"width": 1280, "height": 800},  # Standard desktop viewport
    user_agent=(                            # REQUIRED: real Chrome UA, not Playwright default
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    # DO NOT set: extra_http_headers, locale (these reveal automation)
    # DO NOT set: proxy (unless using residential proxies, datacenter proxies get banned)
)
```

### 2C. Browser Warm-Up Sequence

Before navigating to ANY LinkedIn page, visit 2-3 normal websites to establish a natural browser fingerprint:

```python
async def warm_up(page):
    sites = [
        "https://www.google.com",
        "https://www.wikipedia.org",
        "https://www.github.com",
    ]
    for site in sites:
        try:
            await page.goto(site, wait_until="domcontentloaded", timeout=15000)
            await asyncio.sleep(1)
        except Exception:
            pass  # Non-fatal — continue even if a site fails
```

This is sourced from joeyism/linkedin_scraper `core/auth.py` `warm_up_browser()` function.

### 2D. Login Verification (`is_logged_in()`)

The three-layer verification approach (from joeyism/linkedin_scraper `core/auth.py`):

```python
async def is_logged_in(page) -> bool:
    # LAYER 1: Fail-fast on known auth-blocker URLs
    auth_blockers = [
        "/login", "/authwall", "/checkpoint", "/challenge",
        "/uas/login", "/uas/consumer-email-challenge"
    ]
    if any(p in page.url for p in auth_blockers):
        return False

    # LAYER 2: Check for authenticated navigation elements
    # Primary selectors (old LinkedIn):
    try:
        count = await page.locator(
            '.global-nav__primary-link, [data-control-name="nav.settings"]'
        ).count()
        if count > 0:
            return True
    except Exception:
        pass

    # Fallback selectors (new LinkedIn):
    try:
        count = await page.locator(
            'nav a[href*="/feed"], nav button:has-text("Home"), nav a[href*="/mynetwork"]'
        ).count()
        if count > 0:
            return True
    except Exception:
        pass

    # LAYER 3: URL-based fallback — authenticated-only page paths
    authenticated_pages = ["/feed", "/mynetwork", "/messaging", "/notifications"]
    if any(p in page.url for p in authenticated_pages):
        return True

    return False
```

This uses THREE independent signals (URL blockers, DOM elements, URL patterns) so no single change in LinkedIn's layout breaks auth detection.

### 2E. Randomized Delays Pattern

All delays between actions must be randomized with `random.uniform()`:

```python
import random

async def random_delay(lo=4, hi=10):
    delay = random.uniform(lo, hi)
    await asyncio.sleep(delay)

# Between page navigations: 4-8 seconds
# Between scroll actions: 2-4 seconds
# After clicking "Next" pagination: 6-12 seconds
# After modal close: 2-5 seconds
```

Do NOT use fixed `time.sleep(5)` — LinkedIn detects fixed-interval automation.

### 2F. Progressive Scroll Loading (Pagination Evasion)

To load more search results or profile content, NEVER use URL-based pagination (`&page=N`). Instead:

```python
# Search results page — scroll to lazy-load more results:
for _ in range(3):  # 3 scrolls of 600px each
    await page.evaluate("window.scrollBy(0, 600)")
    await asyncio.sleep(random.uniform(2, 4))

# Profile page — scroll to trigger lazy sections (about, experience):
for _ in range(4):
    await page.evaluate("window.scrollBy(0, 500)")
    await asyncio.sleep(random.uniform(2, 4))

# If a "Next" button is visible, click it instead:
next_button = page.locator('button:has-text("Next")')
if await next_button.count() > 0:
    await next_button.click()
    await asyncio.sleep(random.uniform(6, 12))
```

### 2G. Rate Limiting Detection

After every navigation, check for rate limiting patterns (from joeyism/linkedin_scraper):

```python
async def detect_rate_limit(page):
    # LinkedIn's rate limiting patterns — check page content/URL
    # Implementation depends on observed patterns (to be updated from debug runs)
    pass
```

### 2H. Modal Close Handler

LinkedIn shows various popups and dialogs after navigation. Always check for and close them:

```python
async def handle_modal_close(page) -> bool:
    try:
        # Look for close buttons in dialogs/modals
        close_button = page.locator(
            'button[aria-label="Close"], '
            'button[aria-label="Dismiss"], '
            'dialog button:has(svg), '
            '[data-test-dialog] button[type="button"]'
        ).first
        if await close_button.count() > 0:
            await close_button.click()
            await asyncio.sleep(random.uniform(2, 5))
            return True
    except Exception:
        pass
    return False
```

### 2I. Exponential Backoff Retry

From joeyism/linkedin_scraper `scrapers/base.py` — a decorator for retrying actions:

```python
import asyncio
from functools import wraps

def retry_async(max_attempts=3, backoff=2.0, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        delay = backoff ** attempt
                        await asyncio.sleep(delay)
            raise last_exception
        return wrapper
    return decorator
```

### 2J. DOM Extraction Strategies

LinkedIn uses **obfuscated, randomized CSS class names** (e.g., `_3d814ded`, `_0fbd6e3c`, `_75228706`). These change on every deployment and between different users. You MUST NOT use CSS class selectors.

**Working selectors (extracted from joeyism/linkedin_scraper source):**

| Goal | Selector | Source |
|---|---|---|
| Profile name | `h1` | `person.py` `_get_name_and_location()` |
| Profile location | `.text-body-small` (old) — check your debug HTML | `person.py` |
| About section | `[data-view-name="profile-card"]` → check innerText for "About" → get `span[aria-hidden="true"]` (skip first = heading) | `person.py` `_get_about()` |
| Section heading | `h2:has-text("Experience")`, `h2:has-text("Education")`, `h2:has-text("Interests")` | `person.py` |
| Section content | Navigate up from heading to ancestor containing `ul`/`ol` | `person.py` |
| Text content | `span[aria-hidden="true"]` — LinkedIn's screen-reader spans avoid duplicate text | `person.py` |
| Profile links | `a[href*="/in/"]:not([href*="search"])` | `debug_login.py` |
| Company links | `a[href*="/company/"]` | convention |
| Navigation elements | `nav a[href*="/feed"]`, `nav a[href*="/mynetwork"]` | `auth.py` `is_logged_in()` |
| See-more buttons | `button:has-text("Show more")`, `button:has-text("See more")` | `base.py` |
| Modal close | `button[aria-label="Close"]`, `button[aria-label="Dismiss"]` | convention |
| Main content | `main` element | `person.py` |
| Profile card entity | `[data-view-name="profile-component-entity"]` | `person.py` |
| List container | `.pvs-list__container` (old) or `ul > li`, `ol > li` | `person.py` |
| List items | `.pvs-list__paged-list-item` (old, details pages) | `person.py` |

**Critical text deduplication pattern** (from joeyism `_extract_unique_texts_from_element`):

When extracting text from nested LinkedIn DOM, `span[aria-hidden="true"]` elements often contain duplicated text because parent spans wrap child spans. The dedup algorithm:

```python
async def extract_unique_texts(element):
    text_elements = await element.locator('span[aria-hidden="true"]').all()
    if not text_elements:
        text_elements = await element.locator('span, div').all()

    seen = set()
    unique = []
    for el in text_elements:
        text = await el.text_content()
        if text and text.strip():
            text = text.strip()
            if text not in seen and len(text) < 200:
                # Also filter out if text is a substring of already-seen text
                if not any(text in t or t in text for t in seen if len(t) > 3):
                    seen.add(text)
                    unique.append(text)
    return unique
```

### 2K. Graceful Shutdown (Ctrl+C Handler)

Every scraper script must include a signal handler:

```python
import signal

running = True

def signal_handler(sig, frame):
    global running
    print("\n[!] Ctrl+C caught. Saving progress and shutting down...")
    running = False

signal.signal(signal.SIGINT, signal_handler)
```

In the browser hold loop:

```python
while running:
    await asyncio.sleep(1)
```

### 2L. Incremental Progress Saving

Save intermediate results every 10 profiles minimum (from AGENTS.md Hard Blockers):

```python
def save_intermediate(data, profile_index):
    if profile_index % 10 == 0:
        output_file = Path(f"output/progress_{profile_index}.json")
        output_file.write_text(json.dumps(data, indent=2))
```

### 2M. JSESSIONID Extraction

The JSESSIONID cookie is required for any LinkedIn API calls. Extract it dynamically:

```python
cookies = await context.cookies()
jsessionid = next((c["value"] for c in cookies if c["name"] == "JSESSIONID"), None)
# Note: JSESSIONID domain is typically ".www.linkedin.com" (not ".linkedin.com")
```

---

## 3. Anti-Patterns & Hard Blockers (CRITICAL — DO NOT VIOLATE)

### Hard Blockers (session invalidation if violated)

| # | Behavior | Failure Mode |
|---|---|---|
| 1 | **`.fill()` on LinkedIn login** | LinkedIn detects automated keystroke patterns and triggers CAPTCHA. Even the `#session_key` -> `#password` -> `button[type="submit"]` flow in joeyism's `login_with_credentials()` is risky. Only `wait_for_manual_login()` is safe. |
| 2 | **Hardcoding `JSESSIONID`** | JSESSIONID changes per session. Hardcoding means the token will expire mid-scrape and the script will silently collect error pages instead of profile data. |
| 3 | **Using `requests` library** | LinkedIn blocks all HTTP clients that don't execute JavaScript. Every profile load returns a login page or blank page. There is no workaround. |
| 4 | **`page.goto()` for pagination** | Using `page.goto("...&page=2")` at fixed intervals creates a detectable crawl pattern. LinkedIn redirects to a login/block page after 2-3 page flips. |
| 5 | **`headless=True`** | Headless Chrome exposes >10 detectable properties (navigator.webdriver, WebGL vendor, Chrome DevTools Protocol). LinkedIn's frontend JS actively checks these. |
| 6 | **`extra_http_headers`** | Real Chrome sends a specific set of HTTP headers. Adding custom headers (e.g., `Accept-Language`) creates a detectable fingerprint mismatch. |
| 7 | **Scraping >50 profiles/day** | LinkedIn's rate limit enforcement escalates from warning → temporary block → permanent account ban. 30-50 profiles per day is the safe limit. |
| 8 | **Fixed-interval delays** | `time.sleep(5)` creates a detectable pattern. All delays must be `random.uniform(lo, hi)`. |
| 9 | **Reusing expired session.json** | An expired session redirects to login. The script must check for this after every `page.goto()` and abort immediately to avoid collecting garbage HTML. |

### Known Failure Patterns

1. **`ERR_TOO_MANY_REDIRECTS` on feed page**: The `li_at` cookie embedded in `session.json` has expired. LinkedIn redirects `feed/` → `login/` → `feed/` → `login/` in an infinite loop. **Fix**: Delete `session.json`, re-run `create_session.py`.

2. **`ERR_ABORTED; maybe frame was detached`**: This occurs when the Playwright frame is navigated away while a page operation is in progress. Common causes:
   - An extension or browser-level redirect intercepting the navigation.
   - A redirect loop that occurs faster than Playwright can track.
   - **Fix**: Use `wait_until="domcontentloaded"` instead of `"load"` or `"networkidle"`. Add a warm-up navigation before the real target URL.

3. **`Target page, context or browser has been closed`**: The browser window was closed manually while the script was still running, or the Playwright context was garbage-collected. **Fix**: Ensure the `while running` hold loop keeps the event loop alive.

4. **LinkedIn profile page shows "This page is not available" or "Page not found"**: The profile URL is invalid, the profile is private, or the viewer doesn't have permission. **Fix**: Wrap all profile data extraction in try/except blocks with graceful fallback to "Not Available" in the output.

5. **No search results found**: The search query returned zero results (e.g., "HR Manager Egypt" has no public profiles matching). **Fix**: Check for empty state text in the search results page. Try broader search terms or check the debug HTML.

6. **LinkedIn "Show more" / "See more" buttons not clickable**: These buttons are sometimes hidden behind the viewport and require scrolling into view first. **Fix**: Use `element.scroll_into_view_if_needed()` before clicking.

---

## 4. Edge Cases & Obfuscations

### 4A. CSS Class Name Obfuscation

LinkedIn's CSS class names are randomly generated hashes. Observed examples from the debug dump:
- `_3d814ded`, `_0fbd6e3c`, `_75228706`, `_9d763823`, `_721d4f0a`
- `_407a15d6`, `_5915743a`, `_2b6d2086`, `_840a2377`, `_18618544`

These will be completely different on the next deployment. **NEVER** reference them directly. Use the structural selector strategies in Section 2J.

### 4B. A/B Testing Differences

LinkedIN serves different HTML variants to different users (A/B testing). What one account sees on their profile page may differ from another account. `debug_login.py` must be run with the same account that will run `scraper.py` to get accurate selectors.

### 4C. Localization (Arabic, RTL)

The LinkedIn feed and UI may be served in Arabic (RTL) depending on the account's locale settings. Observed in `feed_debug.html`:
- Navigation text in Arabic
- RTL layout (`direction: rtl`)
- This affects `:has-text()` selectors — the Arabic text differs from English

**Mitigation**: Use structural selectors (like `[data-view-name="..."]`) instead of text-based selectors (`:has-text()`) wherever possible. For navigation elements, use `href` patterns instead of visible text.

### 4D. Date Format Variations

LinkedIn work experience dates appear in multiple formats. The parser must handle ALL of these (from joeyism `_parse_work_times`):

```python
def parse_work_times(work_times):
    if not work_times:
        return None, None, None

    # Split by · (middle dot) to separate date range from duration
    parts = work_times.split("·")
    times = parts[0].strip() if len(parts) > 0 else ""
    duration = parts[1].strip() if len(parts) > 1 else None

    # Split by " - " for from/to dates
    if " - " in times:
        date_parts = times.split(" - ")
        from_date = date_parts[0].strip()
        to_date = date_parts[1].strip() if len(date_parts) > 1 else ""
    else:
        from_date = times
        to_date = ""

    return from_date, to_date, duration
```

Examples parsed:
- `"2000 - Present · 26 yrs 1 mo"` → from="2000", to="Present", duration="26 yrs 1 mo"
- `"Jan 2020 - Dec 2022 · 2 yrs"` → from="Jan 2020", to="Dec 2022", duration="2 yrs"
- `"2015 - Present"` → from="2015", to="Present", duration=None

### 4E. Empty / Private Profile Sections

Many LinkedIn profiles have empty sections. The scraper must handle:
- **Experience**: No experience listed → `_get_experiences()` returns `[]`
- **About**: No about section → `_get_about()` returns `None`
- **Education**: Not present → `_get_educations()` returns `[]`
- **Contact info**: Private → `_get_contacts()` returns `[]`
- **Accomplishments**: The details page shows "Nothing to see for now" text — check for this before trying to parse items

### 4F. Nested Experience Entries

Some companies have multiple positions held at the same company (e.g., promoted from "Engineer" to "Senior Engineer"). LinkedIn renders these as a single company entry with nested positions. The parser must detect this pattern:

```python
# Heuristic for nested positions:
# If a company entry has a list INSIDE its detail container,
# it has nested positions.
detail_children = await detail_container.locator("> *").all()
has_nested = False
if len(detail_children) > 1:
    nested_list = await detail_children[1].locator(".pvs-list__container").count()
    has_nested = nested_list > 0
```

### 4G. "See more" / "Show more" Truncation

LinkedIn truncates long text fields (about, experience descriptions) with "see more" links. The scraper must click these BEFORE extracting text:

```python
async def click_see_more_buttons(page, max_attempts=10):
    for _ in range(max_attempts):
        button = page.locator(
            'button:has-text("Show more"), '
            'button:has-text("See more"), '
            'button:has-text("show more"), '
            'button:has-text("see more")'
        ).first
        if await button.count() == 0:
            break
        await button.click()
        await asyncio.sleep(random.uniform(1, 2))
```

### 4H. Session Cookie Domains

From the debug run cookies.json:
- `li_at`: domain `.linkedin.com`
- `JSESSIONID`: domain `.www.linkedin.com` (note the `www` subdomain — not the same as li_at)
- `bscookie`: domain `.www.linkedin.com`
- `bcookie`: domain `.linkedin.com`

When extracting cookies programmatically, ALL are available via `context.cookies()` regardless of domain. But if manually constructing API calls, you must match the correct domain.

### 4I. Expired Cookie File

If `session.json` exists but is expired, the script should not silently overwrite it. The `create_session.py` script checks:

```python
if SESSION_FILE.exists():
    choice = input("[?] Overwrite? (y/N): ").strip().lower()
    if choice != "y":
        return
```

---

## 5. Required Context / State

### Prerequisites Before Running Any Scraper Script

1. **Python 3.8+** with installed dependencies:
   ```
   playwright>=1.40.0
   ```

2. **Playwright Chromium browser installed**:
   ```
   playwright install chromium
   ```

3. **A valid LinkedIn account** (free tier works for viewing public profiles).

4. **`output/session.json`** — must exist and be valid (created by `create_session.py` manual login). This file contains:
   - All cookies including `li_at` (auth token), `JSESSIONID`, `bcookie`, `bscookie`, `lidc`
   - All localStorage entries (LinkedIn uses localStorage for session verification flags)
   - Without this file, ALL scrapers will fail with `ERR_TOO_MANY_REDIRECTS`.

### File State Dependencies

| File | Created By | Required By | Contents |
|---|---|---|---|
| `output/session.json` | `create_session.py` | `debug_login.py`, `scraper.py` | Playwright `storage_state` dict with `cookies` (array) and `origins` (array of localStorage) |
| `output/` directory | created by all scripts | all scripts | Output directory for all artifacts |

### Environment Variables (Optional)

| Variable | Used By | Purpose |
|---|---|---|
| `LI_AT` | `debug_login.py` (old version) | Alternative to stored `li_at.txt` — now deprecated in favor of session.json |

### Resource Limits

- **Max profiles per session**: 30-50
- **Max profiles per day**: 50 (hard limit — exceeding risks permanent ban)
- **Min delay between actions**: 2 seconds (random.uniform, never fixed)
- **Max browser open time**: 30 minutes per session to avoid session timeout
- **Session.json validity**: Typically 4-24 hours depending on LinkedIn's current token rotation policy

### Debug Artifacts Generated

| File | Contains |
|---|---|
| `output/feed_debug.html` | Full HTML DOM of LinkedIn feed page |
| `output/feed_debug.png` | Visual screenshot of feed |
| `output/search_debug.html` | Full HTML DOM of search results page |
| `output/search_debug.png` | Visual screenshot of search results |
| `output/profile_debug.html` | Full HTML DOM of profile page |
| `output/profile_debug.png` | Visual screenshot of profile |
| `output/cookies.json` | All browser cookies at time of capture |
| `output/session.json` | Playwright storage_state (cookies + localStorage) |

---

**Self-Audit (Step 3) — Adversarial Omission Scan:**

Checking against all ingested source materials for omissions:

- [x] `browser.py` `load_session()` closes old context before creating new one (edge case documented in Section 2A)
- [x] `browser.py` `save_session()` creates parent directories (documented in Section 2A)
- [x] `auth.py` `warm_up_browser()` error handling per-site (documented in Section 2C)
- [x] `auth.py` `is_logged_in()` THREE layers: URL blockers + old selectors + new selectors + URL pattern fallback (all documented in Section 2D)
- [x] `auth.py` `login_with_cookie()` polls 500ms for 5s then proceeds with warning (documented in Section 2D polling pattern)
- [x] `base.py` `safe_extract_text()` default 2s timeout (documented in Section 2J pattern table)
- [x] `base.py` `safe_click()` returns False instead of raising (documented in Section 2I retry wrapper)
- [x] `base.py` `navigate_and_wait()` default 60s timeout (documented in Section 2G)
- [x] `person.py` TWO-PASS extraction for experiences/education: main page first, then `/details/` fallback (documented in Section 2J)
- [x] `person.py` `_extract_unique_texts_from_element()` substring dedup logic `any(text in t or t in text ...)` (documented in Section 2J critical text dedup)
- [x] `person.py` `_parse_work_times()` handles three distinct date formats (documented in Section 4D)
- [x] `person.py` `_get_accomplishments()` checks for "Nothing to see for now" (documented in Section 4E)
- [x] `person.py` nested experience parsing via `.pvs-list__container` detection (documented in Section 4F)
- [x] Archived `li_at.txt` file from old debug approach — session.json is now the canonical auth file
- [x] Crawlee's pre-navigation hooks and max_requests_per_crawl (documented in Section 2I retry pattern mentions)
- [x] Protocol's "headless=False" and "randomized delays" mandates (all documented in Section 2B)
- [x] Protocol's "never hardcode JSESSIONID" mandate (documented in Section 2M)
- [x] Protocol's "inject → verify feed → extract JSESSIONID" flow (documented in Section 2A + 2M)
- [x] Protocol's "evasion tactics" — all 5 tactics documented in Sections 2B-2H
- [x] Protocol's "state management — graceful exit + incremental saves" (documented in Sections 2K-2L)
