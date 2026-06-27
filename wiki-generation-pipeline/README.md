# Data Engineering Wiki Processing Pipeline

A self-contained processing pipeline that receives updates files and applies the **Large File Protocol** to extract, structure, and render data engineering knowledge into a self-contained HTML wiki.

## How It Works

1. **Updates file arrives**
2. **Large File Protocol** processes it through 5 phases:
   - Phase 0: Structural Reconnaissance
   - Phase 1: Spine Pass
   - Phase 2: Deep Extraction → wiki topics generated in `de_wiki/topics/`
   - Phase 3: Cross-Reference Synthesis & Contradiction Resolution
   - Phase 4: Output Mapping & Master Summary
3. **HTML rendered** → `output/option_a/index.html`

## Structure

```
wiki-generation-pipeline/
├── .agents/
│   ├── AGENTS.md
│   ├── protocols/
│   │   └── large_files_protocol.md    # Core processing engine
│   └── registers/
├── aim.md                              # Project scope
├── brain.md                            # Planning
├── de_wiki/                            # Wiki (populated by protocol during processing)
│   ├── index.md
│   ├── spine.md
│   ├── log.md
│   ├── contradictions.md
│   ├── cross_references.md
│   └── topics/                         # Generated during Deep Extraction
├── pipeline/                           # Stage prompts invoking the protocol
│   ├── generate_stage_prompts.py
│   └── stage_prompts/
└── output/
    └── option_a/                       # Generated HTML wiki
        └── index.html
```

## Processing Engine

The **Large File Protocol** (`.agents/protocols/large_files_protocol.md`) is the non-negotiable core. Every phase has defined gates that must be passed before proceeding.
