# File Deduplication Prompt (Category A Resolution)

## Purpose
This protocol defines the explicit deduplication logic for Category A (Exact Duplicate) files identified during the Session-Start File Redundancy Protocol (SFRP) or the Directory Organization & Maintenance Protocol (DOMP).

## Category A (Exact Duplicate) Detection Logic
A file is classified as an exact duplicate if it satisfies **at least two of the following three** conditions when compared to an existing file:
1. **Same filename** (or dash-numbered variant, e.g., `AGENTS-1.md` vs `AGENTS.md`)
2. **Same byte size**
3. **Same content hash** (where tooling permits)

## Resolution Sequence
Upon detecting a Category A exact duplicate, the Agent must execute the following sequence:
1. **Confirm Authoritative Copy:** Check the `DOMP_protocol.md` directory rules to determine which copy is the canonical/authoritative version based on its location. (If both are in the same folder, the existing file or highest dash-number is the canonical keeper).
2. **Archive Non-Authoritative Copy:** Move the non-authoritative duplicate to the correct backup directory under a descriptive name (e.g., `filename_duplicate_archived.ext`):
   - If the duplicate is an instruction file (`AGENTS.md`, `L1`–`L5`), archive to `/backups/original/`.
   - If the duplicate is a source, protocol, or script file, archive to `/backups/source/`.
3. **Delete Non-Authoritative Copy:** Ensure the duplicate is fully removed from its original location (this is effectively completed by the archive move).
4. **Log Action:** Log the deduplication action (files involved, which was kept, which was archived) to `GLOBAL_HUB_SYNC_LOG.md`.

## Execution Constraint
- **No interactive prompting loop:** The Agent must perform this deduplication in one pass, make one decision, execute the resolution, and write one log entry. Do not ask the user for confirmation on exact duplicates.
