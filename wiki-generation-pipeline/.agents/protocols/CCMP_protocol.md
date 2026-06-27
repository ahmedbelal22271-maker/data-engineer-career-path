# Component Co-Migration Protocol (CCMP)

**Status:** Active
**Location:** /protocols/CCMP_protocol.md
**Governs:** HTML block migration between files, component duplication, and dependency extraction.

## Trigger Condition
Whenever an agent cuts, copies, pastes, duplicates, or restores any HTML block from a backup or external source into a live file.

## Rules

### 1. Structural Dependency Extraction
When moving an HTML component, you must also migrate its dependencies:
1. Extract every CSS class name and element ID present in the migrated HTML block by scanning all `class="..."` and `id="..."` attributes. Build an explicit token list before proceeding.
2. Search the source file's `<style>` blocks (or external stylesheets) for every token in that list. Extract every matching CSS rule found.
3. Check the destination file's `<style>` blocks for those same rules. If a rule is absent, inject it. If it already exists, do not duplicate it.

### 2. Logic Migration (Delegation to ISIP)
Perform the same search in `<script>` blocks for any JS referencing the migrated IDs or classes by string. Migrate any missing JS logic using Isolated Script Injection Protocol (ISIP) rules.

### 3. Visual State Preservation
The agent must never strip existing inline styles, structural classes, or CSS properties from an element during a migration without explicit user authorization in that turn. Any authorized removal must be logged to the sync log.

### 4. Environment-Aware Compute Routing (Script Language Optimization)
For large-scale CCMP migrations that require scripting to parse HTML/CSS safely:
- The agent must **go with the flow** of the host environment.
- **Inside Antigravity:** Default strictly to Python for all deterministic scripts (e.g., using `BeautifulSoup`).
- **Inside Google AI Studio:** Default strictly to Node.js (e.g., using `cheerio` or `JSDOM`).
- Avoid cross-polluting environments with non-native runtimes.

## Failure Condition
Migrating HTML without completing the Structural Dependency Extraction is a strict CCMP BREACH.

## Interactions
- **ISIP:** CCMP delegates JS migration tasks to ISIP.
- **SFBP:** CCMP does not replace SFBP. A backup must still be created before any file is modified.
