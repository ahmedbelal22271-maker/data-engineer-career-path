---
name: SkillOpt
description: Microsoft's text-space optimizer that trains reusable natural-language skills for frozen LLM agents through trajectory-driven edits, validation-gated updates, and deployable best_skill.md artifacts. Use when the user wants to optimize agent prompts/skills, run SkillOpt training loops, evaluate skill artifacts, extend with new benchmarks or backends, or use SkillOpt-Sleep for nightly self-evolution. Also use when the user mentions ReflACT, skill optimization, prompt optimization, agent skill training, trajectory-driven editing, text-space gradient descent, "make my agent learn from past sessions", "review my past sessions", "learn my preferences", "consolidate what you learned", "run the sleep cycle", schedule offline self-optimization, memory/skill consolidation, nightly dream cycle, or wants to schedule offline self-improvement. Drives the skillopt_sleep engine: harvest past sessions -> mine recurring tasks -> replay offline -> consolidate validated memory + skills behind a held-out gate.
---

# SkillOpt: Executive Strategy for Self-Evolving Agent Skills

*Train agent skills like you train neural networks — with epochs, (mini-)batchsize, learning rates, and validation gates — but without touching model weights.*

**Repository:** https://github.com/microsoft/SkillOpt | **Paper:** https://arxiv.org/abs/2605.23904 | **Docs:** https://microsoft.github.io/SkillOpt | **PyPI:** `pip install skillopt`

---

## When to use this skill

Trigger when the user wants any of:
- to **optimize agent prompts/skills** via trajectory-driven text-space editing;
- to **run SkillOpt training loops** on any supported benchmark;
- to **evaluate skill artifacts** on held-out test sets;
- to **extend SkillOpt** with new benchmarks, backends, or environment adapters;
- to use **SkillOpt-Sleep** for nightly offline self-evolution — "make my agent learn from how I use it", "get better the more I use it", "remember my preferences across sessions", a nightly/scheduled or on-demand sleep/dream/offline self-improvement run, to review past sessions and distill recurring tasks, to consolidate feedback into memory or managed skills, to schedule the cycle (cron) or adopt a staged proposal;
- the user mentions ReflACT, skill optimization, prompt optimization, agent skill training, trajectory-driven editing, or text-space gradient descent.

---

## 1. Core Architecture & Concepts

SkillOpt treats a **Markdown skill document** as the trainable state of a frozen LLM agent. A separate **optimizer model** turns scored rollout trajectories into bounded add/delete/replace edits on the skill document; a candidate edit is accepted only when it strictly improves a held-out validation score. The deployed artifact is a compact `best_skill.md` (typically 300–2,000 tokens) that runs against the unchanged target model with **zero inference-time overhead**.

### Performance
Across six benchmarks, seven target models, and three execution harnesses (direct chat, Codex CLI, Claude Code CLI), SkillOpt is best or tied-best on **all 52 evaluated cells**. On GPT-5.5 it lifts average no-skill accuracy by **+23.5 pts in direct chat, +24.8 inside Codex, +19.1 inside Claude Code**. Optimized skills transfer across model scales, between harnesses, and to nearby benchmarks without further optimization.

### DL ↔ SkillOpt Mapping

| Deep Learning | SkillOpt | Description |
|---|---|---|
| Model weights | Skill document (Markdown) | The thing being optimized |
| Forward pass | Rollout | Target executes tasks with current skill |
| Loss function | Task evaluator | Scores execution quality (hard/soft) |
| Backpropagation | Reflect | Optimizer analyzes failures → edit patches |
| Gradients | Edit patches | Proposed changes (append/replace/delete/insert_after) |
| Gradient aggregation | Patch aggregation (`merge_patches`) | Merge similar edits across minibatches |
| Gradient clipping | Edit selection (`rank_and_select`) | Cap max edits per step via learning rate budget |
| Learning rate | `optimizer.learning_rate` | Max edits applied per step |
| LR scheduler | `optimizer.lr_scheduler` | cosine / linear / constant / none |
| SGD step | Skill update | Apply selected patches via `apply_patch_with_report` |
| Validation set | Selection split (valid_seen) | Gate checks improvement |
| Early stopping | Gate acceptance/rejection | Reject non-improving updates |
| Momentum | Slow update | Epoch-boundary longitudinal comparison |
| Meta-learning | Meta skill | Cross-epoch optimizer strategy memory |
| Batch size | `train.batch_size` | Tasks sampled per rollout |
| Data parallelism | `gradient.analyst_workers` | Parallel reflection workers |
| Checkpointing | Skill snapshots (`skills/skill_vNNNN.md`) | Saved after each step |
| Transfer learning | Seed skill / cross-benchmark init | Start from pre-trained skill |

---

## 2. Installation & Setup

```bash
# Core install
pip install skillopt

# Or from source
git clone https://github.com/microsoft/SkillOpt.git
cd SkillOpt
pip install -e .

# Optional extras
pip install -e ".[alfworld]"      # ALFWorld benchmark
pip install -e ".[claude]"        # Claude backend
pip install -e ".[qwen]"          # Qwen local via vLLM
pip install -e ".[searchqa]"      # SearchQA data materialization
pip install -e ".[webui]"         # Gradio dashboard
pip install -e ".[dev]"           # ruff + pytest
pip install -e ".[all]"           # everything except docs/dev/webui
```

### Environment Variables

| Variable | Backend | Purpose |
|---|---|---|
| `AZURE_OPENAI_ENDPOINT` | `azure_openai` | Azure resource endpoint |
| `AZURE_OPENAI_API_KEY` | `azure_openai` | Azure API key |
| `AZURE_OPENAI_API_VERSION` | `azure_openai` | API version (default: `2024-12-01-preview`) |
| `AZURE_OPENAI_AUTH_MODE` | `azure_openai` | `api_key` / `azure_cli` / `managed_identity` / `aad` |
| `OPTIMIZER_AZURE_OPENAI_ENDPOINT` | optimizer-specific | Override optimizer endpoint |
| `TARGET_AZURE_OPENAI_ENDPOINT` | target-specific | Override target endpoint |
| `OPTIMIZER_DEPLOYMENT` | optimizer | Optimizer model deployment name |
| `TARGET_DEPLOYMENT` | target | Target model deployment name |
| `OPENAI_API_KEY` | `openai` | OpenAI API key |
| `ANTHROPIC_API_KEY` | `claude` | Anthropic API key |
| `CLAUDE_CLI_BIN` | `claude` | Path to Claude CLI binary (default: `claude`) |
| `CLAUDE_PERMISSION_MODE` | `claude` | Claude CLI permission mode (default: `dontAsk`) |
| `QWEN_CHAT_BASE_URL` | `qwen` | Local vLLM endpoint |
| `MINIMAX_BASE_URL` / `MINIMAX_API_KEY` | `minimax` | MiniMax endpoint |
| `OPENAI_COMPATIBLE_BASE_URL` | `openai_compatible` | Any OpenAI-compatible endpoint |

Verify: `python -c "import skillopt; print('SkillOpt ready!')"`

---

## 3. The Training Loop (ReflACTTrainer)

The main training loop is implemented in `skillopt/engine/trainer.py` as the `ReflACTTrainer` class (2,406 lines). The entry point is `scripts/train.py`.

### 3.1 Initialization Sequence

1. **Adapter setup**: `adapter.setup(cfg)` — one-time init (data loading, split creation)
2. **Dataloader**: `adapter.get_dataloader()` — returns `BaseDataLoader` or `None`
3. **Model configuration**: Configures optimizer/target backends, deployments, reasoning effort, Azure OpenAI clients, Codex exec, Claude code exec, Qwen chat, MiniMax chat
4. **Ray init**: If `adapter.requires_ray()` returns True, initializes Ray with `num_gpus=0`
5. **Initial skill**: Loads from `env.skill_init` path, or starts from blank
6. **Training parameters**: Computes `train_size`, `steps_per_epoch`, `batches_per_epoch`, `total_steps`
7. **LR scheduler**: Builds via `build_scheduler(mode, max_lr, min_lr, total_steps)`
8. **Base seeds**: Generates deterministic seeds via `dataloader.make_base_seeds()` or `seed + i + 1`
9. **Resume check**: Loads `runtime_state.json` and `history.json` if present, resumes from last completed step
10. **Skill-aware reflection**: Configures `use_skill_aware_reflection` toggle, injects empty appendix field if enabled
11. **Selection cache**: Builds from existing history records

### 3.2 Per-Step Pipeline (6 phases)

```
for epoch in num_epochs:
  for step_in_epoch in steps_per_epoch:
    for a in accumulation:
      ① ROLLOUT   — adapter.rollout(train_env, current_skill, rollout_dir)
      ② REFLECT   — adapter.reflect(rollout_results, current_skill, ...) → raw_patches

    ③ AGGREGATE  — merge_patches(current_skill, failure_patches, success_patches, ...)
    ④ SELECT     — rank_and_select(current_skill, merged_patch, max_edits=edit_budget, ...)
    ⑤ UPDATE     — apply_patch_with_report(current_skill, ranked_patch)
    ⑥ EVALUATE   — adapter.rollout(sel_env, candidate_skill, ...) → gate decision
```

### 3.3 Phase Details

**① ROLLOUT** (line ~1132): Target model executes tasks with current skill. Calls `adapter.rollout(train_env, current_skill, rollout_dir, use_eval_feedback=True)`. Returns list of dicts with `{"id", "hard" (0|1), "soft" (0.0-1.0), "fail_reason", ...}`.

**② REFLECT** (line ~1144): Optimizer analyzes trajectories and produces edit patches. Calls `adapter.reflect(rollout_results, current_skill, batch_dir, ...)`. Each raw patch has structure `{"patch": {"edits": [...]}, "source_type": "failure"|"success"}`. The reflect phase is parallelized via `analyst_workers`. Step buffer context and meta skill context are passed to give the optimizer history.

**③ AGGREGATE** (line ~1233): Merges semantically similar patches across minibatches via `merge_patches()`. Uses LLM to deduplicate and consolidate. The merge uses prompts from `skillopt/prompts/merge_failure.md`, `merge_success.md`, `merge_final.md` (and their rewrite/full_rewrite variants).

**④ SELECT** (line ~1251): Ranks and clips edits by learning rate budget. Uses `rank_and_select()` from `skillopt/optimizer/clip.py`. In autonomous LR mode, `decide_autonomous_learning_rate()` from `skillopt/optimizer/lr_autonomous.py` dynamically determines the budget. In full_rewrite_minibatch mode, this phase is skipped.

**⑤ UPDATE** (line ~1321): Applies selected patches to skill document. Three modes:
- `patch` mode: `apply_patch_with_report(current_skill, ranked_patch)` — applies individual edits
- `rewrite_from_suggestions` mode: `rewrite_skill_from_suggestions()` — LLM rewrites full skill from suggestions
- `full_rewrite_minibatch` mode: Selects the best skill candidate from merged candidates

**⑥ EVALUATE** (line ~1431): Validates candidate on selection set (valid_seen). Uses `evaluate_gate()` from `skillopt/evaluation/gate.py`. Returns `GateResult` with action: `accept`, `accept_new_best`, `reject`, or `force_accept`.

### 3.4 Step Buffer

The step buffer (`step_buffer: list[dict]`) accumulates per-step context within an epoch so optimizers see full history. Each entry captures:
- `step`: global step number
- `action`: accept/reject/skip
- `failure_patterns`: extracted from rollout results
- `rejected_edits`: only on reject, with score before/after
- `n_fail`, `n_total`: failure counts

Formatted via `_format_step_buffer()` (line ~522) and passed to reflection as `step_buffer_context`.

### 3.5 Epoch Boundary Operations

**Slow Update** (line ~1637): Longitudinal comparison between epochs.
- Epoch 1: Injects empty placeholder via `inject_empty_slow_update_field()`
- Epoch 2+: Rolls out both prev/curr epoch skills on sampled train items, builds comparison pairs via `build_comparison_pairs()`, runs `run_slow_update()` from `skillopt/optimizer/slow_update.py`
- Comparison pair categories: `improved`, `regressed`, `persistent_fail`, `stable_success`
- Longitudinal pair policy: `mixed` (all pairs), `changed` (improved/regressed only), `unchanged` (persistent_fail/stable_success only)
- Two acceptance modes: `slow_update_gate_with_selection=True` (gated via selection set) or `False` (force-accept into current_skill only, not best_skill)

**Meta Skill** (line ~1957): Cross-epoch optimizer strategy memory.
- Epoch 1: Skipped
- Epoch 2+: Runs `run_meta_skill()` from `skillopt/optimizer/meta_skill.py` comparing prev/curr epoch skills with comparison pairs
- Produces `meta_skill_content` injected into subsequent reflection prompts

### 3.6 Final Evaluation

After training completes:
1. **Final skill validation**: Runs current_skill on valid_seen; if it beats best, promotes to best
2. **Baseline test**: Evaluates initial skill S_0 on test set (valid_unseen)
3. **Best skill test**: Evaluates best skill on test set
4. **Final skill test**: Evaluates last skill on test set (may differ from best)
5. **Summary**: Writes `summary.json` with all scores, timing, token usage, epoch stats

---

## 4. Configuration Reference

Configs use YAML with hierarchical override from `configs/_base_/default.yaml`. Config loading is in `skillopt/config.py` — supports `_base_` inheritance via YAML anchors.

### 4.1 Model Configuration

| Parameter | Type | Default | Description |
|---|---|---|---|
| `model.backend` | str | `azure_openai` | `azure_openai` / `openai_chat` / `claude_chat` / `claude_code_exec` / `codex_exec` / `qwen` / `qwen_chat` / `minimax_chat` / `openai_compatible` |
| `model.optimizer` | str | `gpt-5.5` | Optimizer model name |
| `model.target` | str | `gpt-5.5` | Target model name |
| `model.optimizer_backend` | str | `openai_chat` | Optimizer backend |
| `model.target_backend` | str | `openai_chat` | Target backend |
| `model.reasoning_effort` | str | `medium` | `low` / `medium` / `high` / `xhigh` / `max` / `none` |
| `model.rewrite_reasoning_effort` | str | `""` | Reasoning effort for rewrite mode (empty = off) |
| `model.rewrite_max_completion_tokens` | int | `64000` | Max tokens for rewrite |
| `model.codex_exec_path` | str | `codex` | Codex CLI path |
| `model.codex_exec_sandbox` | str | `workspace-write` | Sandbox mode |
| `model.codex_exec_full_auto` | bool | `false` | Full auto mode |
| `model.codex_exec_reasoning_effort` | str | `none` | Codex reasoning effort |
| `model.codex_exec_use_sdk` | str | `auto` | Use SDK vs CLI |
| `model.codex_exec_network_access` | bool | `false` | Allow network |
| `model.codex_exec_web_search` | bool | `false` | Allow web search |
| `model.codex_exec_approval_policy` | str | `never` | Approval policy |
| `model.codex_trace_to_optimizer` | bool | `true` | Route Codex traces to optimizer |
| `model.claude_code_exec_path` | str | `claude` | Claude CLI path |
| `model.claude_code_exec_effort` | str | `medium` | Claude effort |
| `model.claude_code_exec_max_thinking_tokens` | int | `16384` | Max thinking tokens |
| `model.minimax_base_url` | str | `""` | MiniMax endpoint |
| `model.minimax_api_key` | str | `""` | MiniMax API key |
| `model.minimax_model` | str | `MiniMax-M2.7` | MiniMax model |
| `model.minimax_enable_thinking` | str | `false` | Enable thinking |
| `model.azure_openai_endpoint` | str | `""` | Shared Azure endpoint |
| `model.azure_openai_api_key` | str | `""` | Shared Azure key |
| `model.azure_openai_api_version` | str | `2024-12-01-preview` | API version |
| `model.azure_openai_auth_mode` | str | `""` | Auth mode (empty = env fallback) |

Per-role overrides: `optimizer_azure_openai_*`, `target_azure_openai_*`, `optimizer_qwen_chat_*`, `target_qwen_chat_*`

### 4.2 Training Configuration

| Parameter | Type | Default | Description |
|---|---|---|---|
| `train.num_epochs` | int | `4` | Number of training epochs |
| `train.train_size` | int | `0` | 0 = auto-derive from dataset |
| `train.batch_size` | int | `40` | Tasks per rollout |
| `train.accumulation` | int | `1` | Gradient accumulation steps |
| `train.seed` | int | `42` | Random seed |

Computed: `steps_per_epoch = ceil(train_size / (batch_size * accumulation))`, `batches_per_epoch = steps_per_epoch * accumulation`, `total_steps = num_epochs * steps_per_epoch`

### 4.3 Gradient / Reflection Configuration

| Parameter | Type | Default | Description |
|---|---|---|---|
| `gradient.minibatch_size` | int | `8` | Trajectories per analyst group (M) |
| `gradient.merge_batch_size` | int | `8` | Patch merge batch size |
| `gradient.analyst_workers` | int | `16` | Parallel reflection workers |
| `gradient.max_analyst_rounds` | int | `3` | Max analyst reflection rounds |
| `gradient.failure_only` | bool | `false` | Only reflect on failures |

### 4.4 Optimizer Configuration

| Parameter | Type | Default | Description |
|---|---|---|---|
| `optimizer.learning_rate` | int | `4` | Max edits per step (edit_budget) |
| `optimizer.min_learning_rate` | int | `2` | Min edits for decay schedulers |
| `optimizer.lr_scheduler` | str | `cosine` | `constant` / `linear` / `cosine` |
| `optimizer.lr_control_mode` | str | `fixed` | `fixed` / `autonomous` / `none` |
| `optimizer.skill_update_mode` | str | `patch` | `patch` / `rewrite_from_suggestions` / `full_rewrite_minibatch` |
| `optimizer.use_slow_update` | bool | `true` | Epoch-boundary momentum |
| `optimizer.slow_update_samples` | int | `20` | Samples for slow update |
| `optimizer.slow_update_gate_with_selection` | bool | `false` | Gate slow updates on selection set |
| `optimizer.longitudinal_pair_policy` | str | `mixed` | `mixed` / `changed` / `unchanged` |
| `optimizer.use_meta_skill` | bool | `true` | Cross-epoch strategy memory |
| `optimizer.use_skill_aware_reflection` | bool | `false` | EmbodiSkill: SKILL_DEFECT vs EXECUTION_LAPSE routing |
| `optimizer.skill_aware_appendix_source` | str | `both` | `both` / `failure_only` |
| `optimizer.skill_aware_consolidate_threshold` | int | `0` | LLM-compact appendix past N notes |

### 4.5 Evaluation Configuration

| Parameter | Type | Default | Description |
|---|---|---|---|
| `evaluation.use_gate` | bool | `true` | Validation gating (false = force-accept all) |
| `evaluation.sel_env_num` | int | `0` | Selection set size (0 = all) |
| `evaluation.test_env_num` | int | `0` | Test set size (0 = all) |
| `evaluation.eval_test` | bool | `true` | Run test eval after training |
| `evaluation.gate_metric` | str | `hard` | `hard` / `soft` / `mixed` |
| `evaluation.gate_mixed_weight` | float | `0.5` | Weight for mixed metric |
| `evaluation.use_semantic_density` | bool | `false` | Semantic density gating |
| `evaluation.semantic_density_weight` | float | `0.05` | SD weight |
| `evaluation.leading_words` | str/list | `null` | Leading words for scoring |

### 4.6 Environment Configuration

| Parameter | Type | Default | Description |
|---|---|---|---|
| `env.name` | str | `""` | Benchmark name |
| `env.skill_init` | str | `""` | Path to initial skill file |
| `env.split_mode` | str | `ratio` | `ratio` / `split_dir` |
| `env.split_seed` | int | `42` | Split seed |
| `env.split_dir` | str | `""` | Pre-split directory |
| `env.data_path` | str | `""` | Dataset path |
| `env.split_output_dir` | str | `""` | Output for generated splits |
| `env.exec_timeout` | int | `120` | Per-task timeout (seconds) |
| `env.out_root` | str | `""` | Output root directory |

---

## 5. Source Code Architecture

### 5.1 Package Structure

```
skillopt/
├── engine/
│   └── trainer.py              # ReflACTTrainer (2,406 lines) — main training loop
├── evaluation/
│   └── gate.py                 # GateResult, evaluate_gate(), select_gate_score()
├── optimizer/
│   ├── clip.py                 # rank_and_select() — gradient clipping analog
│   ├── scheduler.py            # build_scheduler() — cosine/linear/constant LR schedulers
│   ├── skill.py                # apply_patch_with_report() — edit application
│   ├── slow_update.py          # run_slow_update() — epoch-boundary momentum
│   ├── meta_skill.py           # run_meta_skill() — cross-epoch memory
│   ├── rewrite.py              # rewrite_skill_from_suggestions() — full rewrite mode
│   ├── select.py               # Backward-compat stub → clip.py
│   ├── skill_aware.py          # EmbodiSkill: SKILL_DEFECT vs EXECUTION_LAPSE routing
│   ├── appendix.py             # Appendix field injection/extraction
│   ├── update_modes.py         # Mode normalization (patch/rewrite/full_rewrite)
│   └── lr_autonomous.py        # decide_autonomous_learning_rate()
├── gradient/
│   ├── reflect.py              # run_minibatch_reflect() — trajectory analysis
│   └── aggregate.py            # merge_patches() — hierarchical patch merging
├── model/
│   ├── __init__.py             # Router: chat_target(), chat_optimizer(), etc.
│   ├── router.py               # Backend dispatch
│   ├── common.py               # CompatAssistantMessage, tracker shared types
│   ├── backend_config.py       # get_optimizer_backend(), get_target_backend()
│   ├── azure_openai.py         # Azure OpenAI wrapper (915 lines) — TokenTracker, dual clients
│   ├── claude_backend.py       # Claude CLI backend (376 lines) — subprocess wrapper
│   ├── codex_backend.py        # Codex CLI backend
│   ├── codex_harness.py        # Codex execution harness
│   ├── qwen_backend.py         # Qwen/vLLM backend
│   ├── minimax_backend.py      # MiniMax backend
│   └── openai_compatible_backend.py  # Generic OpenAI-compatible
├── prompts/
│   ├── __init__.py             # load_prompt(name, env) — env-specific override + fallback
│   ├── analyst_error.md        # Failure analyst prompt
│   ├── analyst_error_rewrite.md / analyst_error_full_rewrite.md
│   ├── analyst_success.md      # Success analyst prompt
│   ├── analyst_success_rewrite.md / analyst_success_full_rewrite.md
│   ├── merge_failure.md / merge_failure_rewrite.md / merge_failure_full_rewrite.md
│   ├── merge_success.md / merge_success_rewrite.md / merge_success_full_rewrite.md
│   ├── merge_final.md / merge_final_rewrite.md / merge_final_full_rewrite.md
│   ├── ranking.md / ranking_rewrite.md
│   ├── rewrite_skill.md
│   ├── slow_update.md
│   ├── meta_skill.md
│   └── lr_autonomous.md
├── envs/
│   ├── base.py                 # EnvAdapter ABC (329 lines) — abstract interface
│   ├── alfworld/               # ALFWorld adapter (428 lines)
│   ├── searchqa/               # SearchQA adapter
│   ├── docvqa/                 # DocVQA adapter
│   ├── officeqa/               # OfficeQA adapter
│   ├── livemathematicianbench/ # LiveMathBench adapter
│   ├── spreadsheetbench/       # SpreadsheetBench adapter
│   └── _template/              # Skeleton for new adapters
├── datasets/
│   └── base.py                 # BaseDataLoader, SplitDataLoader, BatchSpec
├── types.py                    # Edit, Patch, RolloutResult, etc.
├── config.py                   # YAML config with _base_ inheritance
└── utils/
    ├── json_utils.py           # extract_json() — JSON extraction from LLM output
    └── scoring.py              # compute_score() — hard/soft scoring
```

### 5.2 Type System (`skillopt/types.py`)

```python
EditOp = Literal["append", "insert_after", "replace", "delete"]

@dataclass
class Edit:
    op: EditOp
    content: str = ""
    target: str = ""
    support_count: int | None = None
    source_type: Literal["failure", "success"] | None = None

@dataclass
class Patch:
    edits: list[Edit] = field(default_factory=list)
    reasoning: str = ""

@dataclass
class RawPatch:
    patch: dict
    source_type: str = "failure"
    batch_size: int = 1

@dataclass
class RolloutResult:
    id: str
    hard: int  # 0 or 1
    soft: float  # 0.0 to 1.0
    fail_reason: str = ""
    task_type: str = ""
    # ... additional env-specific fields
```

### 5.3 Prompt Loading (`skillopt/prompts/__init__.py`)

`load_prompt(name, env)` resolves prompts with env-specific override:
1. `skillopt/envs/{env}/prompts/{name}.md` (if env given)
2. `skillopt/prompts/{name}.md` (generic fallback)

Results are cached in-memory. Raises `FileNotFoundError` if neither path exists.

### 5.4 Environment Adapter Interface (`skillopt/envs/base.py`)

```python
class EnvAdapter(ABC):
    def setup(self, cfg: dict) -> None: ...           # One-time init
    def get_dataloader(self) -> BaseDataLoader | None: ...
    def requires_ray(self) -> bool: return False
    def build_train_env(self, batch_size, seed, **kw): ...
    def build_eval_env(self, env_num, split, seed, **kw): ...
    def rollout(self, env_manager, skill_content, out_dir, **kw) -> list[dict]: ...
    def reflect(self, results, skill_content, out_dir, **kw) -> list[dict | None]: ...
    def get_task_types(self) -> list[str]: ...
    def build_reference_text(self, item: dict) -> str: ...
    def get_reference_metadata(self, item: dict) -> dict: ...
    def attach_reference_context(self, results, items) -> list[dict]: ...
    def build_env_from_batch(self, batch: BatchSpec, out_root: str): ...
    def build_train_batch(self, batch_size, seed, out_root): ...
    def build_eval_batch(self, env_num, split, seed, out_root): ...
```

### 5.5 Model Backend System

**Dual-client architecture** (`skillopt/model/azure_openai.py`):
- `get_optimizer_client()` — AzureOpenAI or OpenAI client for optimizer
- `get_target_client()` — AzureOpenAI or OpenAI client for target
- `TokenTracker` — thread-safe per-stage token counter

**Public API functions** (all return `tuple[str, dict]` or `tuple[Any, dict]`):
- `chat_optimizer(system, user, ...)` — call optimizer model
- `chat_target(system, user, ...)` — call target model
- `chat_with_deployment(deployment, system, user, ...)` — call arbitrary deployment
- `chat_optimizer_messages(messages, ...)` — pre-built message list
- `chat_target_messages(messages, ...)` — pre-built message list
- `get_token_summary()` — per-stage and total token usage
- `set_reasoning_effort(effort)` — process-wide reasoning effort
- `set_target_deployment(deployment)` — change target at runtime
- `set_optimizer_deployment(deployment)` — change optimizer at runtime

**Auth modes** (Azure OpenAI):
- `api_key` — direct API key
- `azure_cli` — Azure CLI credential (fallback without azure-identity)
- `managed_identity` / `aad` / `azure_ad` — Azure AD token provider
- `openai_compatible` / `compat` / `openai` — OpenAI-compatible endpoint

**Responses API support**: Automatically detected for Codex models (`gpt-5.3-codex`, `gpt-5.1-codex`, `gpt-5-codex`, `codex-mini`, `gpt-5.4-pro`). Converts chat messages to Responses API format via `_messages_to_responses_input()`.

**Claude backend** (`skillopt/model/claude_backend.py`):
- Wraps Claude CLI (`claude -p --output-format json`)
- System prompt passed via `--append-system-prompt-file` (avoids Windows argv cap)
- Image attachments via temp directory + `--add-dir`
- Structured output via `--schema` flag
- Permission mode: `CLAUDE_PERMISSION_MODE` (default: `dontAsk`)

### 5.6 Skill-Aware Reflection (EmbodiSkill)

When `use_skill_aware_reflection=True`, failure/success analysts are augmented:

**Failure analyst** (`ERROR_SUFFIX`): Classifies each failure as:
- `SKILL_DEFECT`: Rule wrong/missing → body edit (normal patch)
- `EXECUTION_LAPSE`: Rule valid but agent didn't follow → appendix reminder

**Success analyst** (`SUCCESS_SUFFIX`): Labels edits as:
- `DISCOVERY`: New rule (typically append)
- `OPTIMIZATION`: Better way to perform existing rule (typically replace)

**Appendix consolidation** (`consolidate_appendix_notes()`): LLM-powered dedup/merge/compact when note count exceeds threshold. Mirrors GMemory `_maybe_refactor_execution_notes` and paper Eq.11.

**Runtime switch** (`configure_skill_aware_reflection(enabled, appendix_source)`): Set once at startup, affects all env adapters process-wide.

### 5.7 Update Modes

Three modes controlled by `optimizer.skill_update_mode`:

| Mode | Alias | Description |
|---|---|---|
| `patch` | `edits` | Individual edit operations (append/replace/delete/insert_after) |
| `rewrite_from_suggestions` | `rewrite`, `suggestions` | LLM rewrites full skill from suggestion list |
| `full_rewrite_minibatch` | `full_rewrite`, `minibatch_full_rewrite` | Selects best complete skill candidate from merged batch |

Mode normalization in `skillopt/optimizer/update_modes.py` handles aliases and payload key mapping.

---

## 6. Supported Benchmarks

| Benchmark | Type | Config | Difficulty | Runtime | Env Adapter |
|---|---|---|---|---|---|
| SearchQA | Open-domain QA | `configs/searchqa/` | Easy | ~30 min | `searchqa/adapter.py` |
| DocVQA | Document QA | `configs/docvqa/` | Medium | ~2 hours | `docvqa/adapter.py` |
| ALFWorld | Embodied AI | `configs/alfworld/` | Hard | ~3 hours | `alfworld/adapter.py` |
| OfficeQA | Enterprise QA | `configs/officeqa/` | Medium | ~2 hours | `officeqa/adapter.py` |
| LiveMathBench | Math reasoning | `configs/livemathematicianbench/` | Medium | ~2 hours | `livemathematicianbench/adapter.py` |
| SpreadsheetBench | Spreadsheet ops | `configs/spreadsheetbench/` | Medium | ~2 hours | `spreadsheetbench/adapter.py` |

Each benchmark has env-specific prompts that override generic prompts (e.g., `skillopt/envs/alfworld/prompts/rollout_no_history.md`).

---

## 7. Model Backends

| Backend | Optimizer | Target | Config Key | Notes |
|---|---|---|---|---|
| Azure OpenAI | Yes | Yes | `azure_openai` | Default, dual-client |
| OpenAI Chat | Yes | Yes | `openai_chat` | Via Azure client |
| Claude Chat | Yes | Yes | `claude_chat` | CLI subprocess |
| Qwen Chat (vLLM) | Yes | Yes | `qwen_chat` | Local inference |
| MiniMax Chat | Yes | Yes | `minimax_chat` | MiniMax API |
| OpenAI-Compatible | Yes | Yes | `openai_compatible` | Any OpenAI-compatible |
| Codex Exec | — | Yes | `codex_exec` | Codex CLI execution |
| Claude Code Exec | — | Yes | `claude_code_exec` | Claude CLI execution |

### Generic OpenAI-Compatible Backend

Works with DeepSeek, Groq, Together AI, Ollama, vLLM/SGLang/TGI, LiteLLM proxy, OpenRouter, Fireworks, xAI, etc.:

```bash
export TARGET_BACKEND=openai_compatible
export OPENAI_COMPATIBLE_BASE_URL="https://api.deepseek.com/v1"
export OPENAI_COMPATIBLE_API_KEY="sk-..."
export OPENAI_COMPATIBLE_MODEL="deepseek-chat"
```

### Backend Auto-Configuration

The trainer auto-configures optimizer/target backends based on `model.backend`:
- `claude` → both backends = `claude_chat`
- `codex` → optimizer = `openai_chat`, target = `codex_exec`
- `claude_code_exec` → optimizer = `openai_chat`, target = `claude_code_exec`
- `qwen` → optimizer = `openai_chat`, target = `qwen_chat`
- Default → both = `openai_chat`

---

## 8. Output Structure

```
outputs/<benchmark>/<run_id>/
├── config.json                    # Frozen config copy (redacted secrets)
├── history.json                   # Full training history (all step records)
├── runtime_state.json             # Resume state (last step, current/best skill paths)
├── best_skill.md                  # Final deployed artifact
├── skills/
│   ├── skill_v0000.md            # Initial skill
│   └── skill_vNNNN.md            # Skill snapshots after each step
├── steps/
│   └── step_NNNN/
│       ├── step_record.json      # Full step metrics (timing, tokens, action, scores)
│       ├── candidate_skill.md    # Candidate skill before gate
│       ├── trajectory_digest.json # Step buffer entry
│       ├── merged_patch.json     # Aggregated patches
│       ├── ranked_edits.json     # Selected patches after clipping
│       ├── rollout/              # Rollout artifacts
│       ├── patches/              # Individual minibatch patches
│       ├── selection_eval/       # Selection set evaluation
│       └── (lr_decision.json / rewrite_result.json / edit_apply_report.json)
├── slow_update/
│   └── epoch_NN/
│       ├── comparison_pairs.json # Longitudinal pair categories
│       ├── slow_result.json      # Slow update guidance
│       ├── candidate_skill.md    # Slow-updated candidate
│       └── selection_eval/       # Gated mode only
├── meta_skill/
│   └── epoch_NN/
│       └── meta_skill_result.json # Cross-epoch memory
├── test_eval_baseline/           # Initial skill on test set
├── test_eval/                    # Best skill on test set
├── test_eval_final/              # Final skill on test set
├── final_selection_eval/         # Final skill on selection set
└── summary.json                  # Global summary (all scores, timing, tokens)
```

---

## 9. Quick Start

```bash
# Train on SearchQA (~30 min)
python scripts/train.py --config configs/searchqa/default.yaml

# Evaluate best skill on test set
python scripts/eval_only.py \
  --config configs/searchqa/default.yaml \
  --skill outputs/searchqa/<run_id>/best_skill.md

# Override any config from CLI
python scripts/train.py \
  --config configs/searchqa/default.yaml \
  optimizer.learning_rate=16 optimizer.lr_scheduler=linear gradient.analyst_workers=8
```

---

## 10. Extending SkillOpt

### Adding a New Benchmark (~200 lines)

1. Create `skillopt/envs/<name>/` package with `__init__.py`
2. Implement `SplitDataLoader` subclass in `dataloader.py` (override `load_split_items`)
3. Write rollout helper in `rollout.py` (use `skillopt.model.chat_target`, score into `hard`/`soft`)
4. Implement `EnvAdapter` subclass in `adapter.py`
5. Register in `scripts/train.py` → `_register_builtins()`:
   ```python
   try:
       from skillopt.envs.<name>.adapter import MyAdapter
       _ENV_REGISTRY["<name>"] = MyAdapter
   except ImportError:
       pass
   ```
6. Create `configs/<name>/default.yaml` inheriting from `_base_/default.yaml`
7. Run: `python scripts/train.py --config configs/<name>/default.yaml`

Use `skillopt/envs/_template/` as a skeleton. Copy `skillopt/envs/officeqa/` as the best worked reference.

### Adding a New Backend

1. Create `skillopt/model/<name>_backend.py` implementing the standard API:
   - `chat_optimizer(system, user, ...) -> (text, usage_dict)`
   - `chat_target(system, user, ...) -> (text, usage_dict)`
   - `chat_optimizer_messages(messages, ...) -> (text, usage_dict)`
   - `chat_target_messages(messages, ...) -> (text, usage_dict)`
   - `get_token_summary() -> dict`
   - `reset_token_tracker() -> None`
   - `set_reasoning_effort(effort) -> None`
   - `set_target_deployment(deployment) -> None`
   - `set_optimizer_deployment(deployment) -> None`
2. Register in `skillopt/model/__init__.py` and `skillopt/model/backend_config.py`
3. Wire through router in `skillopt/model/__init__.py`

Templates: `qwen_backend.py`, `minimax_backend.py`. For OpenAI-compatible providers, use the built-in `openai_compatible` backend first.

---

## 11. Skill Documents

A skill document is a Markdown file encoding task-specific instructions — the "prompt weights" of the agent. During training it evolves via:

- **Additions**: New rules from failed trajectories (append)
- **Modifications**: Refining partially correct rules (replace)
- **Deletions**: Removing consistently wrong rules (delete)
- **Insertions**: Adding rules at specific positions (insert_after)

**Structure example:**
```markdown
# Task Strategy
## General Approach
- Break complex problems into sub-steps
- Always verify intermediate results
## Common Patterns
- When you see X, try approach Y
- Avoid Z because it leads to errors
## Edge Cases
- If the input contains A, handle it specially by...
## Output Format
- Always include reasoning before the answer
```

**Starting points:** empty skill (learn from scratch), seed skill (bootstrap with domain knowledge), or pre-trained skill (transfer from related benchmark). Configure via `env.skill_init`.

**Slow update field**: Injected at epoch boundary via `inject_empty_slow_update_field()` / `replace_slow_update_field()` / `extract_slow_update_field()` from `skillopt/optimizer/slow_update.py`.

**Appendix field**: Injected when skill-aware reflection is enabled via `inject_empty_appendix_field()` from `skillopt/optimizer/appendix.py`.

---

## 12. SkillOpt-Sleep — Nightly Self-Evolution

SkillOpt-Sleep applies SkillOpt's discipline to your own daily usage. A local coding agent gets a nightly **sleep cycle** that reviews past sessions, replays recurring tasks, and consolidates what it learns into validated long-term memory — behind a held-out gate.

### Architecture

The engine lives in `skillopt_sleep/` with **zero dependency** on the research `skillopt/` package (the validation gate is vendored). One engine, four thin shells.

```
skillopt_sleep/
├── cycle.py          # run_sleep_cycle() — orchestrator
├── harvest.py        # Session harvesting
├── harvest_sources.py # Config-driven harvest routing
├── harvest_codex.py  # Codex-specific harvesting
├── mine.py           # Task mining from sessions
├── llm_miner.py      # LLM-assisted task mining
├── replay.py         # Task replay (mock/fresh)
├── dream.py          # Dream consolidation
├── judges.py         # Quality judges
├── gate.py           # Validation gate (vendored)
├── consolidate.py    # Memory consolidation
├── staging.py        # Proposal staging
├── adopt.py          # Live file adoption
├── memory.py         # CLAUDE.md/SKILL.md memory management
├── slow_update.py    # Epoch-level slow updates
├── scheduler.py      # Nightly cron scheduling
├── config.py         # SleepConfig with defaults
├── state.py          # SleepState persistence
├── types.py          # SleepReport, TaskRecord, SessionDigest
├── backend.py        # Backend abstraction (mock/claude/codex/copilot/handoff)
├── handoff_backend.py # Session-executed calls
├── budget.py         # Token/time budget management
├── tasks_file.py     # Task persistence
└── __main__.py       # CLI entry point
```

### The cycle (six stages)

```
harvest session transcripts  ->  mine recurring task patterns
                              ->  replay each pattern under current skill
                              ->  reflect on failures -> propose bounded edits
                              ->  GATE: must improve held-out score
                              ->  stage proposal
                              ->  user adopts (manual, with backup)
```

**Nothing live changes until the user adopts.** Every adopt backs up the prior file first.

### CLI

```bash
skillopt-sleep status      # nights so far + latest staged proposal (read-only)
skillopt-sleep dry-run     # harvest → mine → replay → report (stages nothing)
skillopt-sleep run         # full cycle; stages a proposal (nothing live changes)
skillopt-sleep adopt       # apply staged proposal (backs up first)
skillopt-sleep harvest     # debug: print mined tasks
skillopt-sleep schedule    # install nightly cron entry
skillopt-sleep unschedule  # remove cron entry
```

- Default backend is `mock` (deterministic, **no API spend**) — good for trying the plumbing.
- Add `--backend claude` or `--backend codex` to spend the user's real budget for genuine improvement.
- Always show the user the **held-out baseline → candidate** score and the exact proposed edits before suggesting adoption.

### Plugins

| Platform | Folder | Mechanism | Install |
|---|---|---|---|
| Claude Code | `plugins/claude-code/` | `.claude-plugin` + commands + skill + hooks | `/plugin marketplace add microsoft/SkillOpt` → `/plugin install skillopt-sleep` |
| Codex | `plugins/codex/` | User-level skill + shared runner | `bash plugins/codex/install.sh` |
| Copilot | `plugins/copilot/` | MCP server (`sleep_*` tools) + `copilot-instructions` | Register `plugins/copilot/mcp_server.py` as MCP server |
| Devin | `plugins/devin/` | MCP server (`sleep_*` tools) + ATIF-v1.7 harvest | `devin mcp add skillopt-sleep -- python3 plugins/devin/mcp_server.py` |

### Key Flags

| Flag | Default | Meaning |
|---|---|---|
| `--backend mock\|claude\|codex\|copilot\|handoff` | `mock` | Who runs/optimizes |
| `--preferences "..."` | — | House rules as prior |
| `--gate on\|off` | `on` | Strict held-out gate vs. greedy |
| `--rollouts-k K` | `1` | Multi-rollout contrastive reflection |
| `--optimizer-model` / `--target-model` | — | Split optimizer from target |
| `--budget-tokens` / `--budget-minutes` | — | Cap nightly spend |
| `--scope invoked\|all` | `invoked` | This project only or all |
| `--auto-adopt` | off | Apply without manual review |

### Sleep Split Protocol

| Split | Source | Purpose |
|---|---|---|
| **train** | Real tasks + optional dreamed variants | What optimizer learns from |
| **val** (selection) | Real tasks only, held out | Gate: edit kept only if this score rises |
| **test** | Real tasks only, held out, never seen during optimization | Final reported score |

Dream tasks can NEVER land in val or test — this invariant is unit-tested.

### SleepConfig Defaults

```python
DEFAULTS = {
    "transcript_source": "claude",
    "projects": "invoked",
    "lookback_hours": 72,
    "max_tasks_per_night": 40,
    "max_tokens_per_night": 400_000,
    "val_fraction": 0.34,
    "test_fraction": 0.0,
    "backend": "mock",
    "gate_mode": "on",
    "edit_budget": 4,
    "dream_rollouts": 1,
    "dream_factor": 0,
    "recall_k": 0,
    "evolve_memory": True,
    "evolve_skill": True,
    "llm_mine": True,
    "auto_adopt": False,
    "managed_skill_name": "skillopt-sleep-learned",
    "redact_secrets": True,
    "seed": 42,
}
```

Config resolution: built-in DEFAULTS → `~/.skillopt-sleep/config.json` → explicit overrides.

### Results

- **gbrain-evals `skillopt-v1`**: Deficient skills go **0.00 → 1.00** on all 4 seeds
- **SearchQA** (1,400-item held-out): recall_k=20 → **+4.5 pts** (0.803 → 0.848)
- **SpreadsheetBench** (280-item held-out): **+3.6 pts** (0.279 → 0.314)
- Deterministic proof (no API key): `python -m skillopt_sleep.experiments.run_experiment --persona researcher --assert-improves`

---

## 13. WebUI Dashboard

```bash
pip install -e ".[webui]"
python -m skillopt_webui.app [--port 7860] [--host 0.0.0.0] [--share]
```

Open `http://localhost:7860` to configure parameters, launch training, and monitor progress in-browser.

---

## 14. Hyperparameter Transfer Rules

**What transfers from DL intuition:**
- Cosine schedule > constant (same convergence benefits)
- Moderate LR (4–16) > very high/low
- Slow update helps (prevents catastrophic forgetting across epochs)
- Meta skill memory improves reflection (cross-epoch strategy notes)

**What doesn't transfer:**
- Batch size ≠ better (diminishing returns due to API costs)
- More epochs ≠ better (skills converge faster than neural nets; 2–4 epochs usually enough)

---

## 15. Local Environment Smoke Tests

```bash
python -m py_compile scripts/train.py skillopt/envs/myenv/adapter.py
python scripts/train.py --config configs/myenv/tiny_mock.yaml
```

Use a tiny fixture split with `mock: true` in the adapter. Validate optimizer JSON before returning it. Keep configs CI-friendly with `train.num_epochs: 1`, `batch_size: 3`, `analyst_workers: 1`.

---

## 16. Development

```bash
git clone https://github.com/microsoft/SkillOpt.git
cd SkillOpt
pip install -e ".[dev]"

# Lint
ruff check .

# Tests
pytest tests/

# Docs
pip install -e ".[docs]"
mkdocs serve  # http://localhost:8000
```

**Code style:** 120-char lines, Python 3.10+, type hints, ruff for linting (E/F/I/W rules, E501 ignored).

---

## Hard Rules

- **Never** hand-edit the user's CLAUDE.md / SKILL.md / AGENTS.md as part of SkillOpt-Sleep. Only the `adopt` action changes live files, and it backs them up first.
- Harvest is **read-only**. `mock` replay has no side effects. Do not edit archived sessions or raw transcripts.
- Always show the user the **held-out baseline → candidate** score and the exact proposed edits before suggesting adoption. Evidence before adoption.
- Treat generated edits as **proposals**, not as source of truth.
- Keep raw secrets, credentials, private user data, and unsanitized transcript contents out of messages, logs, generated artifacts, and commits.
- If the SkillOpt training loop is running, do not interrupt or modify the skill file manually — let the gate decide.
- For SkillOpt-Sleep, **nothing live changes** until the user explicitly adopts. The cycle stages proposals; the user is in control of adoption.
- Do not rely on deprecated custom prompts or slash commands for plugin integrations. The skill file is the entrypoint.

---

## When NOT to use this skill

- For a **one-off prompt edit** — SkillOpt is for systematic, validated optimization, not quick fixes.
- When the user has **no evaluation data** — the gate needs a held-out set to validate against.
- During a **crisis or incident** — humans must lead; automated skill changes are too risky.
- For skills **smaller than ~300 tokens** — over-optimization risk; there isn't enough signal.
- When session transcripts are **< 24 hours old** — not enough signal for meaningful task mining.
- When the user wants to **modify model weights** — SkillOpt works in text space only.

---

## 17. Citation

```bibtex
@article{yang2026skillopt,
  title={Skillopt: Executive strategy for self-evolving agent skills},
  author={Yang, Yifan and Gong, Ziyang and Huang, Weiquan and Yang, Qihao and Zhou, Ziwei and Huang, Zisu and Li, Yan and Gao, Xuemei and Dai, Qi and Liu, Bei and others},
  journal={arXiv preprint arXiv:2605.23904},
  year={2026}
}
```
