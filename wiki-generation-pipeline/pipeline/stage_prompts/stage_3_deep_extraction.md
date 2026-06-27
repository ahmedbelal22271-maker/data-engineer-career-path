# Stage 3: Deep Extraction (Wiki Build)

## Objective
Invoke **Phase 2 of the Large File Protocol** — extract content from each chunk into structured wiki topic files.

## Process
Follow the Large File Protocol (`.agents/protocols/large_files_protocol.md`) Section 7 (Phase 2) exactly:
1. For each chunk: perform mandatory 4-layer analysis before extracting
2. Apply extraction rules (high-relevance, cross-references, superseded, off-topic, redundant, etc.)
3. Write extracted content to `de_wiki/topics/[topic].md`
4. Update `de_wiki/index.md` after each topic file write
5. Log contradictions in `de_wiki/contradictions.md`

## Gate
Pass the Phase 2 Gate (Section 7) before proceeding to Stage 4.
