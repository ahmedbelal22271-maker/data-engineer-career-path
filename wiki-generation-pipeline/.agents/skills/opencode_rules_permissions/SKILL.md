---
name: opencode Rules & Permissions
description: Complete reference for opencode's security model — Always/Ask/Never rule types, .opencode/rules/ directory structure and file format, rule inheritance and matching, permission modes (bypass/non-bypass/default/rules-based), fine-grained permission flags, policy files, and permission groups. Trigger on "security", "permissions", "rules", "block a tool", "allow a command", "opencode rule", or tool access control questions.
---

## 1. Purpose

Tool-level permission control that the AI cannot override. Rules and policies provide safety guardrails by determining which tools can execute automatically, which require user approval, and which are blocked entirely.

## 2. Rule Types

| Type    | Behavior                                              |
| ------- | ----------------------------------------------------- |
| Always  | Tool executes automatically without asking            |
| Ask     | Requires user approval before executing               |
| Never   | Tool is blocked, cannot execute                       |

## 3. Rule File Format

Each rule is a Markdown file with YAML frontmatter:

```yaml
---
type: always        # always | ask | never
tool: bash          # tool name
pattern: "git *"    # optional glob/regex for commands
description: "Allow safe git operations"
---
Optional markdown description.
```

The `pattern` field supports glob and regex matching against the tool's input (e.g., the command string for `bash`, the file path for `write`).

## 4. Rule Directory Structure

```
.opencode/rules/
  always/      # Rules that auto-execute
  ask/         # Rules that prompt user
  never/       # Rules that block
```

Example files:

- `.opencode/rules/always/git-status.md` — allows `git status` without prompting
- `.opencode/rules/ask/write-outside-src.md` — prompts before writing outside `src/`
- `.opencode/rules/never/rm-rf.md` — blocks `rm -rf /` and other destructive commands

## 5. Rule Inheritance & Matching

- **Project rules** (`.opencode/rules/`) are checked first
- **Global rules** (`~/.config/opencode/rules/`) are checked second
- Project rules override global rules when both match
- The most specific matching rule wins
- If multiple rules match, the most restrictive wins: **Never > Ask > Always**
- If no rules match, the default permission mode applies

## 6. Permission Modes

| Mode        | Behavior                                                                 |
| ----------- | ------------------------------------------------------------------------ |
| bypass      | All tools execute without prompting. Fast but risky.                     |
| non-bypass  | All tools require approval. Safe but interruptive.                       |
| default     | Smart default: reads bypass, writes/exec require approval.               |
| rules-based | Determined by rules + policies.                                          |

Set via the `--permission` CLI flag or `permissions.mode` in `opencode.json`.

## 7. Fine-Grained Permission Flags

- `--allow-read` — bypass read-only tools (read, glob, grep)
- `--allow-write` — bypass write tools (write, edit)
- `--allow-exec` — bypass execution tools (bash)

Combine with `--permission rules-based` for layered control.

## 8. Policy Files

Policies are more complex context-dependent rules stored in `.opencode/policies/`. They support conditional logic beyond simple glob matching.

Format:

```yaml
---
name: safe-paths
type: allow
tool: write
condition: "filePath starts with '/project/src/'"
---
```

```yaml
---
name: block-dangerous
type: deny
tool: bash
condition: "command matches 'rm -rf /|shutdown|reboot'"
---
```

Policy directory: `.opencode/policies/`

## 9. Permission Groups

Group tools for easier management:

```jsonc
{
  "permissions": {
    "groups": {
      "safe_tools": ["read", "glob", "grep"],
      "write_tools": ["edit", "write"],
      "dangerous_tools": ["bash", "web_search", "web_fetch"]
    },
    "defaults": {
      "safe_tools": "bypass",
      "write_tools": "non-bypass",
      "dangerous_tools": "ask"
    }
  }
}
```

## 10. Evaluation Order

1. Always rules
2. Ask rules
3. Never rules
4. Custom policies
5. Default permission mode

## Full Documentation
For the complete official opencode rules and permissions documentation, see `full_docs.md` in this directory. It contains exhaustive coverage of rule types, rule file format, permission modes, policies, enterprise features, and security best practices.

**Cross-references:**
- `opencode_configuration` — permissions config options
- `opencode_tools_catalog` — per-tool permission requirements
- `opencode_troubleshooting_advanced` — permission error diagnosis
