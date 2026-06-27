# Instruction File Management Protocol (IFMP)

---

## Scope

This protocol governs every interaction the agent has with its own instruction files:
`AGENTS.md`, `L1_core_directives.md`, `L2_formatting.md`, `L3_datalab_sdk.md`,
`L4_session_overrides.md`, `L5_lessons_learned_log.md`.

These files are the agent's brain. They are never touched carelessly, never overwritten blindly,
and never modified without explicit user authorization. This protocol defines exactly when, how,
and in what order the agent may read or write these files.

---

## Rule 1 — Read Manually Before Any Write Operation

Before appending, modifying, or even proposing a change to any instruction file, the agent must
read that file in full using its own reading capability — not a script. A full read satisfies "before write" only if no other write to ANY instruction file has occurred since that read. Any intervening write invalidates it — re-read required.

Scripts have no judgment. They cannot tell whether a proposed append contradicts an existing
directive, duplicates content already present, or belongs in a different file entirely. Only the
agent, reading the file critically with full comprehension, can make that determination.

**The agent must be able to answer these questions before touching any instruction file:**
- What is the current structure of this file?
- What directives already exist, and what do they cover?
- Does the proposed addition conflict with, duplicate, or contradict anything already written?
- Is this the correct file for this addition, or does it belong elsewhere in the hierarchy?

If the agent cannot answer all four questions confidently, it must re-read the file. It does not
proceed until it can.

---

## Rule 2 — Backup Before Every Write (Sliding Window System)

Before writing to any instruction file, without exception, execute this sequence:

**Step 1 — Rotate the window.**
The `/backups/original/` directory holds a maximum of 3 versioned backups per file, named with a version
suffix: `_v1` (oldest), `_v2`, `_v3` (most recent). Before creating a new backup:
- Rename `_v2` → `_v1` (dropping the previous `_v1` permanently)
- Rename `_v3` → `_v2`
- The slot `_v3` is now free for the new backup

If fewer than 3 backups exist yet, simply add the next version without rotating.

**Step 2 — Write the new backup.**
Copy the current file into `/backups/original/` as `_v3`. Example:
`/backups/original/AGENTS_v3.md`, `/backups/original/L1_core_directives_v3.md`

**Step 3 — Confirm the backup.**
Verify the new `_v3` file exists and is readable before proceeding with any write.

**Step 4 — Perform the write operation.**

**Step 5 — Byte-Size Heuristic check.**
Compare the modified file against the `_v3` backup just created:
- If the modified file is smaller in lines or bytes, the automatic-failure-on-shrink check is skipped ONLY IF the user has explicitly authorized a deletion or rule removal in the same turn. Log the authorized exception to GLOBAL_HUB_SYNC_LOG.md instead of triggering rollback.
- Unauthorized shrinkage still fails automatically: restore from `_v3` immediately and investigate before retrying.
- `_v1` and `_v2` remain untouched as additional fallback layers.

**There are no exceptions to this overall sequence.** A write that skips any step is unauthorized,
regardless of how minor the change appears.

---

## Rule 2.1 — Mandatory Pre-Write IFMP Audit (The Mechanical Gate)
Before invoking ANY file-modification method targeting a Gated File (defined explicitly as ANY file residing within `/instructions/` or `/protocols/`), you MUST mechanically verify that the required backup succeeded and the pre-write file state was successfully captured. This rule applies universally to named file-writing tools (e.g., `write_to_file`, `replace_file_content`, `multi_replace_file_content`) AND direct shell/terminal commands (e.g., `Set-Content`, `Add-Content`, `Out-File`, shell redirection, `Copy-Item`).

1. **Execution Requirement:** You must execute `python scripts/ifmp_audit.py <filepath>`.
2. **Verification Gate:** You are authorized to proceed with the modifying operation **if and only if** the script's console output returns `PASS: Backup state verified`.
3. **Failure State:** If the script returns `FAIL` (due to hash mismatch, missing log entry, or missing backup), you are strictly prohibited from writing to the live file. You must immediately re-run the backup script (`backup_sliding_window.py`), then re-run `ifmp_audit.py` to achieve a verified `PASS` before any write is permitted.
4. **Deletion Coverage:** Deletion operations (Remove-Item, del, rm, or equivalent) targeting any gated file are subject to the same gate sequence as writes. No gated file may be deleted without an explicit gate PASS recorded this session. Deletion of a gated file's backup copies is governed by the sliding-window rotation rules in backup_sliding_window.py and does not require a separate gate.
5. **No Self-Attestation:** Relying on memory, assumed state, or conversational claims without the literal `PASS` console output from `ifmp_audit.py` present in your immediate operational context is a strict IFMP BREACH.
6. **Pre-Write Checklist:** Before any write proceeds, confirm the backup file physically exists at /backups/original/[filename]_v3. If absent, halt and report — do not proceed.
7. **Append-Write Backup Mandate:** Non-destructive (append-only) writes are subject to the same mandatory sliding-window backup sequence as destructive writes. Append-only status does not exempt a file from pre-write backup.

---

## Rule 3 — Append, Never Replace

When adding new instructions to an existing file:

- Identify the exact location in the file where the new content logically belongs.
- Append or insert at that location only. Do not restructure, reorder, or rewrite surrounding content.
- Never delete an existing directive unless the user has explicitly instructed its removal and
  stated why.
- If a new instruction appears to contradict an existing one, do not silently overwrite the old
  one. Surface the conflict to the user and ask which takes precedence before writing anything.

---

## Rule 4 — Correct File, Every Time

The five priority files have defined scopes. Every new instruction belongs in exactly one of them:

| File | Scope |
|------|-------|
| `L1_core_directives.md` | Absolute fail-safes, safety mandates, authorization rules |
| `L2_formatting.md` | Large-scale execution, parsing, chunking, file handling at scale |
| `L3_datalab_sdk.md` | SDK-specific or tool-specific integrations (currently cleared) |
| `L4_session_overrides.md` | Workflow alignment, opinion evolution, framework assumptions |
| `L5_lessons_learned_log.md` | UI/presentation rules, visual standards, anti-dump mandates |
| `AGENTS.md` | Condensed master index only — summaries and cross-references, not full rules |

Before writing, the agent states which file it is writing to and why. If the instruction spans
multiple files, it is split accordingly — one clean addition per file.

**Never create new hierarchy files (L6, L7, etc.).** If new content does not fit any existing
file cleanly, that is a signal the content needs to be refined, not that a new file is needed.

---

## Rule 5 — When Scripts Are and Are Not Appropriate

Scripts are powerful tools for the right jobs. They are the wrong tool for instruction file management.

**Use a script when:**
- Extracting raw text from a large file for the agent to then read and reason over
- Performing byte-count or line-count comparisons for the Byte-Size Heuristic
- Automating a backup copy operation

**Never use a script when:**
- Deciding what content to append or where it belongs
- Auto-injecting generated content into `AGENTS.md` or any `L1`–`L5` file
- Making any judgment call about instruction file structure or content

A script that injects content the agent does not fully understand is strictly prohibited.
The agent is responsible for every word written into its instruction files. If a script wrote it,
the agent still owns it — and ignorance of what the script injected is not an excuse.

---

## Rule 6 — AGENTS.md Is a Condensed Index, Not a Dump

`AGENTS.md` is the master entry point the agent reads at the start of every session. Its value
comes from being short, clear, and authoritative. Every line in it must earn its place.

When appending to `AGENTS.md`:
- Write in the most concise form possible. If a rule requires more than two sentences to express,
  it belongs in an `L1`–`L5` file with a one-line reference in `AGENTS.md`.
- Match the existing numbered-directive style exactly.
- Place the addition under the correct priority group.
- Never add prose, explanations, or examples to `AGENTS.md` directly. Those go in the `L` files.

---

## Rule 7 — Explicit Authorization Is Non-Negotiable

The presence of an instruction file in the working directory grants zero permission to modify it.

The agent may only write to an instruction file when the user has explicitly stated, in the
current session, that the write is authorized. Implicit authorization does not exist. Prior
session authorization does not carry over.

When in doubt, the agent asks. It does not assume.

---

## Integration With SEIUP

This protocol works in direct coordination with the Self-Evaluation & Instruction Update Protocol
(SEIUP). SEIUP identifies what needs to be updated. IFMP governs how that update is physically
executed. Neither protocol overrides the other. Both must be followed in sequence:

SEIUP Gate 6 (user approval) → IFMP Rule 2 (backup) → IFMP Rule 1 (read) → IFMP Rule 3 (append).

---

## Rule 8 — Mid-Sequence Restoration Logging

Any restoration of an instruction file from backup during an active write sequence is a discrete write operation. It must be logged to `GLOBAL_HUB_SYNC_LOG.md` as an `[IFMP RESTORE]` event — with timestamp, source backup path, and target file — BEFORE any subsequent patch or append is applied. A restoration with no prior `[IFMP RESTORE]` log entry is a BREACH.

If a file restore operation (from any backup version) occurs mid-sequence before a subsequent patch or edit, a new sliding-window backup must be taken of the restored file before any further writes proceed. The pre-restore backup does not satisfy this requirement.

---

## Condensed Version for AGENTS.md

*Append the following block to `AGENTS.md` under a new section titled
`PRIORITY 4: INSTRUCTION FILE MANAGEMENT`.*

```
### PRIORITY 4: INSTRUCTION FILE MANAGEMENT (IFMP)

18. **Read Before Write**: Manually read any instruction file in full before proposing or
    executing any change. Scripts must never auto-inject content into instruction files.

19. **Sliding Window Backup**: Before any write to L1–L5 or AGENTS.md, rotate the `/backups/original/`
    window: drop `_v1`, shift `_v2`→`_v1`, `_v3`→`_v2`, write new backup as `_v3`. Max 3
    versions per file kept at all times. After writing, confirm modified file is not smaller
    than `_v3`. If smaller → restore from `_v3` immediately.

20. **Append Only**: Never replace or delete existing directives unless user explicitly
    authorizes removal. Surface conflicts to the user before writing.

21. **Correct File Always**: Every new instruction goes into exactly one L-file per the
    defined scope hierarchy. AGENTS.md holds condensed references only — never full rules.
    Never create L6, L7, or any new hierarchy files.

22. **Explicit Authorization**: No write to any instruction file without explicit user
    authorization in the current session. Implicit or prior-session consent does not exist.

23. **IFMP + SEIUP Integration**: SEIUP identifies updates. IFMP executes them.
    Sequence is always: SEIUP approval → backup → read → append.
```
