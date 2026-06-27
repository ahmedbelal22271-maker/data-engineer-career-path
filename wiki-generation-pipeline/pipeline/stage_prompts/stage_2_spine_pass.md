# Stage 2: Spine Pass (Oracle Pass)

## Objective
Invoke **Phase 1 of the Large File Protocol** — read the entire source file sequentially and produce a structural map.

## Process
Follow the Large File Protocol (`.agents/protocols/large_files_protocol.md`) Section 6 (Phase 1) exactly:
1. Read in the chunk sizes defined in Stage 1
2. Log every completed chunk to `de_wiki/log.md` immediately
3. Write per-chunk entries to `de_wiki/spine.md` with content types, themes, and independence assessment
4. Run the Oracle-DAG decision (Section 5) to determine parallelization
5. Arithmetically reconcile line coverage

## Gate
Pass the Phase 1 Gate (Section 6) before proceeding to Stage 3.
