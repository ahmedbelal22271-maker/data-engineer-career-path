---
name: opencode Agent Instructions Guide (AGENTS.md)
description: Guide for opencode itself on how to customize and update its own AGENTS.md file. The primary trigger is when the user tells opencode to "adjust your AGENTS.md", "update your instructions", "change how you behave", "modify AGENTS.md", or "edit your agent file". Also covers how to structure project instructions, what to include, behavioral patterns, file locations and precedence, opencode.json configuration, naming conventions, verification steps, escalation rules, and maintenance tips. Use this whenever the user is writing, editing, or asking about AGENTS.md, CLAUDE.md, or any opencode/Claude instruction file.
---

# How to Customize AGENTS.md for Your Preferences

This file controls how the AI agent behaves in this project. OpenCode automatically loads it into the agent's system prompt at session start — no commands needed.

---

## What Goes in AGENTS.md

Anything you want the agent to **always know or follow** when working here:

| Category | Examples |
|----------|----------|
| Project conventions | File naming, directory layout, coding style, framework choices |
| Build/test/lint commands | `npm run build`, `pytest tests/`, `ruff check .` |
| Architecture overview | How modules relate, data flow, key design decisions |
| Behavioral rules | How the agent should approach tasks, respond, or escalate |
| Reference paths | Pointers to important docs, schemas, or config files |
| Gotchas | Setup quirks, known issues, things that often go wrong |

---

## Writing Effective Instructions

### Be Specific and Actionable

| Instead of | Write |
|------------|-------|
| "Write good code" | "Use async/await, not raw promises. Prefer `Result<T>` over throwing exceptions." |
| "Run tests" | "Run `pnpm test --run` before every commit. Fix all failures before asking for review." |
| "Follow the style" | "Use 2-space indentation, single quotes, trailing commas." |

### Use a Hierarchical Structure

```markdown
# Project Name

## Repository Structure
Brief high-level map of directories and what lives where.

## Development Workflow
1. Steps to build
2. Steps to test
3. Steps to lint

## Code Standards
- Naming conventions
- Imports ordering
- Error handling patterns

## Operational Rules
- Hard constraints the agent must never violate
- Always-do and never-do lists

## Reference Files
Paths to important documents the agent should read when relevant
```

### Reference External Files

Tell the agent to load specific files when needed:

```markdown
## Reference Files
When working on the pipeline, load `.agents/protocols/large_files_protocol.md`
When asked about Todoist, load the `todoist_tasks` skill (`.agents/skills/todoist_tasks/SKILL.md`)
```

Or use `opencode.json` with glob patterns (see below).

---

## File Locations & Precedence

OpenCode checks these paths in order (first match wins):

1. `./AGENTS.md` — project root (this file)
2. `./CLAUDE.md` — Claude Code fallback (only if no AGENTS.md exists)
3. `~/.config/opencode/AGENTS.md` — global rules for all projects
4. `~/.claude/CLAUDE.md` — global fallback

**Project rules + global rules are combined**, not mutually exclusive.

---

## Using opencode.json to Include More Files

### Where to Put It

Place `opencode.json` (or `opencode.jsonc`) in the **project root directory** — same level as this file:

```
project-root/
├── .agents/              # your instruction files
│   ├── AGENTS.md
│   ├── protocols/
│   └── skills/
├── opencode.json         # <-- create this file here
├── package.json
└── ...
```

OpenCode also checks `~/.config/opencode/opencode.json` for global settings, but project-level settings go in the root.

### What to Put Inside

If you keep instructions in multiple files (like your `.agents/` directory), reference them via the `instructions` field:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    ".agents/AGENTS.md",
    ".agents/protocols/*.md",
    ".agents/skills/*.md"
  ]
}
```

Glob patterns (`*`, `**`) are supported. All matched files are combined into the agent's context alongside any root `AGENTS.md`.

Remote URLs also work:

```json
{
  "instructions": ["https://raw.githubusercontent.com/org/shared-rules/main/style.md"]
}
```

---

## Behavioral Patterns That Work Well

### Session-Start Mandates
Hard rules the agent must follow on every operation:

```markdown
## Mandatory Check
Before writing any file, always run `git status` and `git diff` to understand current state.
```

### Verification Steps
Tell the agent how to verify its own work:

```markdown
## Verification
After making changes, run `npm run typecheck && npm run lint`. Fix any errors before reporting completion.
```

### Escalation Rules
When the agent should stop and ask:

```markdown
## When to Ask
- If a task would delete or overwrite files, ask for confirmation first.
- If you're unsure about the right directory, ask before proceeding.
```

### Naming Convention Enforcement

```markdown
## Naming
- Components: PascalCase (`UserProfile.tsx`)
- Utilities: camelCase (`formatDate.ts`)
- Constants: UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`)
- Test files: `*.test.ts` co-located with source
```

---

## Maintenance Tips

- **Keep it concise** — every line costs tokens. Remove outdated rules.
- **Commit it to Git** — share with your team. Run `/init` in OpenCode to auto-generate or refresh it.
- **Use `opencode.json` `instructions`** for large reference files and globs to keep AGENTS.md lean.
- **Revisit quarterly** — as the project evolves, update conventions and commands.
- **Test with a dry run** — ask the agent "read AGENTS.md and summarize what you understand" to verify it parses correctly.

---

## Example: Minimal Starter

```markdown
# My Project

## Commands
- Build: `npm run build`
- Test: `npm run test`
- Lint: `npm run lint`

## Structure
- `src/` — application source
- `tests/` — test files
- `docs/` — documentation

## Rules
- Always run lint before committing.
- Use TypeScript strict mode.
- Never commit to `main` directly — use PRs.
```

---

## Example: Adding Pipeline-Specific Instructions

Since this project uses `.agents/` for protocols and skills, you can delegate via the instructions field:

```json
{
  "instructions": [".agents/AGENTS.md"]
}
```

And in this file, just keep the high-level behavioral preferences and delegate detailed pipeline logic to your `.agents/` files.

---

## Full Documentation
For the complete official opencode agent instructions documentation, see `full_docs.md` in this directory. It contains exhaustive coverage of AGENTS.md structure, rules, skills, behavioral patterns, file precedence, config examples, and maintenance tips.

---

## Key Takeaway

**AGENTS.md is your lever** for shaping agent behavior without repeating yourself in every prompt. Put in the conventions, commands, and constraints you want applied consistently. The agent will follow them as if they were system instructions.
