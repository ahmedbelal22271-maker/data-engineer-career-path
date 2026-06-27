# Pipeline Stage Index

| Stage | File | Protocol Phase | Description |
|-------|------|---------------|-------------|
| 1 | stage_1_config_reconnaissance.md | Phase 0 | Structural Reconnaissance — reading plan |
| 2 | stage_2_spine_pass.md | Phase 1 | Spine Pass — build topic outline |
| 3 | stage_3_deep_extraction.md | Phase 2 | Deep Extraction — write topic content |
| 4 | stage_4_cross_reference_synthesis.md | Phase 3 | Cross-Reference Synthesis — build link graph |
| 5 | stage_5_html_generation.md | Output | HTML Generation — render final output |

## Core Engine
All stages invoke the **Large File Protocol** (`.agents/protocols/large_files_protocol.md`).

## Execution Order
1 → 2 → 3 → 4 → 5 (sequential, each stage depends on previous)
