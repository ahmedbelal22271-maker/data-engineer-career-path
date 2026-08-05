# OpenCode Rules & Permissions — Complete Official Documentation

> **Source:** https://opencode.ai/rules — https://opencode.ai/permissions — https://opencode.ai/policies — retrieved July 2026

---

## Overview

OpenCode has a layered security model: **rules** define what the AI can and cannot do, **permissions** control how those rules are enforced, and **policies** provide high-level governance.

---

## Rules

Rules are instructions that constrain AI behavior. They are checked before every action. Rules apply to the current session and can be project-level or global.

### Rule Types

#### Always Rules

These rules run on every interaction. They cannot be bypassed.

```markdown
<!-- .opencode/rules/security.md -->
---
always: true
---
- Never commit secrets or API keys
- Never run `rm -rf` without user confirmation
- Always use parameterized queries
```

#### Ask Rules

These rules prompt for user confirmation before the action proceeds.

```markdown
<!-- .opencode/rules/deploy.md -->
---
ask: true
---
- Before running any deploy command
- Before modifying production config files
- Before deleting files not tracked by git
```

#### Never Rules

These rules completely block the specified actions.

```markdown
<!-- .opencode/rules/forbidden.md -->
---
never: true
---
- Never access ~/.ssh/ or ~/.aws/ directories
- Never modify .gitignore
- Never run `git push --force`
```

### Rule File Format

Rules are Markdown files with YAML frontmatter:

```markdown
---
always: false
ask: true
never: false
description: "Custom rules for this project"
---

- Always run tests before committing
- Use conventional commit messages
- Prefer TypeScript over JavaScript
```

### Rule File Location

Rules can be placed in:

1. `.opencode/rules/*.md` — project-level rules (checked first)
2. `~/.config/opencode/rules/*.md` — user-level rules (global defaults)
3. Referenced in `instructions` in `opencode.json`

### Rule Inheritance

Rules are merged from all sources:
- User-level rules apply everywhere
- Project-level rules override user rules
- `always: true` rules cannot be disabled
- `never: true` rules cannot be overridden

### Rule Matching

Rules are matched against every tool call and AI action. When a rule matches:
- **always** → action proceeds, logged for audit
- **ask** → user is prompted for confirmation
- **never** → action is blocked, AI is notified

---

## Permission Modes

Permission modes control how rules are enforced during tool execution.

### Bypass Mode

All tools execute without any permission checks. The fastest mode, but least safe.

```json
{ "permission": "bypass" }
```

**Use when:** You trust the AI completely and want maximum speed.

### Default Mode

Standard permission handling:
- **Read-only tools** (read, glob, grep, web_search, web_fetch) → auto-execute
- **Write tools** (write, edit) → ask for confirmation
- **Destructive tools** (bash with dangerous commands) → ask for confirmation

```json
{ "permission": "default" }
```

**Use when:** General development work with reasonable safety.

### Rules Mode

Fine-grained control via the rules system. Only actions explicitly allowed by rules proceed.

```json
{ "permission": "rules" }
```

**Use when:** Enterprise environments, regulated industries, or shared projects.

### Config-Based Permission

Configure permissions directly in `opencode.json`:

```json
{
  "tools": {
    "always": ["read", "glob", "grep", "web_search", "web_fetch"],
    "ask": ["write", "edit", "bash"],
    "never": ["bash:rm -rf"]
  }
}
```

### Preserve State

Remember permission decisions across sessions:

```json
{
  "tools": {
    "preserve": {
      "bash": true,
      "write": true,
      "edit": false
    }
  }
}
```

When `preserve` is `true`, once you allow a tool, it stays allowed for future sessions.

---

## Policies

Policies are high-level governance rules for teams and organizations. They define acceptable usage patterns and can be enforced across multiple projects.

### Policy File Format

```json
{
  "policies": {
    "max_tokens_per_session": 1000000,
    "allowed_providers": ["anthropic", "openai"],
    "blocked_tools": ["bash:curl"],
    "require_approval": {
      "bash": ["git push", "npm publish", "docker push"],
      "write": ["*.env", "*.key", "*.pem"]
    }
  }
}
```

### Policy Fields

| Field | Type | Description |
|-------|------|-------------|
| `max_tokens_per_session` | `number` | Token budget per session |
| `allowed_providers` | `string[]` | Whitelist of AI providers |
| `blocked_tools` | `string[]` | Tools/commands that are always blocked |
| `require_approval` | `object` | Patterns requiring explicit approval |

### Enterprise Policies

For enterprise deployments, policies can be centrally managed:

```json
{
  "policies": {
    "enterprise": {
      "audit_log": true,
      "sso_required": true,
      "rbac_enabled": true,
      "data_classification": "confidential",
      "compliance_framework": "soc2"
    }
  }
}
```

---

## Permission Configuration Reference

### Tool Permission Levels

| Level | Behavior |
|-------|----------|
| `always` | Auto-execute, never ask |
| `ask` | Prompt user before executing |
| `never` | Block entirely |
| `preserve` | Remember last decision |

### Per-Command Permissions (Bash)

You can set permissions on specific bash commands:

```json
{
  "tools": {
    "always": ["read", "glob", "grep"],
    "ask": ["bash:git commit", "bash:git push"],
    "never": ["bash:rm -rf /", "bash:git push --force"]
  }
}
```

### Glob Patterns in Permissions

Rules support glob patterns for file-specific permissions:

```markdown
---
never: true
---
- Never modify *.env files
- Never delete files in *.key or *.pem
```

---

## Security Best Practices

1. **Start with default mode** — Use `"permission": "default"` for general work
2. **Add rules for sensitive operations** — Use `ask: true` for deploy/publish commands
3. **Never allow force-push by default** — Use `never: true` for `git push --force`
4. **Use preserve sparingly** — Only preserve permissions for tools you trust long-term
5. **Audit regularly** — Check `.opencode/rules/` periodically for stale rules
6. **Separate prod and dev rules** — Use environment-specific rule files
7. **Protect secrets** — Use `never: true` for paths containing credentials
