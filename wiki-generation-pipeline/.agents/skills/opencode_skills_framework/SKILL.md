---
name: opencode Skills Framework
description: Complete reference for opencode's skills system — what skills are, YAML frontmatter anatomy, trigger matching mechanism, skill location convention, loading via config, built-in customize-opencode skill, and comparison with protocols. Trigger on "skills system", "how skills work", "skill trigger", "SKILL.md format", "customize-opencode", "what is a skill", "skills vs protocols", or any question about how opencode's skill system works. For actually writing, creating, or improving a skill, see the opencode_skill_authoring skill.
---

# opencode Skills Framework

## 1. What is a Skill?

A skill is a Markdown file (SKILL.md) with YAML frontmatter containing specialized instructions. When a user's request matches the skill's description, the skill loads into context.

## 2. Skill Anatomy

```markdown
---
name: My Skill Name
description: Brief description that determines when this skill activates
---

# Skill Content

Detailed instructions, reference material, and workflows.
```

Frontmatter fields:
- name (required): Human-readable name
- description (required): Used for trigger matching. Keep concise (1-2 sentences). Include key trigger phrases.

## 3. Trigger Matching

How it works:
1. opencode reads all description fields from loaded skills
2. Compares against user's request using semantic matching
3. If match found, loads SKILL.md into AI's context
4. AI uses skill's instructions to inform response

For best trigger accuracy: keep descriptions concise, include trigger phrases like "use when", "trigger on", avoid vague descriptions.

## 4. Skill Location Convention

Skills live at `.agents/skills/<skill_name>/SKILL.md`. Loaded via config (object with `paths`, not an array of files):

```jsonc
{
  "skills": {
    "paths": [".agents/skills"]
  }
}
```

opencode scans each `paths` directory recursively for `**/SKILL.md` files. Individual skill file paths are not listed. Using an array like `"skills": [".agents/skills/my_skill/SKILL.md"]` will cause an initialization error.

## 5. Built-in Skill: customize-opencode

Built-in skill (not in `.agents/skills/`) that auto-fires when user edits:
- opencode.json / opencode.jsonc
- Files under `.opencode/`
- Files under `~/.config/opencode/`
- Creating/fixing opencode agents, subagents, skills, plugins, MCP servers, permission rules

## 6. Creating a Skill

1. Define purpose and trigger conditions
2. Write SKILL.md with frontmatter and content
3. Place at `.agents/skills/<name>/SKILL.md`
4. Load via config's `skills.paths`
5. Test with `opencode check --skills`
6. Iterate based on results

For the creation workflow (test cases, evals, packaging), see the opencode_skill_authoring skill. For the Anthropic eval harness, see skill-creator.

## 7. Skill Testing

```
opencode check --skills           # Validate all skills
opencode check --skills --verbose  # Detailed validation
opencode run skill_test.md        # Run skill-specific tests
```

## 8. Skills vs Protocols

- Skills: `.agents/skills/<name>/SKILL.md`, loaded by trigger matching
- Protocols: `.agents/protocols/<name>.md`, manually referenced
- Both serve as reference/knowledge
- Skills are trigger-activated, protocols are operationally referenced

## Full Documentation
For the complete official opencode skills framework documentation, see `full_docs.md` in this directory. It contains exhaustive coverage of skill anatomy, trigger matching, loading mechanisms, progressive disclosure, skill categories, and rules vs skills comparison.

Cross-references to:
- opencode_core_concepts (how skills fit in ecosystem)
- opencode_configuration (skills config section)
- opencode_cli_commands (check command)
- opencode_skill_authoring (creating, writing, and improving opencode skills)
