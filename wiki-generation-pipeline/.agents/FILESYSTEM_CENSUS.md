# File System Census

```
wiki-generation-pipeline/
├── .agents/
│   ├── AGENTS.md
│   ├── CROSS_REFERENCE.md
│   ├── FILESYSTEM_CENSUS.md
│   ├── protocols/
│   │   └── large_files_protocol.md    # Core processing engine
│   ├── skills/
│   └── registers/
│       └── ANCHORED_SUMMARY.md
├── aim.md                  # Project aim
├── brain.md                # Planning
├── de_wiki/                # Wiki output (populated by protocol during processing)
│   ├── index.md
│   ├── spine.md
│   ├── log.md
│   ├── contradictions.md
│   ├── cross_references.md
│   └── topics/              # Generated during Deep Extraction phase
├── pipeline/               # Pipeline stage prompts and scripts
│   ├── generate_stage_prompts.py
│   ├── prompt_creator_stage_specs.md
│   └── stage_prompts/
├── output/                 # Generated HTML output
│   └── option_a/
│       ├── index.html
│       ├── stage_prompts/
│       └── wiki_plan/
└── README.md
```
