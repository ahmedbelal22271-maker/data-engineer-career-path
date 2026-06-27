# Anchored Summary

**Project:** Data Engineering Wiki Processing Pipeline
**Root:** C:\Users\marwa\OneDrive\Documents\data engineering\wiki-generation-pipeline
**Core Engine:** Large File Protocol (`.agents/protocols/large_files_protocol.md`)

## How It Works
1. An updates file is received
2. The Large File Protocol processes it through 5 phases
3. Wiki markdown is generated in `de_wiki/`
4. HTML is rendered from wiki markdown into `output/option_a/`

## Key Anchors
- `aim.md` — Project scope and purpose
- `brain.md` — Planning and open decisions
- `protocols/large_files_protocol.md` — The processing engine (non-negotiable)
- `de_wiki/log.md` — Append-only processing record
