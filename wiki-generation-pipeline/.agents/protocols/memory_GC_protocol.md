# Agentic Memory Eviction: Garbage Collection for Long-Running Agents

## The Problem

A long-running agent's context window accumulates, in order of typical bloat contribution:
1. Raw tool outputs (full file contents, full command stdout/stderr) — often the single largest contributor.
2. Dead-end exploration (hypotheses tried and disproven, files read that turned out irrelevant).
3. Repeated re-reads of the same file/state across many turns.
4. Verbose intermediate reasoning that was useful in the moment but not after the decision was made.

Left unmanaged, this either hits a hard context limit or — more insidiously — dilutes the signal: the agent's attention is spread across mostly-irrelevant history, degrading decision quality well before the hard limit is hit. Garbage collection is the discipline of actively shrinking working context to keep the relevant-information-density high.

## Core Principle: Distinguish "Used Once" From "Referenced Repeatedly"

Before evicting anything, classify it:
- **Transient**: information needed only to make one specific decision, already made (e.g., the full contents of a file read to check one function signature). Safe to evict once the decision is recorded.
- **Load-bearing**: information needed repeatedly across the remaining task (e.g., the overall architecture, a key constraint, the current objective). Must NOT be evicted — must be promoted into a persistent summary instead (see Compression Format below).
- **Stale**: information that was once load-bearing but has since been superseded (e.g., an old version of a plan that's since been revised). Should be actively evicted, not just left to passively age out — stale-but-present context is worse than absent context because it can be mistakenly treated as current.

Garbage collection ≠ deleting old turns chronologically. Chronological truncation (e.g., "drop everything older than N turns") risks silently dropping load-bearing context while keeping irrelevant recent noise. Eviction decisions should be made on the *classification* above, not on recency alone.

## When to Trigger GC

Don't wait for a hard context-limit error. Trigger proactively at natural checkpoints:
- After completing a discrete subtask (a test passes, a file's refactor is confirmed correct) — this is the moment to compress everything that led to that result into a one-line conclusion.
- After a dead end is confirmed (a hypothesis is disproven) — compress the entire investigation into "ruled out: X, because Y" rather than carrying the full exploration transcript forward.
- Periodically by volume, not just by event — e.g., after every N tool calls, scan for raw outputs that have already served their purpose and haven't been referenced since.

## The Eviction Decision Protocol

For each candidate piece of context, ask in order:
1. **Has the conclusion already been extracted from this?** If yes, the raw form (full file dump, full log) is now redundant with its own conclusion — evict the raw form, keep the conclusion.
2. **Will this be needed again in its raw form?** E.g., a file that will be edited again later needs to be re-read fresh at that time anyway (since it may have changed) — there's rarely a reason to keep a stale copy of file contents "just in case." Re-fetch on demand instead of hoarding.
3. **Is this superseded by a later, more accurate version of the same information?** If a plan was revised, the old plan is now noise, not a useful artifact — evict, don't archive in-context.
4. **Is this irreducible?** Some things genuinely can't be compressed further without losing meaning (e.g., an exact error message that's still actively being debugged). Keep these verbatim until they're resolved.

## Compression Format: Promote, Don't Just Delete

Eviction without compression loses information; deletion alone is lossy garbage collection. The correct pattern is **promote-then-evict**: extract a compressed conclusion into a persistent running summary, then evict the raw material that produced it.

Maintain a structured, continuously-updated summary block (conceptually similar to a `handoff.md`, but updated in place rather than written once at handoff time):

```markdown
## Objective
<unchanged unless the task itself is redefined>

## Confirmed Facts
- <file:line> — <fact, stated once, in present tense>

## Ruled Out
- <approach> — <one-line reason, not the full investigation transcript>

## Current Plan
- [x] <completed step, kept only as a checkbox, not its full execution log>
- [ ] <next step>

## Open Threads
- <anything still unresolved, with enough detail to resume it later>
```

Each time something is promoted into this block, the raw material that justified it (the full file read, the full command output, the full reasoning trace) becomes eviction-eligible. The summary block itself should be re-compressed periodically too — e.g., "Confirmed Facts" entries that turn out not to matter for the remaining task can themselves be dropped, not just the raw logs that produced them.

## Concrete Compression Techniques

### Replace full outputs with their verified takeaway
A full `pytest` run's 200-line output, once read, becomes: `tests: 47 passed, 1 failed (test_refresh, AssertionError at auth.py:84)`. The full text served its purpose at read-time; only the structured takeaway needs to persist.

### Replace multi-turn exploration with its conclusion
Five tool calls spent locating which file defines a function become: `target function defined at auth/tokens.py:112`. The search process itself is not load-bearing once the answer is found.

### Collapse repeated re-reads
If the same file has been read 3 times across the session (common when an agent loses track of what it already knows), this is a GC failure signal — the fact should have been promoted to the summary block after the first read, making the 2nd and 3rd reads unnecessary. Treat repeated identical reads as a trigger to check whether something should have already been promoted.

### Use diffs instead of full-state snapshots for iterative edits
When a file is edited multiple times across a session, don't keep accumulating full copies after each edit — keep only the current full state (or none, if it's re-fetchable) plus a log of what changed and why, not redundant full snapshots at every step.

## What Must NEVER Be Evicted (Even Under Pressure)

- The original objective/constraints, even if restated many times — losing this causes silent goal drift, which is worse than running out of context.
- Active, unresolved error messages currently being debugged (see the debugging framework's "freeze and read the full error" step — compressing this prematurely is a direct cause of misdiagnosis).
- Any explicit constraint given by the user/operator (style rules, scope boundaries, irreversible-action permissions). These are cheap to keep and catastrophic to silently lose.
- Unresolved "Conflicts/Overlaps Flagged" or "Needs manual review" items from any subagent/refactor process — these represent known risk that hasn't been closed out; evicting them doesn't resolve the risk, it just hides it.

## Failure Modes to Watch For

| Failure mode | Symptom | Root cause |
|---|---|---|
| Goal drift | Agent starts optimizing for a sub-goal that was never the actual objective | Original objective got compressed away or buried under newer context |
| Re-litigating closed questions | Agent re-investigates something already ruled out | "Ruled out" conclusions weren't promoted before the raw investigation was evicted |
| Confidently wrong due to stale state | Agent acts on a file's old contents | Raw content was kept past its validity instead of being evicted and re-fetched fresh |
| Context thrashing | Agent oscillates between two plans repeatedly | Old plan wasn't actually evicted, just buried — both versions are competing in context |

## Summary Heuristic

If asked "do I need the raw form of this, or just what I concluded from it?" — and the honest answer is "just the conclusion" — evict the raw form immediately and promote the conclusion into the persistent summary block. The exception is genuinely irreducible, still-active material (live error text, current constraints, current objective): keep those verbatim until they resolve.
