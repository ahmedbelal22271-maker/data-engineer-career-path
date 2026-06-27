# Stage Specifications

This pipeline is driven by the **Large File Protocol** (`.agents/protocols/large_files_protocol.md`). The protocol governs all processing. Stage prompts are invocation guides that map to the protocol's phases.

## Stage Mapping

| Stage | Protocol Section | Purpose |
|-------|-----------------|---------|
| 1 — Config Reconnaissance | Phase 0 + Section 3 | Structural recon, reading plan, preamble |
| 2 — Spine Pass | Phase 1 (Section 6) + Oracle-DAG (Section 5) | Build spine, independence assessment |
| 3 — Deep Extraction | Phase 2 (Section 7) | Multi-layer analysis, wiki topic extraction |
| 4 — Cross-Reference Synthesis | Phase 3 (Section 8) | Cross-reference graph, contradiction resolution |
| 5 — HTML Generation | Output phase | Render wiki markdown into self-contained HTML |

## Execution Order
Stages 1→2→3→4→5 are sequential. Each stage invokes the corresponding protocol phase and passes its gate before proceeding.
