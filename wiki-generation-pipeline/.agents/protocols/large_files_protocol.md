# Large File Protocol
**Version:** 3.0 — General-Purpose | Integrated HPSP + Wiki Architecture + Oracle-DAG
**Scope:** Any large file or file set requiring structured extraction, contradiction resolution, and persistent knowledge output
**Supersedes:** Large File Protocol v2.0

---

## SECTION 0 — Configuration Preamble

**Complete this section before any other action. You may not begin Phase 0 without a completed Configuration Preamble written to disk.**

Fill in each field based on what you know before processing begins. If a field is unknown, write `[TO BE DETERMINED IN PHASE 0]` — but you must return and fill it in once determined.

```
## [CONFIG] Processing Session Preamble
Source file path(s): [path(s)]
Source file type: [chat log / structured document / codebase / data file / mixed]
Approximate known size: [if known; exact count determined in Phase 0]
Expected content characteristics: [what pathologies are likely?
  e.g., contradictions, off-topic sections, deprecated content,
  version drift, sequential dependencies, parallel-safe modules]
Downstream use case: [what will the wiki be used to produce?]
Wiki output directory: [choose a name, e.g., source_wiki/ or projectname_wiki/]
File type module(s) to invoke: [from Section 12; select based on source type]
Parallelization pre-assessment: [LIKELY FEASIBLE / LIKELY SEQUENTIAL / UNKNOWN]
  (Final determination happens at Phase 1 Gate after Spine is built)
```

Write this preamble as the first entry in `[wiki_dir]/log.md`. The preamble is an input to every subsequent phase — when in doubt about scope or intent, return to it.

---

## SECTION 1 — Mandatory Preamble

**Why this protocol is non-negotiable.**

This protocol exists because large files cannot be safely processed without a structured plan. Three failure modes make unstructured processing dangerous:

**Failure Mode 1 — Context overload.** A file exceeding what fits in a single context window cannot be read all at once. Attempting to do so produces truncated reads — the agent processes only what fit, silently misses the rest, and generates output as if coverage were complete. This protocol prevents this by requiring explicit coverage tracking and arithmetic line-count reconciliation.

**Failure Mode 2 — Silent exclusion.** When reading large files, an agent may unconsciously skip content it judges as low-value — content that may have been exactly what the downstream process needed. This protocol prevents this with the Accountability Rule (Section 11): every line read must be explicitly accounted for in one of the defined dispositions. There is no valid disposition called silence.

**Failure Mode 3 — Contradiction propagation.** Large files frequently contain internal contradictions: a recommendation made early that was later revised, a position that changed, a deprecated approach that was superseded. An agent that ingests these without tracking them passes contradictions into downstream work, producing incorrect or inconsistent output. This protocol prevents this by requiring all contradictions to be flagged, tracked, and resolved before the wiki is used for any downstream work.

The protocol is followed exactly, in the order specified. No phase may be bypassed. No gate may be passed without meeting all its conditions.

---

## SECTION 2 — The Wiki Architecture

You will not merely summarize the source file. You will build a **structured wiki** from it. The wiki is a persistent, compounding artifact — organized by topic, internally cross-referenced, and maintained as the active reasoning artifact. Once built, all downstream work uses the wiki. You do not re-read the source file once the wiki is complete.

**Three-layer architecture:**

| Layer | Description | Mutability |
|---|---|---|
| Raw source | The source file(s) you are processing | Immutable — read-only throughout |
| The wiki | Structured `.md` files in `[wiki_dir]/` | Writable by you during processing |
| The schema | This protocol | Fixed during processing |

**Required wiki directory structure — all mandatory files must exist on disk before the Phase 4 Gate is passed:**

```
[wiki_dir]/
  log.md             ← Append-only record: all phase starts/completions, chunk completions,
                       Oracle-DAG decisions, queries, corrections, off-topic logs
  index.md           ← Content catalog: all pages listed with one-line summary and category
  spine.md           ← Phase 1 output: one entry per reading chunk
  contradictions.md  ← All flagged conflicts: superseded content, deprecated content,
                       unresolvable issues

  topics/
    [topic_A].md     ← One file per major topic/domain identified in the source
    [topic_B].md
    [additional topic files as content demands]

  master_summary.md  ← Phase 4 output: orientation document for downstream agents
  output_map.md      ← Phase 4 output: maps wiki content to downstream output structure

  [optional]
  dependency_map.json ← Oracle-DAG output: section dependency map (created only if
                         Oracle-DAG is invoked after Phase 1 Gate)
```

**Critical rules for the wiki:**
- Topic file names are determined during Phase 2 based on content — not pre-defined here. Create files as the content demands them.
- `log.md` is strictly append-only. No entry is ever deleted or overwritten.
- `index.md` is updated incrementally — after every topic file write or significant update, not deferred to the end of Phase 2.
- Any wiki content held only in memory or in chat output does not satisfy this protocol. All output must be written to disk. This rule has no exceptions.

---

## SECTION 3 — Content Classification Reference

Every chunk you read will contain content of one or more of these types. Identify the type before extracting. This table is the reference for the Accountability Rule (Section 11).

| Content Type | Description | How to Handle |
|---|---|---|
| **High-relevance** | Directly supports the downstream use case | Extract into `topics/[topic].md` with full fidelity |
| **Low-relevance** | Related but not material to the downstream task | Extract briefly; tag `[LOW-RELEVANCE]` |
| **Off-topic** | Clearly unrelated to subject or downstream task | Log only: `[OFF-TOPIC] Lines X–Y: [one sentence]. Not extracted.` |
| **Contradictory** | Conflicts with content from an earlier part of the source | Extract both positions; flag in `contradictions.md`; apply status tags |
| **Superseded** | A position later explicitly revised by the same source | Mark earlier `[SUPERSEDED]`; mark later `[CURRENT]`; file in `contradictions.md` |
| **Deprecated** | A technical recommendation explicitly replaced | Mark earlier `[DEPRECATED]`; mark replacement `[CURRENT]`; file in `contradictions.md` |
| **Redundant** | Repetition of content already fully extracted | Note in topic page: `[REDUNDANT — Lines X–Y repeat Lines A–B. Not re-extracted.]` |
| **Hedged/Exploratory** | Raised as a possibility, not confirmed or decided | Mark `[STATUS: UNCONFIRMED]`; do not treat as settled |
| **Ambiguous** | Status (current/deprecated/superseded) cannot be determined | Mark `[REQUIRES VERIFICATION]`; file in `contradictions.md` for Phase 3 resolution |

Silence is not a valid disposition. Every line read receives one of the above treatments.

---

## SECTION 4 — Phase 0: Structural Reconnaissance

**Goal:** Understand the source file's size and format before reading any content in detail. Produce a Reading Plan. Do not perform any detailed content extraction in this phase.

**Steps — complete in this order:**

**Step 1:** Retrieve the exact total line count of the source file using a tool call or shell command. Do not estimate. Record this number — it is your coverage target for all subsequent phases.

**Step 2:** Read the first 100–150 lines of the source. Observe:
- What is the file's visible structure? (headings, section markers, function definitions, turn delimiters, data schema, table of contents)
- What format does the file follow? (Consult Section 12 for file-type-specific guidance on what to look for.)
- What topics or domains appear in the opening?

**Step 3:** Read the last 50–100 lines of the source. Observe:
- How does the file end?
- Are there summary sections, terminal markers, or conclusion blocks?
- What topics appear at the close?

**Step 4:** Produce a **Reading Plan** specifying:
- Total line count (exact)
- Chunk size for reading passes (adjust based on file density — denser content warrants smaller chunks)
- Total chunk count (total lines ÷ chunk size, rounded up)
- Source format as observed (delimiter patterns, heading levels, section markers)
- Preliminary topic areas visible from the first/last inspection
- Preliminary parallelization assessment: are there clearly independent sections visible? (Full determination happens after Phase 1 produces the full Spine)

**Step 5:** Write the Reading Plan as the Phase 0 entry in `[wiki_dir]/log.md`:
```
## [PHASE 0] Structural Reconnaissance — COMPLETE
Total line count: [exact number]
Chunk size: [N lines]
Total chunks: [N]
Format observed: [description]
File type module(s) invoked: [Section 12 modules in use]
Preliminary topics: [list]
Preliminary parallelization assessment: [LIKELY FEASIBLE / LIKELY SEQUENTIAL / UNKNOWN]
Status: READING PLAN CONFIRMED
```

**Phase 0 Gate — ALL conditions must be true before proceeding to Phase 1:**
- [ ] Exact total line count is recorded in `log.md`
- [ ] Reading plan is written to `log.md` with chunk size and total chunk count
- [ ] Source format has been observed and recorded
- [ ] `[wiki_dir]/log.md` exists on disk with the Phase 0 entry
- [ ] No detailed content extraction has been performed yet

---

## SECTION 5 — Oracle-DAG Protocol (Conditional)

**Invoke this section ONLY if the Phase 1 Gate authorizes parallelization. Skip it entirely for sequential sources.**

Phase 1 (the Spine Pass) is the Oracle Pass — the sequential full-file scan that produces the dependency map. The Oracle-DAG Protocol uses the Spine to determine whether Phase 2 can be parallelized, and if so, how.

---

### When Oracle-DAG Is and Is Not Applicable

**MANDATORY SEQUENTIAL — Oracle-DAG is mathematically forbidden when:**
- The source is chronologically ordered content: chat logs, conversation transcripts, ledgers, sequential narratives, journals. Understanding entry/turn N requires having processed entries/turns 1 through N-1.
- Sections share global state that is mutated across sections: shared configuration files, shared schema definitions, shared global variables that multiple sections define or modify.
- The source is a monolithic document where later sections depend on earlier ones for meaning (e.g., a proof that builds on theorems established earlier).

**ORACLE-DAG MAY BE INVOKED when:**
- The Spine identifies sections or blocks that are independently intelligible — each section makes sense without reading the others.
- Different sections belong to wholly separate domains with no cross-references (e.g., independent API modules with no shared state; separate chapters covering distinct subjects with no internal citations between them).
- Cross-references between sections, if any, are navigable lookup links rather than semantic dependencies — one section can be fully extracted without needing to have processed the other first.

**Independence may be granted per-section, not all-or-nothing.** It is valid to parallelize sections B, D, and F while processing A, C, and E sequentially, provided the DAG correctly reflects the dependencies and the merge order respects them.

**If any section fails the independence test, that section must be processed sequentially.** Do not grant independence optimistically — grant it only when the Spine confirms it.

---

### Step 1: Dependency Mapping (from the Spine)

Using the independence assessments recorded per chunk in the Spine, generate `[wiki_dir]/dependency_map.json`:

```json
{
  "source_file": "[path]",
  "total_chunks": "N",
  "sections": [
    {
      "section_id": "S1",
      "chunks": [1, 2, 3],
      "depends_on": [],
      "independent": true
    },
    {
      "section_id": "S2",
      "chunks": [4, 5],
      "depends_on": ["S1"],
      "independent": false
    }
  ],
  "parallelizable_groups": [["S1", "S3", "S5"]],
  "sequential_chains": [["S2", "S4", "S6"]]
}
```

For each identified section: list which chunks it covers, list all dependencies, and mark `independent: true` only if confirmed by the Spine.

---

### Step 2: DAG Generation

From the dependency map, generate the directed acyclic graph of Phase 2 extraction tasks:

- **Sequential node:** A section with dependencies — must be processed after its dependencies complete.
- **Parallel node:** A section confirmed independent — can be processed simultaneously with other parallel nodes.
- **Merge point:** Where parallel branches rejoin before a shared dependency or before Phase 3.

Record the DAG in `[wiki_dir]/log.md`:
```
## [ORACLE-DAG] DAG Generated
Sequential chains: [list]
Parallel groups: [list]
Merge order (for Reduce Phase): [list in dependency order]
Status: DAG CONFIRMED
```

---

### Step 3: Subagent Spawning (Parallel Branches)

For each parallel group, spawn a subagent using this boundary-enforcing prompt pattern. Deviation from this pattern is a protocol breach:

> *"You are assigned to extract wiki content from Section [ID], covering lines [X]–[Y] of [source file path]. Write your output ONLY to `[wiki_dir]/topics/[assigned_topic_files]`. Do NOT write to any other file in `[wiki_dir]/`. If you discover content that belongs to a section not assigned to you, do NOT extract it. Log it in your output under the heading `[OUT-OF-SCOPE FLAGS]` with the relevant line numbers and a one-sentence description. Another subagent or sequential pass will handle it. Confine all extraction strictly to your assigned chunks and assigned topic files. Follow the Phase 2 extraction rules defined in Section 7 of the Large File Protocol."*

Each subagent must:
- Produce the same per-chunk spine-to-extraction accountability as a sequential Phase 2 pass
- Append their completed chunk logs to `[wiki_dir]/log.md` upon completing each chunk
- Never modify topic files outside their assigned set
- Write all out-of-scope discoveries to their `[OUT-OF-SCOPE FLAGS]` section

---

### Step 4: Dependency-Ordered Merge (Reduce Phase)

When all parallel subagents complete, merge outputs in the dependency order the DAG specifies:

1. Process foundation sections first (sections with no dependencies)
2. Then process sections that depend on those foundations
3. Before applying any subagent's changes, run a diff against the target file to verify no other subagent has modified it
4. If a diff reveals a conflict: escalate to arbitration (manual review) rather than overwriting
5. If a subagent flagged out-of-scope content: process those flags as a sequential arbitration pass before proceeding to Phase 3

Record the merge completion in `[wiki_dir]/log.md`:
```
## [ORACLE-DAG] Merge Complete
Sections merged: [list in merge order]
Conflicts encountered: [N] (see arbitration entries in log.md)
Out-of-scope flags resolved: [N]
Status: MERGE COMPLETE — Proceeding to Phase 2 Gate
```

After the merge, proceed to the Phase 2 Gate to verify full coverage before Phase 3.

---

## SECTION 6 — Phase 1: Spine Pass (Oracle Pass)

**Goal:** Read the entire source file sequentially, tracking coverage precisely, and produce a structural map of every chunk in `[wiki_dir]/spine.md`. This is simultaneously the structural map needed for the wiki and the Oracle Pass needed for Oracle-DAG. Both uses are served by one sequential scan.

**This phase maps structure only. It does not perform deep extraction. Extraction happens in Phase 2.**

**Reading mechanics:**
- Read in the chunk sizes defined in Phase 0
- Log every completed chunk to `[wiki_dir]/log.md` immediately upon completion — do not batch-log multiple chunks
- If a tool call returns fewer lines than requested: stop, record the shortfall in `log.md`, and re-read the missing lines before logging the chunk as complete. A partial read is not a completed chunk.
- Never skip a chunk based on a judgment that it looks uninformative — read every chunk without exception

**Per-chunk output — one entry per chunk in `[wiki_dir]/spine.md`:**
```
### Chunk [N] — Lines [X]–[Y]
Content type(s) present: [from Section 3 classification reference]
Primary themes: [2–4 bullet points of the major ideas in this chunk]
Flags:
  - [OFF-TOPIC]: contains clearly off-topic material
  - [CONTRADICTION]: appears to conflict with an earlier chunk (note the earlier chunk number)
  - [SUPERSEDED]: a position here may be revised in a later chunk
  - [DEPRECATED]: a technical recommendation here may have been replaced
  - [DENSE]: high-information chunk requiring careful Phase 2 extraction
Independence assessment: [INDEPENDENT / DEPENDS ON CHUNKS X–Y / SEQUENTIAL-ONLY]
```

The `Independence assessment` field on every chunk entry is the input to the Oracle-DAG decision at the Phase 1 Gate.

**Coverage tracking — append to `[wiki_dir]/log.md` after each chunk:**
```
## [PHASE 1] Chunk [N]: Lines [X]–[Y] — COMPLETE
```

**Phase 1 Gate — ALL conditions must be true before proceeding:**
- [ ] Every chunk in the reading plan has a corresponding entry in `[wiki_dir]/spine.md`
- [ ] Every chunk is logged in `[wiki_dir]/log.md` as COMPLETE
- [ ] Sum of all chunk line ranges equals the total line count recorded in Phase 0. Verify arithmetically — not by estimation. If the sum does not match, stop, identify the gap, and re-read before checking this gate again.
- [ ] `[wiki_dir]/spine.md` exists on disk with all chunk entries

**Oracle-DAG decision — recorded in `log.md` immediately after the above conditions are met:**

Review all `Independence assessment` fields in the spine. Apply the criteria from Section 5.

```
## [PHASE 1] Oracle-DAG Decision
Parallelization-eligible sections: [list, or "NONE"]
Sequential-only sections: [list with reason]
Decision: [INVOKE ORACLE-DAG (proceed to Section 5) / SEQUENTIAL PHASE 2 (proceed directly to Section 7)]
Reason: [one sentence]
```

- If Oracle-DAG: proceed to Section 5 before Phase 2
- If sequential: proceed directly to Section 7 (Phase 2)

---

## SECTION 7 — Phase 2: Deep Extraction (Wiki Build)

**Goal:** Process each chunk and extract its content into the structured `[wiki_dir]/topics/` files. This is where the wiki is built.

If Oracle-DAG was invoked: each subagent runs Phase 2 for its assigned section only. All rules in this section apply equally to subagents.

**Reading mechanics:**
- For each chunk: re-read from the source file, or extract from your Phase 1 spine entry if it is sufficiently detailed
- If a chunk was flagged in Phase 1 with `[CONTRADICTION]`, `[SUPERSEDED]`, `[DEPRECATED]`, or `[DENSE]`: re-read from the source before extracting — do not rely on Phase 1 notes alone for flagged chunks

**Mandatory Multi-Layer Analysis before extracting any chunk:**

Before writing a single word of wiki content for a given chunk, resolve all four layers:

1. **What is this chunk saying?** (One sentence, plainly stated)
2. **What domain does it belong to?** (Which topic file should receive this content?)
3. **What is its specificity level?** (High-level concept / specific technical detail / opinion or preference / deprecated claim / exploratory suggestion / off-topic)
4. **What does this connect to?** (Which existing wiki pages does this relate to? Are cross-references needed?)

You may not begin extracting until all four layers are resolved. Proceeding without completing this analysis is a critical failure mode that this protocol exists to prevent.

---

**Extraction rules — apply these in order when writing to topic pages:**

**Rule 1 — High-relevance content.**
Write to `topics/[topic].md`. Write with enough fidelity that a downstream agent reading only the wiki can fully understand and act on the content. Capture the reasoning chain, not just the conclusion — a recommendation without its rationale is half-useful.

**Rule 2 — Cross-references.**
When content in chunk N relates to content already in a wiki page, add a cross-reference on both pages:
```
[Cross-ref: topics/[file].md — [description of related content]]
```
Isolated facts with no connections to related content are a wiki defect. The wiki's value comes from its connections.

**Rule 3 — Superseded and deprecated content.**
```
**[POSITION/RECOMMENDATION: SUPERSEDED]** [earlier position, summarized]
**[POSITION/RECOMMENDATION: CURRENT — supersedes above]** [revised position, summarized]
[Cross-ref: contradictions.md — [entry ID]]
```
Also file in `[wiki_dir]/contradictions.md`:
```
### [C-N] [Brief description]
Earlier: [description] | Source: Lines [X]–[Y]
Later: [description] | Source: Lines [A]–[B]
Resolution status: PENDING
```

**Rule 4 — Off-topic content.**
Do NOT extract into any topic file. Write one line to `[wiki_dir]/log.md` only:
```
[OFF-TOPIC] Lines X–Y: [one sentence description]. Not extracted.
```
This satisfies the Accountability Rule. No further action required for off-topic content.

**Rule 5 — Redundant content.**
Extract the first occurrence fully. For subsequent repetitions, write only this note in the topic page:
```
[REDUNDANT — Lines X–Y repeat content already extracted from Lines A–B. Not re-extracted.]
```
This note must appear in the topic page itself, not only in the log.

**Rule 6 — Hedged or exploratory content.**
Mark with `[STATUS: UNCONFIRMED]`. Do not present in the wiki as a settled decision.

**Rule 7 — Ambiguous content.**
Mark with `[REQUIRES VERIFICATION — Lines X–Y. Issue: [description].]` and file a corresponding entry in `contradictions.md`.

**Rule 8 — Low-relevance content.**
Extract briefly. Tag `[LOW-RELEVANCE]` and include a one-sentence reason (e.g., `[LOW-RELEVANCE — peripheral context; may not be actionable for downstream task]`).

---

**Updating `index.md`:**
After writing or significantly updating any topic page, update `[wiki_dir]/index.md` immediately:
```
| Page | Category | Summary | Last updated (chunk) |
|------|----------|---------|----------------------|
| topics/[name].md | [category] | [one-sentence summary] | Chunk [N] |
```
Do not defer index updates to the end of Phase 2. The index must reflect reality at all times during processing.

**Phase 2 Gate — ALL conditions must be true before proceeding to Phase 3:**
- [ ] Every chunk from Phase 1 has been processed in Phase 2
- [ ] Every chunk's content is explicitly accounted for: extracted, logged as off-topic, noted as redundant, or tagged per Section 3
- [ ] `[wiki_dir]/contradictions.md` contains entries for all flagged contradictions, superseded content, and ambiguous items
- [ ] All `contradictions.md` entries have `Resolution status: PENDING`
- [ ] `[wiki_dir]/index.md` is current and reflects all topic pages
- [ ] No topic page contains `[REQUIRES VERIFICATION]` without a corresponding `contradictions.md` entry
- [ ] (If Oracle-DAG was active) Merge is complete per Section 5, Step 4, and all out-of-scope flags are resolved

---

## SECTION 8 — Phase 3: Cross-Reference Synthesis and Contradiction Resolution

**Goal:** Build the connections between wiki pages, resolve all flagged contradictions, verify the wiki's internal consistency, and ensure no content is orphaned or misrepresented.

**Steps — complete in this order:**

**Step 1: Directory audit.**
Read the full `[wiki_dir]/` directory listing. Read `index.md` in full. You must have a complete picture of what the wiki contains before making changes.

**Step 2: Cross-reference audit.**
For each topic page, check:
- Are there related facts in other topic pages that are not cross-referenced?
- Are there concepts referenced by name on one page that have their own dedicated page but no link?
- Are there claims that appear on only one page with no surrounding context — orphaned facts?

Add all missing cross-references.

**Step 3: Contradiction resolution.**
Read `[wiki_dir]/contradictions.md` in full. For each `Resolution status: PENDING` entry:

**(a) Chronological verification:** The revised position must appear later in the source than the initial position. Later in the source = more authoritative. Check the line references recorded in Phase 2 to confirm chronological order.

**(b) If verified → update `contradictions.md`:**
```
Resolution status: RESOLVED
Later content (Lines A–B) supersedes earlier (Lines X–Y). Current position: [description].
```
Update the topic page to clearly distinguish current from deprecated:
```
~~[deprecated claim]~~ [SUPERSEDED — see contradictions.md C-N]
**Current:** [revised claim] [CONFIRMED CURRENT as of Lines A–B]
```

**(c) If unresolvable from the source alone → mark:**
```
Resolution status: UNRESOLVED — HUMAN CLARIFICATION REQUIRED
Reason: [specific description of why it cannot be resolved from the source alone]
```
Note this in `log.md`. Any downstream output section that touches this content must acknowledge the uncertainty explicitly.

**Step 4: Distribution check.**
No single topic page should contain more than 40% of the total wiki content volume. If one page has grown disproportionately, it likely contains multiple sub-topics that should be separated into their own files. Split if necessary; update `index.md` after splitting.

**Step 5: Gap audit.**
Review the wiki against the downstream use case recorded in the Configuration Preamble. For each domain the downstream task requires:
- Is there a dedicated topic page?
- Is it substantively populated?
- If a domain is sparsely covered: is that because the source had little to say (acceptable — document it in `log.md`) or because content was missed in Phase 2 (not acceptable — return to the relevant chunks and extract)?

**Step 6: Lint check.**
Flag and resolve every issue found against these criteria:
- **Inter-page contradictions:** Subtle inconsistencies between pages not already in `contradictions.md`
- **Stale claims:** Pages describing plans or proposals when later pages confirm they were changed or abandoned
- **Orphan pages:** Pages with no inbound links from other pages or from `index.md`
- **Unlinked concepts:** Important terms mentioned across multiple pages but lacking their own dedicated page
- **Missing cross-references:** Two related pages discussing connected content without linking to each other

Write all lint findings and their resolutions to `[wiki_dir]/log.md`:
```
## [PHASE 3] Lint Check
Issue 1: [description] → Resolution: [description]
[etc.]
No further issues found after [N] checks.
```

**Phase 3 Gate — ALL conditions must be true before proceeding to Phase 4:**
- [ ] All cross-references are in place; no orphan pages remain
- [ ] Every `contradictions.md` entry has status RESOLVED or UNRESOLVED — no PENDING entries remain
- [ ] Distribution check passed: no topic page exceeds 40% of total wiki content volume
- [ ] Gap audit complete: sparse coverage is documented; missed Phase 2 content has been extracted
- [ ] Lint check passed: all issues found are resolved or explicitly noted
- [ ] `log.md` Phase 3 completion entry is written and on disk

---

## SECTION 9 — Phase 4: Output Mapping and Master Synthesis

**Goal:** Map the completed wiki to the structure of the downstream output. Produce the master summary. After this phase, the source file is closed — all further work uses the wiki only.

**Step 1: Define the downstream output structure.**
Based on the downstream use case in the Configuration Preamble, define the complete list of sections or components the downstream output will contain. This list becomes the structure of `[wiki_dir]/output_map.md`. If the downstream use case is known ahead of time, this structure may already be defined — verify it against what the wiki actually contains and adjust if necessary.

**Step 2: Map each output section.**
For each section of the downstream output, produce an entry in `[wiki_dir]/output_map.md`:
```
## Output Section: [Section Name]

Primary wiki sources:
- topics/[file].md — [specific subsection or content description]
- topics/[file].md — [specific subsection or content description]

Key content to include:
- [Summary specific enough to be actionable by the downstream agent]

Contradictions/caveats (content to avoid or qualify):
- [Any superseded content this section must not present as current — reference contradictions.md entry]

Unresolved issues affecting this section:
- [Any UNRESOLVED entries from contradictions.md that require human clarification]

Coverage confidence: [HIGH / MEDIUM / LOW — with reason if not HIGH]
```

**Step 3: Coverage check.**
Every wiki page must appear in at least one output section entry in `output_map.md`. If a page has no mapping:
- It belongs to a section not yet defined → define the section and add it
- It is genuinely not relevant to the downstream output → log as `[NOT MAPPED — reason: [description]]` in `log.md`

No wiki page may be silently unmapped.

**Step 4: Write `[wiki_dir]/master_summary.md`.**
The master summary is the first document any downstream agent will read. It must:
- Give a complete, clear overview of the source material as understood from the wiki
- State which domains are well-documented in the wiki and which are sparse or uncertain
- List all unresolved contradictions that require human clarification, with a brief description of each
- Point explicitly to `output_map.md` for the mapping of wiki content to output sections
- Point explicitly to the relevant `topics/` files for domain detail
- Not reproduce the full content of the wiki — it orients the reader to the wiki, it does not replace it

**Step 5: Phase 4 log entry.**
```
## [PHASE 4] Output Mapping and Master Synthesis — COMPLETE
Output sections defined: [N]
Wiki pages mapped to output sections: [N of N total]
Wiki pages not mapped (logged as not relevant): [N]
Unresolved issues requiring human clarification: [N] (in contradictions.md and master_summary.md)
Files completed this phase: output_map.md, master_summary.md
Status: COMPLETE — Wiki is ready for downstream use
```

**Phase 4 Gate — ALL conditions must be true before the wiki is considered complete:**
- [ ] `[wiki_dir]/output_map.md` exists on disk and covers all output sections
- [ ] `[wiki_dir]/master_summary.md` exists on disk and is complete
- [ ] All wiki pages have a mapping status (mapped to a section, or logged as not relevant)
- [ ] `log.md` Phase 4 entry is written and on disk
- [ ] The source file(s) have not been modified
- [ ] No wiki file contains an open `[REQUIRES VERIFICATION]` or `[PENDING]` marker — all unresolved items have been escalated to UNRESOLVED status with human clarification noted

**After Phase 4 is complete: you do not read the source file again. All subsequent reasoning uses the wiki.**

---

## SECTION 10 — The Query Protocol (Using the Wiki After It Is Built)

When you need information from the source material after Phase 4, follow this sequence. Do not go directly to the source file before consulting the wiki.

1. Read `[wiki_dir]/master_summary.md` first for full orientation
2. Consult `[wiki_dir]/output_map.md` to identify which wiki pages are relevant to your current task
3. Read the relevant `topics/` pages
4. If you encounter a gap — something needed that is not in the wiki — check in this order before returning to the source:
   - Is it in a different topic page not yet consulted?
   - Is it in `contradictions.md`?
   - Is it logged as `[UNRESOLVED]`?
5. If the wiki genuinely lacks the information after checking all pages: return to the source file, extract only the specific section needed, integrate the extraction into the appropriate topic page, update `index.md`, and log the extraction in `log.md` before proceeding

**Log every query in `[wiki_dir]/log.md`:**
```
## [QUERY] [Brief description of what was needed]
Pages consulted: [list]
Result: [FOUND in topics/file.md] / [NOT FOUND — returned to source, extracted, integrated]
```

Valuable analyses and connections discovered during the output-building phase may be filed back into the wiki as new topic pages. The wiki is a compounding artifact — insights derived from it enrich it for all subsequent use.

---

## SECTION 11 — The Accountability Rule (Full Coverage Mandate)

No content from the source file may be silently discarded. Every line read must be accounted for in one of the following dispositions:

| Disposition | Where recorded | Tag |
|---|---|---|
| Extracted as high-relevance content | In `topics/[topic].md` | (no tag required) |
| Extracted as low-relevance content | In `topics/[topic].md` | `[LOW-RELEVANCE]` |
| Off-topic | One-line entry in `log.md` | `[OFF-TOPIC]` |
| Redundant | Note in topic page | `[REDUNDANT]` |
| Superseded (earlier position) | Topic page + `contradictions.md` | `[SUPERSEDED]` |
| Deprecated (earlier recommendation) | Topic page + `contradictions.md` | `[DEPRECATED]` |
| Hedged or unconfirmed | Topic page | `[STATUS: UNCONFIRMED]` |
| Ambiguous (status unclear) | Topic page + `contradictions.md` | `[REQUIRES VERIFICATION]` |
| Unresolvable contradiction | `contradictions.md` | `[UNRESOLVED]` |
| Not mapped to output | `log.md` | `[NOT MAPPED]` |

**"Accounted for" does not require that all content be extracted as wiki text.** Off-topic content logged with one line has been accounted for. What the Accountability Rule prohibits is silence: dropping content without any record of the decision to do so.

Any wiki file that contains content not present in the source, or that omits source content without a corresponding tag or log entry, is invalid. Invalid wiki files must be corrected before the wiki is used for any downstream output.

---

## SECTION 12 — File Type Modules

Select the module(s) matching the source file's type as identified in the Configuration Preamble. Apply the relevant guidance throughout all phases. Multiple modules may apply simultaneously.

---

### MODULE 12A — Chat-Log Sources

Invoke when the source is a conversation transcript (human-AI, human-human, or multi-party chat log).

**1. Context dependency.** A statement in turn N may only make sense in light of turn N-1. Never extract a claim without absorbing the context of the immediately preceding turn. Capture enough context in the wiki that the reasoning chain is recoverable — not just the conclusion.

**2. Question vs. answer.** The questioner's turns provide context; the answerer's turns are the primary extraction target. Capture what question an answer is responding to. An extracted answer without its motivating question may be unusable.

**3. Hedged language.** Track whether a recommendation was confirmed in a subsequent turn or merely floated as a possibility. If not confirmed: mark `[STATUS: UNCONFIRMED]`. Do not treat exploratory suggestions as settled decisions.

**4. Turn delimiter consistency.** Record the exact turn delimiter format during Phase 0. Apply it consistently throughout all reading phases. If the delimiter format changes partway through the file (common in exported chat logs), note this in `log.md` and update parsing accordingly.

**5. Intra-turn revisions.** If a speaker revises themselves within a single turn (e.g., "Actually, let me reconsider..."), the revision supersedes the earlier statement within that turn. Note inline: `[Self-revised within this turn — earlier: [X]; revised: [Y]; revised is operative]`. This is distinct from inter-turn contradictions (which are handled via `contradictions.md`).

**6. Speaker or version differences.** If the log spans multiple versions of an AI system, multiple participants, or multiple sessions with different configurations, record this in extraction notes. Different versions or participants may have given conflicting advice — a common source of genuine contradictions.

**7. Mandatory sequential processing.** Chat logs are chronologically ordered. Oracle-DAG parallelization is mathematically forbidden for chat-log sources. All chunk independence assessments in Phase 1 must be marked `SEQUENTIAL-ONLY`. Do not override this.

---

### MODULE 12B — Codebase Sources

Invoke when the source is a software codebase, script file, or collection of code files.

**1. Import and dependency mapping.** During Phase 1, pay particular attention to `import`, `require`, `include`, or equivalent dependency declarations. A file that imports another cannot be fully understood without that dependency. Record all import dependencies in the spine entry for each chunk.

**2. Global state identification.** Identify all shared global variables, shared configuration files, shared schema definitions, and shared constants. Any section that reads or modifies shared global state cannot be safely parallelized with other sections that do the same. Mark these `SEQUENTIAL-ONLY` in the independence assessment.

**3. Oracle-DAG primary use case.** Codebase sources are the primary use case for Oracle-DAG. Modules with no shared state and no import dependencies between them are strong parallelization candidates. However, do not declare independence until the Spine confirms it — import maps often reveal non-obvious dependencies.

**4. Logic branching.** When extracting code-related content, capture error handling, edge cases, and configuration details — not just the happy path. Critical logic frequently lives in exception handling and edge conditions.

**5. Changelog maintenance.** When processing a codebase that will be modified (not merely read), maintain a running `CHANGES.md` in `[wiki_dir]/` so the evolution of the project is traceable.

---

### MODULE 12C — Structured Document Sources

Invoke when the source is an academic paper, technical report, PDF, book, specification, or similar document with explicit section structure.

**1. Section independence.** Structured documents often have well-defined sections that are relatively independent. Use the table of contents or heading structure as the preliminary basis for independence assessment during Phase 1, subject to verification that later sections do not depend on earlier ones for meaning.

**2. Hedging and citation norms.** Academic and technical writing uses disciplined hedging conventions. "We observe," "results suggest," "it appears" are genre conventions, not admissions of genuine uncertainty. Do not over-apply `[STATUS: UNCONFIRMED]` to normally hedged academic language. Reserve it for genuinely unresolved empirical questions or explicitly open problems.

**3. Abstract and conclusion priming.** For academic papers: after Phase 0, read the abstract and conclusion before beginning the Spine pass. These provide a ground truth — a known endpoint against which to calibrate your extraction throughout Phase 1.

**4. Version and edition tracking.** If the document has version numbers, edition markings, or date stamps, record them in the Configuration Preamble and in `log.md`. If multiple versions of the same document are being processed, treat version differences as a potential source of contradictions.

---

## SECTION 13 — Checkpoint Reference

All checkpoints must be completed in the order listed. No checkpoint may be bypassed.

| Checkpoint | Phase | Verification method |
|---|---|---|
| Configuration Preamble recorded | Pre-Phase 0 | Check `log.md` for preamble entry |
| Exact total line count recorded | Phase 0 | Check `log.md` Phase 0 entry |
| Reading plan written | Phase 0 | Check `log.md` for chunk size and count |
| Source format identified | Phase 0 | Check `log.md` Phase 0 entry |
| Phase 0 Gate passed | Phase 0 | All Phase 0 Gate checkboxes confirmed |
| Every chunk read | Phase 1 | `log.md` lists every chunk as COMPLETE |
| Spine complete | Phase 1 | `spine.md` has entry for every chunk |
| Line count arithmetically reconciled | Phase 1 | Sum of chunk ranges = total line count |
| Oracle-DAG decision recorded | Phase 1 | `log.md` Oracle-DAG decision entry present |
| Phase 1 Gate passed | Phase 1 | All Phase 1 Gate checkboxes confirmed |
| *(If Oracle-DAG)* Dependency map created | Oracle-DAG | `dependency_map.json` exists on disk |
| *(If Oracle-DAG)* DAG generated and recorded | Oracle-DAG | `log.md` DAG entry present |
| *(If Oracle-DAG)* Subagents use boundary-enforcing prompts | Oracle-DAG | Prompts match Section 5 Step 3 pattern |
| *(If Oracle-DAG)* Merge complete in dependency order | Oracle-DAG | `log.md` merge entry present |
| All chunks processed for extraction | Phase 2 | Every Phase 1 chunk has Phase 2 disposition |
| Topic pages written | Phase 2 | `topics/` directory populated |
| All contradictions logged | Phase 2 | All flagged items in `contradictions.md` as PENDING |
| `index.md` current | Phase 2 | Index reflects all topic pages |
| Phase 2 Gate passed | Phase 2 | All Phase 2 Gate checkboxes confirmed |
| All cross-references added | Phase 3 | No orphan pages; all links verified |
| All contradictions resolved or escalated | Phase 3 | No PENDING entries in `contradictions.md` |
| Distribution check passed | Phase 3 | No topic page exceeds 40% of total wiki content |
| Gap audit complete | Phase 3 | Sparse coverage documented; misses corrected |
| Lint check passed | Phase 3 | All lint issues resolved or noted |
| Phase 3 Gate passed | Phase 3 | All Phase 3 Gate checkboxes confirmed |
| Output map complete | Phase 4 | `output_map.md` covers all output sections |
| All wiki pages have mapping status | Phase 4 | Every page mapped or logged as not relevant |
| Master summary written | Phase 4 | `master_summary.md` exists and is complete |
| Phase 4 Gate passed | Phase 4 | All Phase 4 Gate checkboxes confirmed |

---

## SECTION 14 — Error Recovery

**If a Phase Gate fails:** Identify the specific failing condition. Do not proceed past the gate. Fix the condition. Recheck only that gate — do not re-run preceding phases unless the failing condition requires it.

**If a chunk was missed during Phase 1:** Re-read the missed chunk. Add its spine entry to `spine.md`. Process it through Phase 2. Update all affected topic pages and `index.md`. Log the recovery in `log.md`. Recheck Phase 1 and Phase 2 Gates before proceeding.

**If the line count does not reconcile at the Phase 1 Gate:** Stop all processing. Re-read from the beginning of the unreconciled region. Do not reconcile by estimating. The reconciliation must be arithmetically exact.

**If a contradiction cannot be resolved during Phase 3:** Mark `[UNRESOLVED — HUMAN CLARIFICATION REQUIRED]` in `contradictions.md`. Note it explicitly in `master_summary.md`. Do not guess. The downstream output section that touches this content must either defer to the user for resolution or acknowledge the uncertainty explicitly in the final output.

**If the file is larger than expected:** Do not compress or skip phases. Add chunks and processing passes as needed. A complete wiki is required regardless of final file size. There is no early-exit option based on file size.

**If Oracle-DAG subagent boundaries are breached:** Do not merge the offending subagent's output. Escalate to arbitration. Re-extract the out-of-scope content in a sequential pass. Log the breach, the arbitration, and the resolution in `log.md`.

**If a topic page is found invalid (content missing without accounting):** Identify what is missing by comparing the spine entries for the relevant chunks against the topic page content. Re-extract the missing content. Update `index.md` and `contradictions.md` as relevant. Log the correction. Do not proceed to downstream work until all affected pages are valid.

---

## SECTION 15 — Immutability Rule

The source file(s) are raw sources. They must never be:
- Modified
- Deleted
- Overwritten
- Used as a scratch space or output target

They are read-only throughout this entire protocol. All work product is written to `[wiki_dir]/`. This rule is absolute and has no exceptions.

---

## SECTION 16 — Pre-Handoff Checklist

Before the wiki is passed to any downstream agent or process, confirm every item on this checklist. Do not hand off a wiki with any unchecked item.

- [ ] `[wiki_dir]/index.md` exists on disk and is current
- [ ] `[wiki_dir]/log.md` is on disk with entries for all phases and all chunk completions
- [ ] `[wiki_dir]/spine.md` is on disk with an entry for every reading chunk
- [ ] `[wiki_dir]/contradictions.md` is on disk and every entry has status RESOLVED or UNRESOLVED — no PENDING entries remain
- [ ] All `[wiki_dir]/topics/` files are on disk and populated
- [ ] `[wiki_dir]/output_map.md` is on disk and covers all output sections
- [ ] `[wiki_dir]/master_summary.md` is on disk and is complete
- [ ] No wiki page contains an open `[REQUIRES VERIFICATION]` or `[STATUS: PENDING]` marker
- [ ] All unresolved contradictions are listed explicitly in `master_summary.md`
- [ ] The source file(s) are unmodified — verify by checking that size/line count matches what was recorded in Phase 0
- [ ] No wiki page contains content that does not originate from the source file(s) — no fabrication
- [ ] *(If Oracle-DAG was used)* Merge is confirmed complete; no out-of-scope flags remain open

**Only when every item on this checklist is confirmed is the wiki ready for downstream use.**

---

*This protocol governs the processing of any large source file or file set. Any deviation — skipping a phase, bypassing a gate, omitting a log entry, failing to write artifacts to disk, or beginning processing without a completed Configuration Preamble — constitutes a breach. A breached protocol does not protect against the failure modes it was designed to prevent. Follow it exactly.*
