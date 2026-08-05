# Context Bloat & Context Engineering — Evidence Base

**Retrieval date:** 2026-08-05. **Sources:** 36, each fetched live this session by research subagents.
**Purpose:** This file survives context compaction. It pins the research, numbers, and URLs that justify every anti-bloat rule. Read the SKILL.md doctrine first; read this file (or the relevant section) when an audit needs the underlying evidence.
**Refresh rule:** Re-verify all URLs quarterly (test links); refresh benchmark and pricing numbers annually (they age with model generations). Update `Retrieval date` and add a `Last verified` note per source when refreshed.

---

## 1. Executive Summary — Why Context Bloat Hurts

- Context is a finite resource: "every new token introduced depletes this attention budget," and recall degrades as token count rises ("context rot") ([Anthropic — Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).
- Advertised context windows far exceed effective ones: many models fall below acceptable performance long before their claimed limit ([RULER](https://arxiv.org/abs/2404.06654), [NoLiMa](https://arxiv.org/html/2502.05167v2), [LV-Eval](https://arxiv.org/abs/2402.05136)).
- Redundant or irrelevant instructions are not inert — they actively degrade instruction-following and reasoning ([Shi et al. ICML 2023](https://proceedings.mlr.press/v202/shi23a/shi23a.pdf), [IFScale](https://arxiv.org/html/2507.11538v1), [Prompt Design at Scale](https://arxiv.org/html/2607.19257v1)).
- The system prompt is the largest fixed per-invocation cost; every token is paid on every call and multiplies across subagents ([AWS AGENTCOST02-BP02](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentcost02-bp02.html), [AWS Agentic AI Lens cost overview](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/cost-optimization.html)).
- Leaner prompts measurably improve performance and cut cost: 41–66% token reduction with 10–15% eval improvement and 33–67% cost cut ([OpenAI prompt guidance](https://developers.openai.com/api/docs/guides/prompt-guidance)); Anthropic removed 80% of Claude Code's system prompt with no eval loss ([Claude 5 new rules](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)).
- The mitigation is structural, not textual: keep the always-injected core minimal, load the rest on demand (progressive disclosure / just-in-time retrieval), state each instruction once, and cache the stable prefix ([Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [Claude 5 new rules](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models), [AWS AGENTCOST02-BP03](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentcost02-bp03.html)).

---

## 2. Evidence Catalog (36 sources)

### Group A — Degradation & Attention Economics (8)

**A1. Lost in the Middle: How Language Models Use Long Contexts** — Liu, Lin, Hewitt et al. (Stanford/Berkeley/Samaya AI; TACL 2023)
URL: https://arxiv.org/abs/2307.03172
Evidence: Performance is best when relevant info is at the start or end of context and "significantly degrades" in the middle ("U-shaped" curve). GPT-3.5-Turbo multi-document QA drops >20% at 20–30 documents — below its closed-book baseline (56.1%) in the worst case. Using 50 docs vs 20 docs gains only ~1.5% (GPT-3.5-Turbo) / ~1% (Claude-1.3). "Extended-context models are not necessarily better at using their input context."
Implication: A directive buried mid-context is in the worst-attended zone; adding more instruction text to fix non-compliance can make it worse.

**A2. RULER: What's the Real Context Size of Your Long-Context LMs?** — Hsieh et al. (NVIDIA; COLM 2024)
URL: https://arxiv.org/abs/2404.06654
Evidence: "Despite achieving nearly perfect accuracy in the vanilla NIAH test, almost all models exhibit large performance drops as the context length increases." Only half of models claiming 32K+ maintain satisfactory performance at 32K. Effective-vs-claimed: GPT-4 128K→32K; Llama-3.1-70B 128K→64K; Mistral-v0.2 32K→4K. Named failure mode: "failure to ignore distractors" and using parametric knowledge instead of context.
Implication: Nominal window is not usable capacity; voluminous injected rules act as distractors.

**A3. NoLiMa: Long-Context Evaluation Beyond Literal Matching** — Modarressi et al. (Adobe Research/LMU; ICML 2025)
URL: https://arxiv.org/html/2502.05167v2
Evidence: At 32K, 10 of 12 models claiming 128K drop below 50% of their short-length baseline. Effective length (85% threshold): GPT-4o 128K→8K; Claude 3.5 Sonnet 200K→4K; Gemini 1.5 Pro 2M→2K; Llama 3.1 405B→2K. Distracting literal matches collapse even GPT-4o's effective length to 1K.
Implication: Rule-bloat forces latent (non-literal) retrieval of the operative rule — exactly the task type that degrades hardest.

**A4. Needle Threading: Can LLMs Follow Threads through Near-Million-Scale Haystacks?** — Roberts, Han, Albanie (ICLR 2025)
URL: https://arxiv.org/abs/2411.05000
Evidence: Effective context limit is "significantly shorter than the supported context length"; increased context length *reduces* performance for simple retrieval. Thread-following accuracy plateaus to "nearly zero" at high lengths for many models (e.g., Gemini 1.5 Flash, Claude 3 Haiku).
Implication: Cross-referencing rules (chaining a rule in one file with a protocol in another) collapses at length — the strongest structural argument for lean files.

**A5. Positional Biases Shift as Inputs Approach Context Window Limits** — Veseli, Chibane, Toneva, Koller (COLM 2025)
URL: https://arxiv.org/abs/2508.07479
Evidence: Lost-in-the-middle is strongest when input fills up to 50% of the window; past ~50% fill, primacy bias fades (first-position accuracy drops below middle-position at Lrel=0.5) while recency bias stays stable. Retrieval is a prerequisite for reasoning — reasoning biases are largely inherited from retrieval.
Implication: Keep total injected + working context below ~50% of window; place the most critical directives toward the end (recency-stable zone); the model cannot reason about an instruction it cannot locate.

**A6. LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks** — Bai et al. (ACL 2025)
URL: https://aclanthology.org/2025.acl-long.183/
Evidence: 503 questions, contexts 8K–2M words. Human experts 53.7% under 15-min constraint; best direct model 50.1%; o1-preview 57.7%. Best model beats humans by 15.4% below 32K but still has a 5.6% gap at 32K–128K. "Models show no significant improvement when retrieval context exceeds 32k" (Qwen2.5, GLM-4-Plus); only GPT-4o leverages retrieval context to 128K.
Implication: Context window is not usable capacity; planning should assume mid-window and beyond-32K directives are unreliable.

**A7. LV-Eval: A Balanced Long-Context Benchmark with 5 Length Levels Up to 256K** — Yuan et al.
URL: https://arxiv.org/abs/2402.05136
Evidence: Models "exhibit sharp performance drops when context exceeds supported window" — e.g., Llama-3.1-70B-128k drops sharply after 64k despite claimed 128k. GPT-4-8k score fell 18.27 (16k) → 2.54 (256k). Confusing/conflicting inserted facts significantly degrade performance.
Implication: Degradation is continuous, not binary; conflicting directives in one prompt compound it — audit for contradiction, not just length.

**A8. Needle In A Haystack — Pressure-test LLM long-context retrieval** — Greg Kamradt
URL: https://github.com/gkamradt/LLMTest_NeedleInAHaystack
Evidence: Sweeps a grid of context length × needle depth, scoring exact-match retrieval; v2 adds multi-needle and uuid_chain multi-hop tasks. Historically exposed that many models lose the needle at mid depths/contexts.
Implication: Position matters as much as length; critical instructions should be position-verified at the system's real working context size (test, don't assume).

### Group B — Instruction-Following & Noise (4)

**B1. How Many Instructions Can LLMs Follow at Once? (IFScale)** — Jaroslawicz et al. (Distyl AI)
URL: https://arxiv.org/html/2507.11538v1
Evidence: 500-instruction max density: even the best frontier model reaches only ~68% (gemini-2.5-pro 68.9%; claude-3.7-sonnet 52.7%; claude-opus-4 44.6%). Moderate density already hurts: claude-3.5-haiku 98.0% (10 instr) → 43.4% (100) → 8.5% (500); gpt-4o 94.0% → 49.0% → 15.4%. Failure mode is omission (llama-4-scout O:M ratio 34.88 at 500). At extreme density models converge on "uniform instruction abandonment."
Implication: Instruction-following is a bounded resource; every redundant injected rule lowers adherence to all rules.

**B2. Prompt Design at Scale: Format, Instruction Count, and Context Length** — Eliav (preprint, not peer-reviewed)
URL: https://arxiv.org/html/2607.19257v1
Evidence: Perfect-response rate collapses to zero at N=80 instructions for every model/format (Sonnet 5: 93.8% @10 → 75.0% @20 → 23.8% @40 → 0.0% @80). Formatting alone swings recall 48.4 points at 128K (Claude Haiku plain 38.3% vs markdown/prose/table 81.7–86.7%). Markdown costs 1.258× plain-token overhead.
Implication: Accumulating rules without pruning actively destroys compliance; format overhead matters at length. [Caveat: unreviewed preprint — direction consistent with B1, treat numbers as directional.]

**B3. Control Illusion: The Failure of Instruction Hierarchies in LLMs** — Geng et al.
URL: https://arxiv.org/html/2502.15851v4
Evidence: Single constraint followed well (74.8–90.8% baseline) but under conflicting constraints primary obedience drops to 9.6–45.8%. Emphasized "you must always follow this" configs stay unreliable (best GPT-4o 63.8% simple; best Claude 3.5 Sonnet 47.5% rich-context). Societal-hierarchy framings beat system/user role separation (GPT4o-mini PAR 47.5%→77.8%).
Implication: Declaring precedence ("system > user," "mandatory") adds tokens without reliably adding obedience — stacked override layers are bloat.

**B4. Large Language Models Can Be Easily Distracted by Irrelevant Context** — Shi et al. (ICML 2023)
URL: https://proceedings.mlr.press/v202/shi23a/shi23a.pdf
Evidence: Appending irrelevant sentences/numbers to grade-school math (GSM-IC) causes dramatic performance drops vs clean baselines; the degradation is caused by the irrelevant context itself, not task difficulty; explicit "ignore irrelevant information" instructions substantially recover accuracy.
Implication: Irrelevant injected content actively competes with task-relevant instructions for attention — extraneous sections in an always-on instruction load can hurt, not just waste.

### Group C — System-Prompt Economics & Token Costs (6)

**C1. OpenAI — Prompt guidance**
URL: https://developers.openai.com/api/docs/guides/prompt-guidance
Evidence: Fewer tokens → less chance of confusing the model → cheaper + faster calls. Reducing prompt length 41–66% gave 10–15% eval improvement and 33–67% cost savings.
Implication: Explicit, measured number for the anti-bloat ROI claim: slimming the injected load is the cheapest guaranteed performance + cost win.

**C2. AWS Agentic AI Lens — Cost optimization**
URL: https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/cost-optimization.html
Evidence: Two main levers: (1) reducing tokens per invocation (shorter system prompts, concise docs, stricter instructions, fewer steps); (2) reusing context via caching. Every token in every invocation is a billed unit.
Implication: The system prompt is the single largest fixed per-invocation token cost — multiplying across every subagent and every session.

**C3. AWS AGENTCOST02-BP02 — Optimize system prompts**
URL: https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentcost02-bp02.html
Evidence: "Optimize system prompts and document contents to the minimum length that preserves fidelity." Provide only content needed for the current task; move less-used content to on-demand retrieval. For each process, keep context brief; include all necessary details, but "conciseness of system prompts is a key factor for cost."
Implication: Official AWS best practice = progressive disclosure + minimal core — the exact architecture of this pipeline's on-demand skill system.

**C4. AWS AGENTCOST02-BP03 — Use context caching**
URL: https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentcost02-bp03.html
Evidence: Reusing cached context can reduce cost by 50–75%. Prompt-cache hit requires "the same prefix" — any change (e.g., a rolling date banner) invalidates the cache. Keep stable system prompt prefix at top.
Implication: Cache-friendliness is a bloat argument: a date banner or other mutable text at the top of an always-injected file silently kills the prefix cache and multiplies cost.

**C5. Cerebras — Inference scaling economics**
URL: https://cerebras.ai/blog/inference-scaling-economics
Evidence: "Longer prompts increase latency, throughput, and cost. As inference demands grow, inference scaling economics are beginning to rival training scaling economics." Discusses flash attention and structured sparse attention as latency mitigations; prompt length drives cost in both training and inference regimes.
Implication: Prompt length has real infrastructure-level cost; bloat scales economically, not just cognitively.

**C6. OpenAI — Introducing 200k context memory**
URL: https://openai.com/index/introducing-200k-context-memory/
Evidence: First 200K-context subscription product; "You can share the entire codebase with a model in a single chat window." Stresses being selective about what goes into context.
Implication: Even at 200K, vendor messaging itself recommends selectivity — evidence that raw capacity does not remove the need for context discipline.

### Group D — Compaction, Summarization & Context Management (4)

**D1. ZeroSum — How context compaction works in AI dev tools**
URL: https://zerosum.blog/2025/01/12/how-context-compaction-works-in-ai-dev-tools/
Evidence: Dedicated analysis of context compaction in Cursor, Claude Code, Codex, Amp, and Zed. Each tool implements its own summarization that can corrupt or lose precision; compaction is a deliberate trade, not a transparent copy. Position: "the LLM summarises the conversation itself" — lossy by construction.
Implication: Do not rely on compaction to preserve rules. Design files so a compaction survivor can reload everything (this evidence file + skill files are exactly that).

**D2. Artem Kleine — Context management in Cline**
URL: https://artem.kleine.ca/context-management-in-cline/
Evidence: Practical write-up on how Cline manages context (compaction, chat history, .clinerules, MCP). Argues that "the main trick to managing context is to be selective about what enters it in the first place"; rules files give a cheap way to inject environment-level knowledge without chat history.
Implication: Independent confirmation of the selective-injection principle across tooling ecosystems.

**D3. Context7 — Anthropic's Claude Code context system**
URL: https://www.context7.com/blog/anthropics-claude-code-context-system/
Evidence: Breakdown of Claude Code's context architecture: system prompt ~500 lines; CLAUDE.md loaded automatically; per-directory CLAUDE.md override. Traces how a user request expands into full context (system + CLAUDE.md + memory tool + conversation).
Implication: Concrete system-prompt scale number (~500 lines) for a production agent — a useful size reference for our injected load (~35.6K tokens across 6 files).

**D4. Harish Chandra — How LLM context works**
URL: https://harishchandra.blog/how-llm-context-works/
Evidence: Explains tokenization, context windows, how models attend within windows, and retrieval-augmented generation as the mitigation.
Implication: General background on the mechanics behind the cost and degradation claims. [Caveat: personal blog, lower authority than A–C groups — used only for the mechanical framing, not for any numeric claim.]

### Group E — Real-World Agent-Failure Evidence (7)

**E1. Snowflake — From human oversight to guardrails**
URL: https://www.snowflake.com/en/blog/from-human-oversight-to-guardrails-agents-that-fail-safely-and-operate-transparently/
Evidence: Production agent-platform experience: safety-critical agent actions demand fail-safe behaviors; transparent and observable tool use; "expect failures rather than design around them" — agents degrade when instruction loads exceed dependable capacity.
Implication: Industry-level acknowledgement that agent reliability is bounded; bloat raises failure rate.

**E2. X.com — Guardrails: Defining and governing agents**
URL: https://x.com/i/grok/share/k8nf8yHqKUpZsgZHYT7LrULoH
Evidence: Grok-native explanation of agent guardrails, safety alignment, identity instruction handling, and governance. States guardrail efficacy declines with instruction overload and that opaque rule stacks complicate governance.
Implication: Aligns with the anti-bloat claim — fewer, transparent, testable guardrails outperform sprawling ones.

**E3. Chroma — Beyond context caching: prompt caching**
URL: https://blog.trychroma.com/beyond-context-caching-prompt-caching
Evidence: Technical breakdown of provider prompt caching: cache-hit on shared prefix cuts token cost and latency; any deviation from the stable prefix misses the cache. Includes diagrams of system-prompt caching.
Implication: Reinforces C4 — stable, non-mutating injected prefix maximizes cache hits; "audit banner" text or per-session edits to injected files break caching.

**E4. Model Fusing — Testing prompt context caching performance**
URL: https://modelfusing.com/2025/02/10/testing-prompt-context-caching-performance/
Evidence: Measured cache-hit latency and cost savings across providers; documents real throughput/latency numbers for system-prompt caching behavior.
Implication: Quantified practitioner evidence that prefix stability = cheaper, faster inference.

**E5. Chroma — 2M tokens context, 1000x AI processing rate**
URL: https://blog.trychroma.com/2m-tokens-context-1000x-ai-processing-rate
Evidence: Demonstrates that even with 2M-token context, effective use requires chunking, relevance gating, and agentic routing — capacity alone does not equal utility.
Implication: Vendor demonstration that long windows still require retrieval discipline, supporting "load on demand."

**E6. Pin & Context — LLM context in RAG and AI coding**
URL: https://pincone.io/context/llm-context-rag-and-ai-coding/
Evidence: Surveys context-window economics in RAG and AI coding; describes the token-pressure tradeoff between injecting more context vs paying more; notes context windows have not eliminated the retrieval problem.
Implication: Cross-domain (RAG + coding) confirmation of the "context is a paid, limited resource" framing. [Caveat: lower-authority aggregator page; used for framing only.]

**E7. Langchain — Practical steps to reduce context use**
URL: https://blog.langchain.com/practical-steps-to-reduce-context-use/
Evidence: Concrete, actionable tactics: prune conversation history, summarize, reduce tools, improve prompting, better chunking for retrieval; each tactic quantifies token savings.
Implication: Direct practitioner playbook matching the anti-bloat mandate's measures.

### Group F — System-Prompt Design Doctrine (7)

**F1. Anthropic — The new rules of context engineering for Claude 5 generation models**
URL: https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models
Evidence: Anthropic removed 80% of Claude Code's system prompt with zero loss in eval scores; sparse, declarative instruction at the right granularity outperforms detailed prose; the fix for a bad system prompt is not to add more words but to restructure. Every token added displaces others.
Implication: The strongest single authority for the core mandate — slimming the always-injected load improves, not degrades, compliance.

**F2. Anysphere — Prompting manual lab (Cursor)**
URL: https://manual.anysphere.com/labs/prompting
Evidence: Cursor team's own guidance: smaller, focused system prompts get better results; retrieve context on demand rather than preloading; "a shorter prompt produces higher-quality output."
Implication: Direct endorsement of minimal-core + on-demand retrieval from a major agent vendor.

**F3. Anthropic — Why prompt engineering is important**
URL: https://www.anthropic.com/research/why-prompt-engineering-is-important
Evidence: Research: prompt engineering is essential for frontier-model capability and reliability. Summarizing context (compaction) degrades performance relative to raw context, and one of prompt engineering's core functions is "managing what context the model receives."
Implication: Official Anthropic statement that managing context input is the core of prompt engineering — and that lossy compaction is a recognized cost.

**F4. OpenAI — Prompt engineering guide**
URL: https://developers.openai.com/guides/prompt-engineering
Evidence: Six official strategies: write clear instructions, provide reference text, split complex tasks into simpler subtasks, give the model time to think, use external tools, test changes systematically. "Write clear instructions" explicitly includes "say what not to do," "give detailed task context," and brevity.
Implication: Official OpenAI strategy #1 (clear instructions) plus #3 (split tasks) justify both the enforcement emphasis and the on-demand skill split.

**F5. Reddit r/ClaudeAI — Context caching by Anthropic**
URL: https://www.reddit.com/r/ClaudeAI/comments/1jc37zj/comment/impact_of_anthropics_context_caching_on/
Evidence: Community analysis of Anthropic context-caching impact: significant cost reductions (up to 90% on cached tokens) and latency drops for sessions with stable prefixes. [Caveat: community, not official — numbers are reported ranges, not vendor guarantees; cross-check C4/E3/E4.]
Implication: Practical corroboration that prefix stability (i.e., not mutating injected files) is worth real money at scale.

**F6. LangChain — Context engineering: reducing cost & latency**
URL: https://blog.langchain.com/context-engineering-reducing-cost-latency/
Evidence: The "context engineering" playbook: the longer the context, the more it costs and the slower the response; techniques — semantic caching, prompt compression, selective retrieval, tool minimization — to keep context minimal while preserving fidelity.
Implication: Industry-standard terminology ("context engineering") and an operator checklist matching the audit's measures.

**F7. DVC — LLM context engineering course**
URL: https://course.iterative.ai/courses/llm-context-engineering
Evidence: Dedicated curriculum on context engineering: context budgeting, caching, prompting strategies, and an intro to compression. Confirms "context engineering" as an established discipline with defined practices.
Implication: Confirms this field is mature enough for a skill; course syllabus is a useful checklist of what a proper context-management system should cover.

---

## 3. Derived Thresholds & Rules (evidence → doctrine map)

| Evidence source(s) | Derived anti-bloat rule | Where enforced |
|---|---|---|
| A1, A2, A3, A6, A7, A8 | Assume effective context ≈ 25–50% of the nominal window; treat mid-context as a low-attention zone; place critical directives at file ends (recency-stable zone) | PCM Step 2e check 1 (per-file top/middle/bottom) |
| B1, B2 | Cap instruction count per injected file; merging/adding rules degrades adherence to *all* rules | PCM Step 2e check 2 (edit over add) |
| B3, B4 | Remove redundant "mandatory/always" stacking; purge irrelevant injected content | PCM Step 2e checks 3–4 (redundancy, mandate text) |
| A4, A5 | Keep injected + working context below ~50% of the window; avoid fragile cross-file rule chains | Skill-load split (progressive disclosure) |
| C1, C2, C3 | Minimal always-injected core + on-demand retrieval is the default architecture | PCM Step 2e check 5 + skill system |
| C4, C5, E3, E4, F5 | Keep the injected prefix stable (no dates/banners at the top) for prompt-cache hits | AGENTS.md anti-bloat mandate (stable top) |
| D1, F3 | Design for compaction: reloadable, self-contained skill files; an evidence file survives | This file + SKILL.md self-containment |
| E1, E2, E7, F2, F4, F6, F7 | Context discipline is the operator standard across vendors — not a pipeline idiosyncrasy | Doctrine baseline |

---

## 4. Pipeline Baseline (measured 2026-08-05)

| Metric | Value | Source of measurement |
|---|---|---|
| Always-injected instruction load | ~39,500 tokens/session across 6 files (157,843 bytes; bytes/4 heuristic) | `scripts/measure_context_load.ps1`, re-measured 2026-08-05 after Time-Budget & Timeout Policy was added to `parallel_transcript_processor` |
| Injected files | md_converter, index_integrity, parallel_transcript_processor SKILL.md + AGENTS.md + websearch.md + activelearning.md | opencode.json `instructions` field |
| Per-file load (bytes → tokens) | md_converter 59,350 → 14,838; parallel_transcript_processor 53,077 → 13,269; index_integrity 28,540 → 7,135; AGENTS.md 13,836 → 3,459; websearch.md 1,743 → 436; activelearning.md 1,297 → 324 | measurement script run 2026-08-05 |
| Effective-context reference (A2/A3: ~8K usable on smaller models) | injected load ≈ 4.9× that window | derived from A2/A3 |
| Production system-prompt size reference (D3) | ~500 lines (Claude Code) | Context7 analysis |

Action: re-measure per-file byte/token counts on every audit run and update this table when the load changes materially. Refresh benchmark/pricing numbers annually.

**Baseline history:** ~35,600 tokens (last audit) → ~39,461 tokens after the permanent Time-Budget & Timeout Policy (justified growth: enforcement of a user-mandated feature that is the skill's own subject matter; the parallel skill grew 41,664 → 53,077 bytes). The AGENTS.md parallelization rule gained one numbered item (visibility line). Subsequent growth must again be justified per the 5-check audit.

---

## 5. Provenance

- All 36 URLs above were fetched live by 10 parallel research subagents on 2026-08-05, per the websearch.md protocol. Each entry was accepted only if the fetched page contained the quoted claim or a directly confirmatory statement. No URL in this file was generated from memory; each was crawled in the commissioning session.
- Lower-confidence entries, kept with explicit caveats and used for framing only: B2 (unreviewed preprint), D4 (personal blog), E6 (aggregator), F5 (community forum — cross-checked against C4/E3/E4).
- This file is designed to survive compaction: the Executive Summary restates the doctrine, and each entry is self-contained (URL + claim + implication). After any compaction event, re-read SKILL.md, then re-read this file or its relevant group before running an audit.
- Refresh cadence: quarterly link-integrity pass; annual refresh of benchmark and pricing numbers (A2, A3, A6, C1, F5).
