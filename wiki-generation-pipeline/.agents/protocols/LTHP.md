# PROTOCOL IMPLEMENTATION PROMPT — HTML Project
## Target: AI Coding Agent working on this project's HTML codebase

## 1. Objective
Design, codify, and implement a persistent editing protocol named the
**"Last-Touch Highlight Protocol" (LTHP)** for all HTML file edits in this
project. The name distinguishes it from any other diffing, versioning, or
styling protocols already in use — LTHP refers specifically to marking
whichever block was most recently touched (added or modified), and only that
block. This protocol must be written into the project's `AGENTS.md` file (and
any other core-instructions file the agent maintains) so it is automatically
followed on every future edit — not just this one.

## 2. Protocol Rules (must be implemented exactly as specified)

1. **On every edit that adds new content OR modifies existing content** in any
   HTML file in the project:
   - Wrap or tag the affected block(s) — whether newly added or an existing
     block that was changed/updated — with a dedicated CSS class, e.g.
     `class="lthp-highlight"`.
   - Define `.lthp-highlight` using the exact theme-safe CSS pattern:
```css
/* Base highlight rule for standard components (e.g., .card) */
.lthp-highlight {
  box-shadow: inset 0 0 0 2px rgba(234, 179, 8, 0.9);
  background: rgba(234, 179, 8, 0.12);
  border-radius: 4px;
  transition: background 0.3s ease;
}

/* Compound override for .insight-box components.
   Required because insight-boxes use border-left for their thematic color.
   This override ensures the yellow highlight replaces the thematic border. */
.insight-box.lthp-highlight {
  background: rgba(234, 179, 8, 0.12);
  border-left-color: rgba(234, 179, 8, 0.9);
  box-shadow: inset 0 0 0 2px rgba(234, 179, 8, 0.9);
}
```

     in the project's shared stylesheet (or a `<style>` block if no external
     stylesheet exists). Choose a single consistent yellow shade not used
     elsewhere in the project's palette, and do not change it between edits.
   - Apply this class only to the block(s) touched in *that specific edit* —
     never to blocks that were not added or modified in the current edit.


## Enforcement Mechanism

Layer 1 (Prevention): The CCMP Standard Injection Template includes
the lthp-highlight class on all text/data elements by default.
Correct highlight application is a property of a valid injected
block, not a post-step.

Layer 2 (Detection): After every injection, lthp_audit.py (Usage:
`python lthp_audit.py <session-id> <html_file> <sync_log>`) must be
run before the injection is logged as complete. The script checks
every element listed in the current session's [LTHP-MANIFEST] entry
in GLOBAL_HUB_SYNC_LOG.md for the presence of lthp-highlight. If
any element is missing the class, the script prints the violating
IDs and exits sys.exit(1). A missing manifest is treated as a
failure, not a clean state.

Fallback: Layer 1 failure is caught by Layer 2. Layer 2 has no
further fallback — a sys.exit(1) requires human review before
the injection is considered complete.

Deprecated path: Applying LTHP highlights manually as a remembered
post-step, without running lthp_audit.py, is no longer a valid
execution path and constitutes an LTHP BREACH.

2. **On the next subsequent edit within the same file:**
   - Remove the `lthp-highlight` class (and any inline highlight styling) from
     whatever block(s) carried it previously.
   - The de-highlighted block must return to a fully normal state — no
     residual styling, no marker comments, no special attributes added by the
     protocol.
   - If that block already had its own pre-existing formatting/classes before
     it was highlighted, that original formatting must remain untouched and intact.
   - Generation tracking is per-file, not global. Editing `dashboard.html` does not require revisiting `index.html` to strip its highlight. Each file independently carries at most one active highlighted generation.

3. **Behavioral analogy:** This mirrors how a git diff highlights only the
   lines changed in the latest commit for that specific file — once the next commit lands, the prior
   diff highlighting disappears and the code is just code again, regardless of
   whether that prior change was an addition or a modification.

## 3. Required Deliverables
1. Add a clearly titled section (`## Last-Touch Highlight Protocol (LTHP)`) to
   `AGENTS.md` describing the rules in Section 2 verbatim or in equivalent
   precise language.
2. If a separate core-instructions file exists for this agent, mirror the same
   section there.
3. Implement the CSS class and styling in the appropriate stylesheet location.
4. Apply the protocol to the very next HTML edit you make — whether an
   addition or a modification — as a working demonstration that the protocol
   is active.
5. Do not narrate or explain that you are "now following this protocol" in
   any user-facing output — it should operate silently as standard practice.

## 4. Out of Scope

> LTHP highlights must only be applied to text elements or data rows
> (e.g., `<p>`, `<li>`, `<tr>`, `<td>`, `<h2>`–`<h6>`).
> LTHP must never be applied to structural layout containers including
> but not limited to: `<section>`, `<div class="...wrapper...">`,
> `<main>`, `<table>`, or any element whose primary role is layout
> rather than content display. Applying LTHP to a layout container is
> an LTHP BREACH.

- Do not apply highlighting to edits in non-HTML files.
- Do not retroactively highlight content from edits made before this protocol
  was implemented.
- Do not use inline `style` attributes if a shared stylesheet is available —
  prefer the CSS class method for maintainability.

**Amendment A — §4 Negative Constraint:**
Add explicitly: structural tags (`<h2>`, `<section>`, `<header>`, `<footer>`, `<nav>`, `<article>`, `<aside>`) must NEVER receive `class="lthp-highlight"`. Only content-bearing component wrappers are valid highlight targets.

**Amendment B — §4 Positive Granularity:**
Define the valid highlight target as the "outermost content-bearing component" (e.g. `.card`, `.panel`, `.feature-block`). Highlighting every individual `<p>` or `<h3>` inside a component is a BREACH.

**Expanded Positive Granularity Definition:**
The valid and only target for `class="lthp-highlight"` is the outermost content-bearing component wrapper (e.g. `.card`, `.panel`, `.feature-block`). Applying `lthp-highlight` to any tag nested inside a component wrapper — including `<p>`, `<h3>`, `<span>`, `<li>` — is a BREACH. One highlight class per edited component, on the wrapper only.

Highlight granularity targets are strictly limited to text-bearing and data-bearing elements (e.g., result blocks, content cards, data rows). Application to structural layout shells (<main>, <section>, <div> wrappers that contain no direct text or data) is prohibited and constitutes a BREACH. When in doubt, apply highlighting to the innermost content-bearing element, not its container.

## 5. Ambiguity Clause
If anything in this prompt is unclear — including file locations, naming
conventions, existing stylesheet structure, or how "block" should be scoped
(e.g., single element vs. whole section, or how to handle partial edits within
a larger block) — stop and ask one precise question before proceeding. Do not
guess or assume.
