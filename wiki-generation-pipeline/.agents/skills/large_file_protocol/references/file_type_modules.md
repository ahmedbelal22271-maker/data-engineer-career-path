# SECTION 12 — File Type Modules

Select the module(s) matching the source file's type as identified in the Configuration Preamble. Apply the relevant guidance throughout all phases. Multiple modules may apply simultaneously.

---

## MODULE 12A — Chat-Log Sources

Invoke when the source is a conversation transcript (human-AI, human-human, or multi-party chat log).

**1. Context dependency.** A statement in turn N may only make sense in light of turn N-1. Never extract a claim without absorbing the context of the immediately preceding turn. Capture enough context in the wiki that the reasoning chain is recoverable — not just the conclusion.

**2. Question vs. answer.** The questioner's turns provide context; the answerer's turns are the primary extraction target. Capture what question an answer is responding to. An extracted answer without its motivating question may be unusable.

**3. Hedged language.** Track whether a recommendation was confirmed in a subsequent turn or merely floated as a possibility. If not confirmed: mark `[STATUS: UNCONFIRMED]`. Do not treat exploratory suggestions as settled decisions.

**4. Turn delimiter consistency.** Record the exact turn delimiter format during Phase 0. Apply it consistently throughout all reading phases. If the delimiter format changes partway through the file (common in exported chat logs), note this in `log.md` and update parsing accordingly.

**5. Intra-turn revisions.** If a speaker revises themselves within a single turn (e.g., "Actually, let me reconsider..."), the revision supersedes the earlier statement within that turn. Note inline: `[Self-revised within this turn — earlier: [X]; revised: [Y]; revised is operative]`. This is distinct from inter-turn contradictions (which are handled via `contradictions.md`).

**6. Speaker or version differences.** If the log spans multiple versions of an AI system, multiple participants, or multiple sessions with different configurations, record this in extraction notes. Different versions or participants may have given conflicting advice — a common source of genuine contradictions.

**7. Mandatory sequential processing.** Chat logs are chronologically ordered. Oracle-DAG parallelization is mathematically forbidden for chat-log sources. All chunk independence assessments in Phase 1 must be marked `SEQUENTIAL-ONLY`. Do not override this.

---

## MODULE 12B — Codebase Sources

Invoke when the source is a software codebase, script file, or collection of code files.

**1. Import and dependency mapping.** During Phase 1, pay particular attention to `import`, `require`, `include`, or equivalent dependency declarations. A file that imports another cannot be fully understood without that dependency. Record all import dependencies in the spine entry for each chunk.

**2. Global state identification.** Identify all shared global variables, shared configuration files, shared schema definitions, and shared constants. Any section that reads or modifies shared global state cannot be safely parallelized with other sections that do the same. Mark these `SEQUENTIAL-ONLY` in the independence assessment.

**3. Oracle-DAG primary use case.** Codebase sources are the primary use case for Oracle-DAG. Modules with no shared state and no import dependencies between them are strong parallelization candidates. However, do not declare independence until the Spine confirms it — import maps often reveal non-obvious dependencies.

**4. Logic branching.** When extracting code-related content, capture error handling, edge cases, and configuration details — not just the happy path. Critical logic frequently lives in exception handling and edge conditions.

**5. Changelog maintenance.** When processing a codebase that will be modified (not merely read), maintain a running `CHANGES.md` in `[wiki_dir]/` so the evolution of the project is traceable.

---

## MODULE 12C — Structured Document Sources

Invoke when the source is an academic paper, technical report, PDF, book, specification, or similar document with explicit section structure.

**1. Section independence.** Structured documents often have well-defined sections that are relatively independent. Use the table of contents or heading structure as the preliminary basis for independence assessment during Phase 1, subject to verification that later sections do not depend on earlier ones for meaning.

**2. Hedging and citation norms.** Academic and technical writing uses disciplined hedging conventions. "We observe," "results suggest," "it appears" are genre conventions, not admissions of genuine uncertainty. Do not over-apply `[STATUS: UNCONFIRMED]` to normally hedged academic language. Reserve it for genuinely unresolved empirical questions or explicitly open problems.

**3. Abstract and conclusion priming.** For academic papers: after Phase 0, read the abstract and conclusion before beginning the Spine pass. These provide a ground truth — a known endpoint against which to calibrate your extraction throughout Phase 1.

**4. Version and edition tracking.** If the document has version numbers, edition markings, or date stamps, record them in the Configuration Preamble and in `log.md`. If multiple versions of the same document are being processed, treat version differences as a potential source of contradictions.

---

## MODULE 12D — Scraped Web Content

Invoke when the source is content scraped from web pages via the bundled `web_scraper.py` CLI tool. Each scraped file contains YAML frontmatter (url, title, domain, scraped_at, word_count) followed by cleaned markdown extracted from the page.

**1. Multiple independent sources.** Scraped content typically consists of multiple independent pages from different URLs. Each page is a self-contained document. This makes scraped content the strongest candidate for Oracle-DAG parallelization — pages from different domains with no cross-references are fully independent.

**2. Metadata-rich frontmatter.** Every scraped file has YAML frontmatter with source URL, title, domain, scrape timestamp, and word count. Use this metadata during Phase 0 to: (a) record the source URL in the Configuration Preamble, (b) assess content freshness via `scraped_at`, (c) identify domain diversity for bias assessment.

**3. Redundancy across pages.** Multiple scraped pages may cover the same topic from different angles. During Phase 2 extraction, detect redundancy early: if page B restates content already extracted from page A, mark it `[REDUNDANT — repeats content from [file_A.md]]` and extract only the delta. Do not double-extract.

**4. Varying extraction quality.** readability-lxml produces clean extraction for article-style pages (blog posts, documentation, news articles) but may produce noisy or incomplete extraction for pages with heavy JavaScript rendering, paywalls, or non-standard layouts. During Phase 1, flag any scraped file where the content appears truncated or corrupted with `[SCRAPER-QUALITY-LOW]` in the spine entry.

**5. Freshness and staleness.** Scraped content has a `scraped_at` timestamp. If the wiki is being updated weeks or months after the initial scrape, consider whether the content may be stale. For time-sensitive data (market stats, regulatory deadlines, version numbers), prefer re-scraping over using cached content.

**6. Domain bias assessment.** During Phase 0, list all unique domains in the scraped content set. If more than 40% of pages come from a single domain, note this as a potential source bias in `log.md` and in the Configuration Preamble. The wiki's master_summary.md should acknowledge the domain distribution.

**7. Oracle-DAG eligibility.** Scraped web pages are the strongest Oracle-DAG candidates in this protocol. Pages from different domains with no cross-references can be processed in parallel subagents. Mark independence assessments as `INDEPENDENT` unless cross-references exist between pages.
