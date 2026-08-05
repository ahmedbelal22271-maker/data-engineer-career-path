---
name: opencode Decision Trees — Best Approach Selector
description: Structured decision logic for choosing the optimal opencode approach for any task. Covers 9 decision trees: Mode Selection (Plan vs Auto vs opencode run), Agent Selection (which of 7 agent types), Tool Selection (which tool + workflow sequence), Instructions Strategy (AGENTS.md vs rules vs skills vs inline vs scripts vs agent instructions), Integration Decision (MCP vs ACP vs GitHub vs IDE vs SDK vs SSH vs LSP), Model Selection (Opus vs Sonnet vs Haiku vs GPT vs Gemini vs Ollama), Permission Strategy (bypass vs non-bypass vs rules vs flags), Output Format (terminal vs json vs markdown vs html vs edit), and Error Recovery (diagnostic tree for each failure type). Also includes a Common Scenarios quick-reference table mapping 20+ user requests to recommended approaches. Trigger on "best way to", "which approach", "what's the optimal", "how should I", "recommend a", or any strategic decision question about using opencode.
---

# opencode Decision Trees — Best Approach Selector

## 1. Mode Selection: Plan vs Auto vs opencode run

### Flowchart (text-based):

```
                    ┌─────────────────────────────┐
                    │     What kind of task?       │
                    └─────────────┬───────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
        High-risk             Routine            Repeatable
        Poorly-defined        Well-defined        Scheduled
        Architecture          Low-risk            Scripted
        Needs user input      One-off             Fully automated
        Exploration
              │                   │                   │
              ▼                   ▼                   ▼
         Plan Mode            Auto Mode         opencode run
        (read-only)         (read + write)    (no interaction)
```

### Decision Table

| Scenario | Mode | Rationale |
|---|---|---|
| "Review my architecture" | Plan | Read-only, analytical |
| "Fix this bug" | Auto | Well-defined, needs write |
| "Explore the codebase" | Plan | Research only |
| "Deploy to production" | Plan then Auto | High-risk → review → execute |
| "Add a unit test" | Auto | Routine |
| "Weekly report" | opencode run | Scheduled, scripted |
| "I'm not sure what I need" | Plan | Ambiguous, explore first |
| "Refactor across 50 files" | Plan then Auto | Plan first, execute staged |
| "Migrate database schema" | Plan then Auto | Risk assessment → migrate |
| "Lint and format all files" | Auto | Fully automated, safe |
| "Security audit" | Plan | Read-only review |
| "Generate documentation" | Plan then Auto | Outline first → generate |

## 2. Agent Selection Chart

### Agent Selection Matrix

| Task Characteristic | Best Agent | Why |
|---|---|---|
| Write new feature | code | Full tool access, focused on implementation |
| Refactor existing code | code | Read + edit + test workflow |
| Fix a bug | debug | Systematic root-cause analysis |
| Design database schema | architect | Analytical, read-only by default |
| Choose tech stack | architect | Weighs tradeoffs, presents options |
| Find where X is used | explore | Fast, limited toolset |
| Understand project structure | explore | Efficient glob/grep/read |
| Diagnose test failure | debug | Systematic debugging |
| Build frontend component | frontend | Specialized for UI |
| Research library API | ask | Web search + read + synthesis |
| Create documentation | ask or general | Research + writing |
| Multi-step complex task | general | Full tool access, flexible |
| Security audit | architect then code | Review first, then fixes |
| Performance optimization | debug | Profile → identify → fix |
| Write a shell script | code | Implementation focused |
| Answer conceptual question | ask | Research + synthesis |
| Review code quality | architect or ask | Analysis + recommendations |
| Set up CI/CD pipeline | code | Implementation with bash |

### Agent Hierarchy (fallback order):
```
general → code → debug → architect → explore → frontend → ask
```
If a specialized agent fails, fall back to `general` for maximum flexibility.

## 3. Tool Selection Matrix

### Single Tool Decisions

| Need | Best Tool |
|---|---|
| Find files by name | glob |
| Search file contents | grep |
| Read a file | read |
| Create/overwrite file | write |
| Make precise edit | edit |
| Run command | bash |
| Search web | web_search |
| Fetch URL | web_fetch |
| Delegate subtask | task |
| Ask user | question |
| Track progress | todowrite |
| Load knowledge | skill |

### Multi-Tool Workflow Patterns

| Goal | Sequence |
|---|---|
| Understand feature | glob → grep → read |
| Fix a bug | grep → read → edit → bash |
| Add new file | glob → read → write |
| Refactor function | grep → read → edit → edit → bash |
| Research + implement | web_search → web_fetch → write → bash |
| Explore unknown codebase | glob → read → todowrite |
| Complex multi-file change | todowrite → task → verifier |
| Generate report | read → web_search → write |
| Debug flaky test | grep → read → bash → edit → bash |
| Database schema change | read → edit → bash → bash |

## 4. Instructions Strategy

### Where should a directive live?

| Lifespan | Scope | Mechanism |
|---|---|---|
| Permanent, project-wide | Entire project | AGENTS.md (instructions config) |
| Permanent, per-tool | Specific tools | .opencode/rules/ |
| Until removed | Task-triggered | SKILL.md |
| Single turn | Current message | Inline prompt |
| Until deleted | Task run | opencode run script |
| Permanent, per-agent | Specific agent | Agent config instructions |

### Promotion Flow

```
Inline prompt (experiment)
       │
       ▼ (used 2+ times)
AGENTS.md (project-wide rule)
       │
       ├──► SKILL.md (if trigger-matched, reusable across projects)
       │
       ├──► .opencode/rules/ (if permission/tool restriction)
       │
       └──► Agent config instructions (if agent-specific)
```

### Decision Questions

1. **Is this a one-off?** → Inline prompt. Stop.
2. **Will I need this again in this project?** → AGENTS.md
3. **Does this apply across multiple projects?** → SKILL.md
4. **Is this a permission/tool restriction?** → .opencode/rules/
5. **Is this fully automated?** → opencode run script

## 5. Integration Decision Tree

```
               ┌──────────────────────────────┐
               │    What are you connecting?   │
               └──────────────┬───────────────┘
                              │
    ┌─────────────┬───────────┼───────────┬─────────────┬─────────────┐
    ▼             ▼           ▼           ▼             ▼             ▼
External      Another     GitHub/    Editor     Custom      Remote
tool/service  AI agent   Git/CI     (VS Code,  function    machine
                          Actions    JetBrains)
    │             │           │           │             │             │
    ▼             ▼           ▼           ▼             ▼             ▼
   MCP           ACP      GitHub       IDE          SDK or        SSH
                        integration   extension     Plugin
                        + gh CLI
```

| Need | Approach |
|---|---|
| External tool/service | MCP (Model Context Protocol) |
| Another AI agent | ACP (Agent Communication Protocol) |
| GitHub (PR, issues, Actions) | GitHub integration + gh CLI |
| Editor (VS Code, JetBrains) | IDE extension/plugin |
| Custom functionality | SDK or Plugin |
| Remote machine | SSH |
| Language intelligence | LSP |

## 6. Model Selection

| Constraint | Recommended | Rationale |
|---|---|---|
| Maximum reasoning | Claude Opus / Fable 5 | Best at deep analysis |
| Balance speed/quality/cost | Claude Sonnet 4.6 | Best all-rounder |
| Max speed/min cost | Claude Haiku / GPT-4o-mini | Fastest/cheapest |
| Very large context (1M+) | Gemini 2.5 Pro | Massive context window |
| Offline/no internet | Ollama (Llama 3, Qwen) | Runs locally |
| Cost primary | Haiku, GPT-4o-mini, Gemini Flash | Lowest token cost |
| Max output length | Claude Opus (16K tokens) | Largest output tokens |
| Code generation | Sonnet or Opus | Best code quality |
| Multimodal (images) | Gemini or GPT-4o | Strong vision capabilities |
| Low latency API | Haiku or GPT-4o-mini | Sub-second responses |
| Reasoning + tools | Sonnet 4.6 (default) | Best tool-use balance |

### Cost-Performance Curve

```
Cheapest ──────────────────────────────────────────── Most expensive
Haiku ── GPT-4o-mini ── Gemini Flash ── Sonnet 4.6 ── Opus / Fable 5
  │            │               │              │               │
 Fast        Fastest        Balanced       Balanced      Best reasoning
```

## 7. Permission Strategy

| Risk Level | Mode | Flags |
|---|---|---|
| Low risk, trusted | bypass | --yes |
| Normal | default | (none) |
| High risk | non-bypass | --no |
| Custom | rules-based | Configure rules + policies |
| Selective read | default + --allow-read | --allow-read |
| Full automation | bypass + --yes | --yes --allow-read --allow-write --allow-exec |

### Permission Decision Flow

```
                   ┌─────────────────────────────┐
                   │    What's the risk level?    │
                   └─────────────┬───────────────┘
                                 │
            ┌────────────────────┼────────────────────┐
            ▼                    ▼                    ▼
        Low risk             Normal risk          High risk
        Trusted              Mixed ops            Destructive
            │                    │                    │
            ▼                    ▼                    ▼
       bypass mode          default mode         non-bypass mode
       --yes flag           (ask per op)         --no flag
            │                    │                    │
            ▼                    ▼                    ▼
    ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
    │ Full speed    │   │ Safe default  │   │ Max safety    │
    │ No prompts    │   │ User controls │   │ Must confirm  │
    │ CI/cron only  │   │ Each action   │   │ Each action   │
    └───────────────┘   └───────────────┘   └───────────────┘
```

## 8. Output Format Selection

| Consumer | Format |
|---|---|
| Human in terminal | terminal (default) |
| Another program / CI | json or jsonl |
| Documentation / wiki | markdown or html |
| Code review | edit (changes only) |
| Web publishing | html (self-contained) |
| Both human + structured | terminal + json |
| Debugging | verbose |
| Minimal output | terminal --no-progress |

### Format Decision Flow

```
Who is consuming the output?
    │
    ├── Human at CLI ──────► terminal (default)
    ├── Human reading doc ─► markdown or html
    ├── CI pipeline ───────► json
    ├── Another program ───► json or jsonl
    ├── Code reviewer ─────► edit (diff only)
    └── Web audience ──────► html (self-contained)
```

## 9. Error Recovery Tree

### Tool Call Failures

| Error | Diagnostic | Resolution |
|---|---|---|
| edit "oldString not found" | Stale file cache | Read file fresh, match exact content with context |
| edit "multiple matches" | Ambiguous pattern | Add more surrounding context or use replaceAll |
| API 401 | Auth failure | Check API key → retry → fallback model |
| API 429 | Rate limited | Wait → reduce concurrency → check plan limits |
| Bash "not found" | Missing dependency | Install tool or use different approach |
| Write "not read first" | Safety check | Read file before writing |
| Permission denied | Rule restriction | Check rules, adjust mode, or --yes |
| Glob no results | Wrong pattern | Broaden pattern or check path |
| Task timeout | Too long | Reduce scope or increase timeout |

### Session Issues

| Symptom | Action |
|---|---|
| Hung session | Ctrl+C → re-prompt with clearer instructions |
| Corrupted config | opencode config validate → opencode config edit |
| Model errors | Ctrl+/ switch model → restart with --model |
| Lost work | /save → check .opencode/logs/ |
| Endless loop | Ctrl+C → /compact → restart with tighter constraints |
| Tool misuse | Review recent output → adjust prompt strategy |
| Unexpected edits | Undo with git → restrict permissions → retry |

### Recovery Flow

```
Error occurs
    │
    ├──► Is it a tool error?
    │       ├── Edit: Read file fresh, re-match
    │       ├── Bash: Check PATH, dependencies
    │       └── API: Retry, switch model, or fallback
    │
    ├──► Is it a permission error?
    │       ├── Check .opencode/rules/
    │       ├── Adjust mode (bypass vs non-bypass)
    │       └── Use --yes, --allow-read/write/exec
    │
    └──► Is it a session issue?
            ├── Ctrl+C to break
            ├── /compact to reset context
            └── Restart with stricter instructions
```

## 10. Common Scenarios Quick-Reference

| User says | Recommended approach |
|---|---|
| "Find all TypeScript interfaces" | glob for *.ts → grep for "interface " |
| "Fix bug but not sure where" | grep error msg → explore agent → code agent |
| "Automate weekly report" | Create opencode run script → cron/GitHub Actions |
| "Review this PR" | GitHub integration → opencode run with PR script |
| "Set up my config" | Edit opencode.json → opencode config validate |
| "Connect to database" | MCP server → configure in opencode.json |
| "This command is dangerous" | .opencode/rules/never/ rule with pattern |
| "How do I...?" | ask subagent |
| "Create a new skill" | opencode_skill_authoring → skill tool → check |
| "Model keeps failing" | Troubleshoot → switch model → reduce context |
| "Explain architecture" | architect subagent with Plan Mode |
| "Run this daily" | opencode run + cron/scheduler |
| "Show me changes" | --output-format edit or /diff |
| "Share this analysis" | --output-format html → opencode share |
| "Keep it simple/cheap" | Haiku model, limit max_tokens, reduce tool calls |
| "Fix permission error" | Check rules, adjust mode, use --yes |
| "Refactor large codebase" | Plan → staged Auto, use task for parallel work |
| "What's the best way to X?" | Load this skill → follow decision tree |
| "Which agent should I use?" | Consult Agent Selection Matrix (§2) |
| "How do I structure instructions?" | Follow Instructions Strategy (§4) |

## Full Documentation
For the complete official opencode decision trees documentation, see `full_docs.md` in this directory. It contains exhaustive coverage of all 9 decision trees with flowcharts, decision tables, and common scenarios quick-reference.

---

**Cross-references:** All other `opencode_*` skills. This skill is the strategic router — consult it first before delegating to specialized skills.
