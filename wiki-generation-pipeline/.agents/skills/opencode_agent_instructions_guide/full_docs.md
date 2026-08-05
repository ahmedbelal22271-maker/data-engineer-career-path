# OpenCode Agent Instructions Guide — Complete Official Documentation

> **Source:** https://opencode.ai — compiled from docs/agents, docs/rules, docs/config, docs/skills — retrieved July 2026

---

## Overview

This guide covers how to customize and update OpenCode's own instruction files — AGENTS.md (or CLAUDE.md), SKILL.md files, opencode.json configuration, and the `.opencode/` directory. This is the meta-skill: how to configure the agent itself.

---

## AGENTS.md — The Primary Instruction File

AGENTS.md is the primary instruction file for OpenCode. It sits at the project root and defines behavioral rules, workflows, and context for the AI.

### File Location

```
my-project/
├── AGENTS.md           # Primary instructions (this file)
├── opencode.json       # Configuration
├── src/
└── .opencode/
    ├── rules/          # Behavioral rules
    └── skills/         # Domain skills
```

### Naming Convention

- **AGENTS.md** — Primary name (recommended)
- **CLAUDE.md** — Also supported (backward compatibility)
- **.opencode/AGENTS.md** — Project-level variant

### What to Include

AGENTS.md should contain:

1. **Project overview** — What the project is, tech stack, goals
2. **Behavioral rules** — How the AI should behave
3. **Coding standards** — Style, conventions, patterns
4. **Workflow instructions** — How to handle common tasks
5. **File structure** — Where things live
6. **Testing requirements** — How to test changes
7. **Deployment rules** — How/when to deploy

### Structure Template

```markdown
# Project Name

## Overview
Brief description of the project.

## Tech Stack
- Language: TypeScript
- Framework: Next.js
- Database: PostgreSQL
- Testing: Jest

## Behavioral Rules
1. Always run tests before committing
2. Use conventional commit messages
3. Never modify migration files

## Coding Standards
- Use TypeScript strict mode
- Prefer named exports
- Use functional components

## File Structure
- `src/components/` — React components
- `src/lib/` — Utility functions
- `src/api/` — API routes
- `tests/` — Test files

## Testing
- Write unit tests for all new functions
- Run `npm test` before committing
- Aim for >80% coverage

## Deployment
- Production deploys on merge to main
- Use semantic versioning
```

---

## opencode.json — The Configuration File

opencode.json defines models, providers, tools, permissions, MCP servers, and skills.

### Minimal Config

```json
{
  "model": {
    "primary": "anthropic/claude-sonnet-4-6"
  }
}
```

### Full Config

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["AGENTS.md"],
  "model": {
    "primary": "anthropic/claude-sonnet-4-6",
    "big": "anthropic/claude-sonnet-4-6"
  },
  "provider": {
    "anthropic": {
      "apiKey": "env:ANTHROPIC_API_KEY"
    }
  },
  "tools": {
    "always": ["read", "glob", "grep"],
    "ask": ["write", "edit", "bash"]
  },
  "mcp": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-github"]
    }
  },
  "skill": {
    "my-skill": {
      "path": ".opencode/skills/my-skill",
      "description": "My custom skill",
      "trigger": "use when doing X"
    }
  }
}
```

---

## .opencode/ Directory Structure

```
.opencode/
├── config.json         # Project-level config override
├── rules/              # Behavioral rules
│   ├── security.md     # Security rules
│   ├── testing.md      # Testing rules
│   └── style.md        # Style rules
├── skills/             # Domain skills
│   ├── api-docs/
│   │   └── SKILL.md
│   └── code-review/
│       └── SKILL.md
└── plugins/            # Custom plugins
    └── my-plugin/
        └── plugin.json
```

---

## File Precedence

When multiple sources define the same setting:

1. **CLI flags** — Highest priority
2. **Environment variables** — Second
3. **`.opencode/config.json`** — Project-level override
4. **`opencode.json`** — Project root config
5. **`~/.config/opencode/config.json`** — User-level defaults
6. **Built-in defaults** — Lowest priority

For rules:
1. **Project rules** (`.opencode/rules/`) — Override user rules
2. **User rules** (`~/.config/opencode/rules/`) — Global defaults

For skills:
1. **Project skills** (`.opencode/skills/`) — Always available
2. **User skills** (`~/.config/opencode/skills/`) — Global skills

---

## Writing AGENTS.md — Best Practices

### 1. Be Specific

**Bad:**
```markdown
Write good code.
```

**Good:**
```markdown
- Use TypeScript strict mode
- Prefer `const` over `let`
- Use early returns for guard clauses
- Name functions verb-first (e.g., `getUserById`, `calculateTotal`)
```

### 2. Structure for Scannability

Use headers, lists, and code blocks. The AI reads the entire file but references it by section.

### 3. Include Examples

```markdown
## Commit Messages
Use conventional commits:
- `feat: add user authentication`
- `fix: resolve login timeout`
- `docs: update API reference`
- `refactor: extract validation logic`
```

### 4. Define Boundaries

```markdown
## Do NOT
- Do not modify migration files
- Do not commit directly to main
- Do not use `any` type in TypeScript
- Do not add new dependencies without approval
```

### 5. Reference External Files

```markdown
## Standards
Follow the style guide in `docs/style-guide.md`.
Reference architecture in `docs/architecture.md`.
```

---

## Writing Rules — Best Practices

### Rule File Format

```markdown
---
always: false
ask: true
never: false
description: "Testing requirements"
---

- Always write tests for new functions
- Run the full test suite before committing
- Do not skip flaky tests — fix them
```

### Rule Types

| Type | Behavior | Use For |
|------|----------|---------|
| `always: true` | Auto-enforced, cannot bypass | Security, compliance |
| `ask: true` | Prompts for confirmation | Risky operations |
| `never: true` | Blocks entirely | Forbidden actions |
| Default | Informational only | Guidelines, preferences |

### Rule Placement

- **Security rules** → `.opencode/rules/security.md`
- **Testing rules** → `.opencode/rules/testing.md`
- **Style rules** → `.opencode/rules/style.md`
- **Deploy rules** → `.opencode/rules/deploy.md`

---

## Writing Skills — Best Practices

### Skill Structure

```
.opencode/skills/my-skill/
├── SKILL.md              # Core instructions
├── templates/            # Output templates
│   └── output.md
├── scripts/              # Helper scripts
│   └── validate.py
└── references/           # Reference material
    └── api-docs.md
```

### SKILL.md Template

```markdown
---
name: My Skill
description: "What this skill does. Trigger on: 'keyword1', 'keyword2', 'phrase'."
---

# My Skill

## Role
You are a [specialization].

## Task
Given [input], produce [output].

## Instructions
1. Step one
2. Step two
3. Step three

## Constraints
- Do not [forbidden action]
- Always [required action]

## Output Format
[Expected structure]

## Verification
Before presenting, verify:
- [ ] Check 1
- [ ] Check 2
```

### Progressive Disclosure

Load supporting files only when needed:

```markdown
## Templates
When generating output, read the template at `templates/output.md`.
```

---

## Behavioral Patterns

### The AGENTS.md Loop

1. **Read AGENTS.md** at session start
2. **Apply rules** to every action
3. **Update AGENTS.md** when rules need changing
4. **Never assume** — verify against the file

### The Rule Enforcement Loop

1. **Before action** → Check relevant rules
2. **During action** → Follow constraints
3. **After action** → Verify compliance
4. **If violation** → Report and correct

### The Skill Loading Loop

1. **User request** → Match against skill descriptions
2. **Match found** → Load SKILL.md into context
3. **Follow instructions** → Execute skill workflow
4. **No match** → Fall back to general behavior

---

## Common Patterns

### Pattern: Project Onboarding

```markdown
# AGENTS.md

## Getting Started
1. Run `npm install` to install dependencies
2. Run `npm run dev` to start the dev server
3. Run `npm test` to run tests
4. Read `docs/architecture.md` for system design

## Key Commands
- `npm run dev` — Start development server
- `npm test` — Run tests
- `npm run build` — Production build
- `npm run lint` — Run linter
```

### Pattern: Code Review

```markdown
## Code Review Rules
When reviewing code:
1. Check for security vulnerabilities
2. Verify test coverage
3. Validate error handling
4. Ensure documentation updates
5. Check for performance issues
```

### Pattern: Deployment Gate

```markdown
## Deployment Rules
Before ANY production deploy:
1. All tests must pass
2. Linter must pass
3. Build must succeed
4. Changelog must be updated
5. Version must be bumped
```

---

## Maintenance

### Updating AGENTS.md

When your project evolves:
1. Add new rules for new patterns
2. Remove obsolete rules
3. Update examples to match current code
4. Verify all referenced files exist

### Reviewing Rules

Periodically review `.opencode/rules/`:
- Are rules still relevant?
- Are any rules contradictory?
- Do rules need more specificity?

### Skill Hygiene

Keep skills updated:
- Remove unused skills
- Update skill descriptions for accuracy
- Prune unnecessary supporting files
- Consolidate overlapping skills

---

## Configuration Examples

### Startup Project

```json
{
  "model": {
    "primary": "anthropic/claude-sonnet-4-6"
  },
  "instructions": ["AGENTS.md"]
}
```

### Team Project

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["AGENTS.md", "docs/team-standards.md"],
  "model": {
    "primary": "anthropic/claude-sonnet-4-6"
  },
  "tools": {
    "always": ["read", "glob", "grep"],
    "ask": ["bash:git push", "bash:npm publish"]
  },
  "mcp": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-github"]
    }
  }
}
```

### Enterprise Project

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["AGENTS.md", "docs/compliance.md", "docs/security.md"],
  "permission": "rules",
  "tools": {
    "always": ["read", "glob", "grep"],
    "ask": ["write", "edit", "bash"],
    "never": ["bash:rm -rf", "bash:git push --force"]
  },
  "network": {
    "proxy": "env:HTTP_PROXY",
    "tls": {
      "ca": "/etc/ssl/certs/company-ca.pem"
    }
  }
}
```

---

## Verification Steps

After updating any instruction file:

1. **Syntax check** — Ensure valid Markdown/YAML/JSON
2. **Reference check** — Verify all referenced files exist
3. **Contradiction check** — Ensure no conflicting rules
4. **Test run** — Start a session and verify behavior matches expectations
5. **Version control** — Commit changes with descriptive message
