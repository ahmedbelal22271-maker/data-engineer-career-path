# OpenCode Skills Framework — Complete Official Documentation

> **Source:** https://opencode.ai/skills — https://opencode.ai/rules — retrieved July 2026

---

## Overview

Skills in OpenCode are specialized instruction sets that inject domain-specific context into the AI's conversation. They are Markdown files with YAML frontmatter that describe what the skill does, when to activate it, and what instructions to follow.

---

## What Are Skills

Skills are self-contained instruction packages that extend OpenCode's capabilities. Each skill is a directory containing a `SKILL.md` file (required) and optional supporting files (templates, scripts, references).

When a skill is loaded, its SKILL.md content is injected into the current conversation context. The AI then follows those instructions for the duration of the session.

### Skills vs. Other Mechanisms

| Mechanism | Scope | Persistence | Use Case |
|-----------|-------|-------------|----------|
| **Skills** | Task-specific | Session (loaded on demand) | Domain expertise, workflows |
| **Instructions** | Global | Always in context | Behavioral rules, standards |
| **Rules** | Behavioral | Always enforced | Permissions, constraints |
| **MCP Servers** | External | Always connected | Tool access, data sources |

---

## Skill Directory Structure

```
.opencode/skills/
├── my-skill/
│   ├── SKILL.md              # Required — the skill definition
│   ├── templates/            # Optional — template files
│   │   ├── template1.md
│   │   └── template2.md
│   ├── scripts/              # Optional — helper scripts
│   │   └── validate.py
│   └── references/           # Optional — reference material
│       └── api-docs.md
```

### SKILL.md Format

Every skill must have a `SKILL.md` file with YAML frontmatter:

```markdown
---
name: My Skill
description: "Short description of what this skill does. Used for trigger matching."
---

# My Skill

## Role

You are a specialized assistant for...

## Instructions

1. First, analyze the request...
2. Then, apply the appropriate template...
3. Finally, validate the output...

## Templates

[Embedded templates or references to template files]

## Verification

Before presenting output, verify...
```

---

## YAML Frontmatter

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | Display name of the skill |
| `description` | `string` | Description used for trigger matching |

### Description as Trigger

The `description` field is critical — it's used to match user requests to skills. A good description:

- States what the skill does
- Lists trigger phrases
- Is concise but complete

```yaml
description: "Converts raw data engineering content into enriched Markdown. Trigger on: 'process transcript', 'convert to markdown', 'enrich content', 'create lesson file'."
```

---

## Skill Loading

### Via `skill` Tool

The primary way to load a skill:

```
skill(name: "My Skill")
```

The AI looks up the skill by name from the available skills list, reads its SKILL.md, and injects it into context.

### Via opencode.json

Register skills for auto-loading or explicit reference:

```json
{
  "skill": {
    "my-skill": {
      "path": ".opencode/skills/my-skill",
      "description": "My custom skill",
      "trigger": "use when doing custom work"
    }
  }
}
```

### Via Instructions

Reference skill files in your instructions:

```json
{
  "instructions": [".opencode/skills/my-skill/SKILL.md"]
}
```

This loads the skill into EVERY session — useful for critical skills that must always be active.

### Progressive Disclosure

Skills use progressive disclosure to manage context:

1. **SKILL.md** — Core instructions (always loaded when skill activates)
2. **Supporting files** — Loaded on demand via `read` tool
3. **Templates** — Read when specific output is needed
4. **Scripts** — Executed when automation is required

This prevents loading unnecessary content into the context window.

---

## Skill Categories

### Domain Skills

Provide expertise in a specific domain:

```markdown
---
name: Database Expert
description: "Database design, optimization, and migration. Trigger on: 'database', 'SQL', 'schema', 'migration', 'query optimization'."
---
```

### Workflow Skills

Define multi-step processes:

```markdown
---
name: Code Review Workflow
description: "Structured code review process. Trigger on: 'review PR', 'code review', 'check code quality'."
---
```

### Tool Skills

Extend capabilities with specific tools:

```markdown
---
name: Docker Expert
description: "Docker container management. Trigger on: 'Docker', 'container', 'image', 'docker-compose'."
---
```

### Template Skills

Generate specific output formats:

```markdown
---
name: README Generator
description: "Generate professional README files. Trigger on: 'create README', 'write documentation', 'project docs'."
---
```

---

## Writing Effective Skills

### Principles

1. **One skill, one purpose** — Each skill should do one thing well
2. **Clear trigger description** — The description must accurately trigger on relevant requests
3. **Progressive disclosure** — Load only what's needed; don't dump everything into context
4. **Concrete examples** — Include examples of expected input/output
5. **Verification steps** — Include quality checks in the skill

### Description Best Practices

**Good:**
```yaml
description: "SQL query optimization and performance tuning. Trigger on: 'optimize query', 'slow query', 'SQL performance', 'explain plan', 'index strategy'."
```

**Bad:**
```yaml
description: "Helps with SQL stuff"
```

### Instruction Structure

1. **Role** — Define who the AI is when this skill is active
2. **Task** — What the skill accomplishes
3. **Instructions** — Step-by-step process
4. **Constraints** — Rules and limitations
5. **Output format** — Expected response structure
6. **Verification** — Quality checks before presenting

### Example Skill

```markdown
---
name: API Documentation Generator
description: "Generate OpenAPI/Swagger documentation from code. Trigger on: 'document API', 'create swagger', 'OpenAPI spec', 'API docs'."
---

# API Documentation Generator

## Role

You are a technical writer specializing in API documentation. You analyze code (routes, handlers, models) and generate complete OpenAPI 3.0 specifications.

## Task

Given source code containing API endpoints, generate a complete OpenAPI 3.0 specification in YAML format.

## Instructions

1. **Analyze the codebase:**
   - Find all route definitions
   - Identify HTTP methods and paths
   - Extract request/response schemas
   - Find validation rules

2. **Generate the spec:**
   - Use OpenAPI 3.0 format
   - Include all endpoints with full schemas
   - Add example requests/responses
   - Include error responses

3. **Verify the output:**
   - Validate the YAML syntax
   - Ensure all endpoints are documented
   - Check schema completeness

## Output Format

```yaml
openapi: 3.0.0
info:
  title: API Title
  version: 1.0.0
paths:
  /endpoint:
    get:
      summary: Endpoint description
      # ...
```

## Constraints

- Do NOT invent endpoints that don't exist in the code
- Always use the actual parameter names from the code
- Include ALL error responses (4xx, 5xx)
- Use actual data types, not generic "object"
```

---

## Skill Discovery

### Available Skills List

The system prompt includes a list of all available skills:

```xml
<available_skills>
  <skill>
    <name>My Skill</name>
    <description>What it does</description>
    <location>.opencode/skills/my-skill/SKILL.md</location>
  </skill>
</available_skills>
```

### Auto-Triggering

Skills can be configured to auto-trigger based on the description match:

```json
{
  "skill": {
    "my-skill": {
      "path": ".opencode/skills/my-skill",
      "description": "Auto-activates on database questions",
      "trigger": "database OR SQL OR query OR schema"
    }
  }
}
```

---

## Built-in Skills

### customize-opencode

The only built-in skill. Used for editing OpenCode's own configuration files.

**Triggers:** `opencode.json`, `.opencode/`, `config`, `customize-opencode`

**Use ONLY when:** Editing OpenCode's own files, not user application code.

---

## Skill Management

### Listing Skills

View all available skills in the system prompt's `<available_skills>` section.

### Updating Skills

Edit the SKILL.md file directly. Changes take effect on the next session.

### Removing Skills

Delete the skill directory from `.opencode/skills/`.

### Sharing Skills

Export the skill directory and share it. Others can add it to their `.opencode/skills/`.

---

## Skill Performance

### Context Window Impact

Each loaded skill consumes context window tokens. Consider:

- **Small skill (100 lines):** ~500 tokens
- **Medium skill (500 lines):** ~2,500 tokens
- **Large skill (1000+ lines):** ~5,000+ tokens

### Optimization Tips

1. **Be concise** — Shorter skills load faster and use less context
2. **Use progressive disclosure** — Reference files instead of embedding everything
3. **Load on demand** — Only load skills when needed
4. **Consolidate related skills** — Merge small, related skills into one
5. **Remove unused skills** — Keep the skills directory lean

---

## Rules vs. Skills

| Feature | Rules | Skills |
|---------|-------|--------|
| **Purpose** | Behavioral constraints | Domain expertise |
| **When loaded** | Always | On demand |
| **Format** | Markdown + YAML | Markdown + YAML |
| **Location** | `.opencode/rules/` | `.opencode/skills/` |
| **Enforcement** | Automatic | Manual (`skill` tool) |
| **Persistence** | Session-long | Session-long |

### When to Use Rules

- Security constraints (never access certain files)
- Behavioral requirements (always run tests before commit)
- Formatting standards (use specific code style)

### When to Use Skills

- Domain expertise (database optimization, Docker management)
- Multi-step workflows (code review, API documentation)
- Template generation (README, CHANGELOG, commit messages)

---

## Skill Examples

See the available skills in this project for real-world examples:

- `opencode_core_concepts` — Foundational OpenCode knowledge
- `opencode_cli_commands` — CLI command reference
- `opencode_configuration` — Config file reference
- `opencode_tools_catalog` — Tool catalog
- `opencode_skills_framework` — This skill (skills system reference)
- And 8 more specialized skills
