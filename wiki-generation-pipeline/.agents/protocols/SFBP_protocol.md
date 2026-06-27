# Source File Backup Protocol (SFBP)

**Status:** Active
**Location:** /protocols/SFBP_protocol.md
**Governs:** Pre-modification safety mechanisms for source code files.

## Trigger Condition
Before executing any tool or command that modifies an existing source file (e.g., `.html`, `.js`, `.py`, `.css`). 
*Note: Instruction files (`AGENTS.md`, `SKILL.md`) are governed separately by IFMP.*

## Rules

### 1. Mandatory Backup Sequence
1. Create a versioned copy of the target file in `/backups/source/` before any modification.
2. Naming Convention: Use the format `[original_basename]_v[N].[ext]` where `N` is the next available version number (e.g., `index_v1.html`). Start at `v1`.
3. Retention Rule: Keep a maximum of 3 versioned backups per file. Delete the oldest before creating the 4th.

### 2. Post-Write Size Validation (Anti-Deletion Guardrail)
Immediately after the file edit completes:
- Compare the byte size of the newly written file against the backup copy.
- If the new file is significantly smaller (e.g., >15% drop) and the user did NOT explicitly instruct a deletion or truncation, the agent must execute a hard revert immediately: overwrite the live file with the backup copy.
- Log the size delta and revert status in the sync log.

### 3. Deadlock-Free Approval Gates
When an operational checklist exists (e.g., "confirm backup is created before proceeding"):
- **Approval Mode:** The agent must pause and ask the human to confirm the backup exists.
- **Turbo/Hybrid Mode:** To prevent a system deadlock, the agent must autonomously execute a `list_dir` or `view_file` tool call to physically verify the target file (the backup) exists on disk. Once the internal tool verifies the gate condition, the agent proceeds without waiting for human confirmation.

## Failure Condition
Modifying a source file without a verified backup physically residing in `/backups/source/` is a strict BREACH of SFBP.
