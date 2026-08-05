# SECTION 14 — Error Recovery

**If a Phase Gate fails:** Identify the specific failing condition. Do not proceed past the gate. Fix the condition. Recheck only that gate — do not re-run preceding phases unless the failing condition requires it.

**If a chunk was missed during Phase 1:** Re-read the missed chunk. Add its spine entry to `spine.md`. Process it through Phase 2. Update all affected topic pages and `index.md`. Log the recovery in `log.md`. Recheck Phase 1 and Phase 2 Gates before proceeding.

**If the line count does not reconcile at the Phase 1 Gate:** Stop all processing. Re-read from the beginning of the unreconciled region. Do not reconcile by estimating. The reconciliation must be arithmetically exact.

**If a contradiction cannot be resolved during Phase 3:** Mark `[UNRESOLVED — HUMAN CLARIFICATION REQUIRED]` in `contradictions.md`. Note it explicitly in `master_summary.md`. Do not guess. The downstream output section that touches this content must either defer to the user for resolution or acknowledge the uncertainty explicitly in the final output.

**If the file is larger than expected:** Do not compress or skip phases. Add chunks and processing passes as needed. A complete wiki is required regardless of final file size. There is no early-exit option based on file size.

**If Oracle-DAG subagent boundaries are breached:** Do not merge the offending subagent's output. Escalate to arbitration. Re-extract the out-of-scope content in a sequential pass. Log the breach, the arbitration, and the resolution in `log.md`.

**If a topic page is found invalid (content missing without accounting):** Identify what is missing by comparing the spine entries for the relevant chunks against the topic page content. Re-extract the missing content. Update `index.md` and `contradictions.md` as relevant. Log the correction. Do not proceed to downstream work until all affected pages are valid.

---

## Scraper Error Recovery

**If the scraper fails on a URL (HTTP error, timeout, connection refused):**
1. Log the failure in `log.md` as `[SCRAPER-FAILURE]` with the URL, error type, and timestamp.
2. Continue with remaining URLs. Do not halt the entire scraping batch for one failure.
3. If the failed URL is critical to the wiki's coverage: retry once after a 10-second delay. If it fails again, escalate to the user.
4. If the failed URL is supplementary: note the gap in `log.md` and proceed without it. The wiki's gap audit (Phase 3) will identify any coverage holes.

**If readability-lxml produces empty or near-empty content (<50 chars):**
1. The scraper already logs `[CONTENT TOO SHORT]` and skips the file.
2. In `log.md`, record `[SCRAPER-EXTRACTION-FAILURE]` with the URL and the reason.
3. Do not include empty/failed files in wiki processing.
4. If the page is critical: try an alternative extraction approach — use `page.content()` directly with html2text instead of readability, or use `page.inner_text('body')` for plain text fallback.

**If Playwright browser fails to launch:**
1. Check that Playwright browsers are installed: `python -m playwright install chromium`
2. If installation fails: escalate to the user with the full error output.
3. If installation succeeds: retry the scraping operation.

**If manifest.json is corrupted or unreadable:**
1. Delete the corrupted manifest.
2. Re-scrape all URLs with `--force` flag.
3. Log the corruption event in `log.md`.

**If scraped file YAML frontmatter is missing or malformed:**
1. The file may have been written by an older version of the scraper or corrupted during write.
2. Attempt to reconstruct frontmatter from the file content and filename.
3. If reconstruction fails: re-scrape the URL.
4. Log the reconstruction in `log.md`.
