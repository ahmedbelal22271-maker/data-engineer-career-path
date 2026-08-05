---
name: duckduckgo-search
description: Use when orchestrating OSINT data gathering or web scraping via the DuckDuckGo Search (ddgs) Python library. Triggers for API implementation, rate limit handling, proxy configuration, and DHT network caching configuration.
---
# DuckDuckGo Search (DDGS) API

## 1. Core Mandate
This skill governs the integration and execution of the `duckduckgo_search` library (`ddgs` module). You must NEVER treat this library as a simple REST client or a basic wrapper. It is a highly concurrent metasearch aggregator with built-in async loops, daemon threads, a peer-to-peer (DHT) caching engine, dynamic subclass reflection, and TLS-impersonation HTTP clients. You must explicitly control its context manager, handle its aggressive concurrency scaling, and explicitly define timeout/proxy configurations to avoid background thread leaks, zombie processes, or rate-limit blocks.

## 2. Technical Implementation & Workflows

The primary interaction layer is the `DDGS` context manager, which aggregates results from dynamically loaded internal engine backends.

**Initialization & Query Execution:**
```python
from ddgs import DDGS
from ddgs.exceptions import DDGSException, TimeoutException

# Context manager is mandatory to ensure backend threads/async loops are released
with DDGS(proxy="socks5://user:pass@host:port", timeout=10, spawn_api=False) as ddgs:
    # 1. Metasearch (Auto-shuffles engines, defaults to wikipedia/grokipedia + others)
    results = ddgs.text("search query", max_results=100, backend="auto")
    
    # 2. Extract HTML/Text directly from a URL (bypasses standard requests library)
    # Available formats: "text_markdown", "text_plain", "text_rich", "text" (raw HTML), "content" (raw bytes)
    page_data = ddgs.extract("https://example.com", fmt="text_markdown")
```

**Architectural Patterns:**
- **Concurrency Model (`ddgs.py`):** `_search_sync` dispatches parallel queries via a `ThreadPoolExecutor`. The thread pool ceiling scales dynamically based on available engines: `min(len_unique_providers, ceil(max_results / 10) + 1)`.
- **Dynamic Engine Discovery (`engines/__init__.py`):** Backends are not hardcoded. The library uses `pkgutil.iter_modules` and `inspect.getmembers` to build the `ENGINES` registry at runtime. A class is only loaded if:
  1. It subclasses `BaseSearchEngine`.
  2. Its class name does not start with `"Base"`.
  3. It explicitly declares `disabled = False` (the registry checks `getattr(cls, "disabled", True)`).
  4. It explicitly defines both `name: str` and `category: str`.
- **TLS Impersonation (`http_client.py`):** All outbound requests (including `ddgs.extract()`) are routed through `primp.Client`. The library forces `impersonate="random"` and `impersonate_os="random"` to bypass WAFs and anti-bot systems (like Cloudflare).

## 3. Anti-Patterns & Hard Blockers (CRITICAL)

- **DO NOT IGNORE CLEANUP (ZOMBIE THREADS):** Never instantiate `DDGS()` without the `with` block or manual cleanup in long-running processes. The library spawns a background `ThreadPoolExecutor(_cache_executor)` and an `asyncio` event loop daemon thread (`_async_thread`). Failing to clean up causes severe thread starvation.
- **DO NOT USE `requests` FOR URL FETCHING:** If `DDGS` is in context, do not use standard HTTP libraries (`requests`, `aiohttp`, `urllib`) to visit scraped links. Standard libraries will trigger bot defenses. ALWAYS use `ddgs.extract()` which relies on the Rust-based `primp.Client` with built-in JA3/TLS impersonation.
- **DO NOT HARDCODE BACKENDS IGNORANTLY:** If setting `backend="wikipedia,grokipedia"`, recognize that if a backend string doesn't match an internal key, the API logs a warning. If ALL specified backends are invalid, it silently overrides your config and recursively calls itself with `backend="auto"`.
- **EXCEPTION OBFUSCATION:** Do not write bare `except Exception:`.
  - The API catches `primp.TimeoutError` and re-raises `TimeoutException`.
  - It raises a generic `DDGSException("No results found.")` when queries yield nothing. 
  - If a thread crashes, `_search_sync` checks if the string `"timed out"` is present in the internal exception string. If yes, it throws `TimeoutException`, otherwise `DDGSException`.

## 4. Edge Cases & Obfuscations

- **Network Caching & DHT Spawning:** The API supports a peer-to-peer network cache via an optional `DhtClient` aiming at `http://localhost:4479`. If `spawn_api=True` is passed to the constructor, it uses `subprocess.Popen` to launch `python -m ddgs api -d` silently in the background. 
- **Aggressive Subprocess Cleanup:** To prevent zombie DHT servers, `ddgs.py` hooks into Python's `atexit.register(_cleanup_api_process)`. When the parent Python script exits, it forcefully calls `.poll()`, `.terminate()`, and subsequently `.kill()` on the subprocess, and forcefully shuts down the `asyncio` loop.
- **Graceful Import Failures:** If the `dht` dependencies are missing from the pip environment, the DHT health check might succeed, but `import DhtClient` fails. It silently suppresses the `ImportError` and disables the network cache without crashing the search execution.
- **Proxy Environment Resolution:** Proxies can be explicitly passed during initialization (`proxy="..."`), but if omitted, the library automatically resolves aliases via an internal `_expand_proxy_tb_alias` helper, or falls back to the system environment variable `DDGS_PROXY`.
- **Result De-duplication:** The internal `ResultsAggregator` automatically strips duplicate results by comparing the `"href"`, `"image"`, `"url"`, and `"embed_url"` keys before returning them to the user.

## 5. Required Context / State
- **Dependencies:** Requires the `duckduckgo-search` and `primp` pip packages. (DHT caching requires optional network dependencies).
- **Environment Variables:** `DDGS_PROXY` must be set if system-wide proxy routing is required and not explicitly provided.
- **Network Constraints:** Outbound TCP 443 for primary search, and potentially local TCP 4479 if DHT API server caching is enabled.
