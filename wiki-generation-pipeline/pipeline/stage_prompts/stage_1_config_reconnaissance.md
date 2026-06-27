# Stage 1: Config Reconnaissance

## Objective
Invoke **Phase 0 of the Large File Protocol** — understand the source file's structure and produce a reading plan.

## Process
Follow the Large File Protocol (`.agents/protocols/large_files_protocol.md`) Section 4 (Phase 0) exactly:
1. Complete the Configuration Preamble (Section 0)
2. Retrieve exact total line count of the source file
3. Read first 100–150 lines and last 50–100 lines
4. Produce a Reading Plan with chunk size and total chunk count
5. Write the Phase 0 entry to `de_wiki/log.md`

## Gate
Pass the Phase 0 Gate (Section 4) before proceeding to Stage 2.
