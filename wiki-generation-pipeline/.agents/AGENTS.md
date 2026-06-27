# Data Engineering Wiki Pipeline — Agent Kernel

## Core Processing Engine
This pipeline uses the **Large File Protocol** (`protocols/large_files_protocol.md`) as its processing engine. When an updates file is received, the protocol is invoked to process it through the full 5-phase extraction pipeline, producing a structured wiki in `de_wiki/` and rendering it to HTML in `output/option_a/`.

## Available Protocols (`.agents/protocols/`)
- `DOMP_protocol.md`: Directory Organization
- `FILE_DEDUP_PROMPT.md`: Deduplication Logic
- `IFMP_protocol_prompt.md`: Instruction File Management (Mandatory for all instruction file writes)
- `ISIP_protocol.md`: Isolated Script Injection
- `LTHP.md`: Last-Touch Highlight Protocol
- `PCOM_protocol.md`: Commit/Modification Protocol
- `PDPP_protocol.md`: Protocol Design & Propagation (Mandatory for architecture changes)
- `PSM_protocol.md`: Prompt State Management
- `SFRP.md`: Session-Start File Redundancy
- `UNIVERSAL_PROTOCOL_IMPLEMENTATION_PROFESSIONAL_PROMPT_TEMPLATE.md`: Professional Prompt Templates
- `error_grasping_protocol.md`: SEIUP Error Tracking
- `systematic_debugging_protocol.md`: Systematic Root-Cause Debugging
- `subagent_handoff_protocol.md`: Context Compression & Agent Handoffs
- `AST_refactoring_protocol.md`: AST-Driven Refactoring
- `memory_GC_protocol.md`: Agentic Memory Eviction
- `api_reversing_protocol.md`: Hypothesis-Driven API Reversing
- `large_files_protocol.md`: Handling massive contexts — core processing engine
- `TURBO_AUTONOMY_PROTOCOL.md`: Rules for Turbo Mode
- `CCMP_protocol.md`: Component Co-Migration Protocol
- `SFBP_protocol.md`: Source File Backup Protocol
- `protocol-factory-system-prompt.md`: Protocol factory template
- `index.md`: Protocol directory index

## Available Domain Skills (`.agents/skills/`)
- `anthropic_product_knowledge`: Fact-checking Anthropic products
- `data_architecture`: Dual-database knowledge core and graph/SQL integration
- `datalab_conversion`: Convert PDFs, images, and documents
- `datalab_core`: Base Datalab SDK installation and auth
- `datalab_extraction`: Structured JSON extraction from PDFs/images
- `datalab_form_filling`: Fill forms in PDFs/images
- `datalab_pipelines`: Chain processors into pipelines
- `docx_creation`: Programmatic .docx handling
- `html_css_generation`: Responsive HTML/CSS generation with chunking
- `image_processing`: Image handling and formatting
- `modern_engineering`: Karpathy three-layer architecture
- `prompt_engineering`: Prompt generation, ambiguity resolution
- `prompt_engineering_best_practices`: Comprehensive prompt engineering guide
- `skill-creator`: Create, modify, and evaluate skills
- `study_guide_generation`: Study guide and exam bank templates
- `system_architecture`: Subagent orchestration and error mitigation

## Processing Flow
1. **Incoming updates file** → received into pipeline
2. **Large File Protocol invoked** → phases 0–4 run: reconnaissance → spine → extraction → cross-reference → output mapping
3. **HTML Generation** → Phase 5 renders the wiki markdown into self-contained HTML
