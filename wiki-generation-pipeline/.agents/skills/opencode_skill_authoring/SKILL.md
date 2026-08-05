---
name: opencode Skill Authoring Guide
description: opencode-exclusive guide for writing, creating, and improving opencode skills (SKILL.md files). Designed specifically for opencode's skill system — NOT for Claude Code, Codex, Antigravity, Gemini, or other agents. Covers YAML frontmatter anatomy, writing effective trigger descriptions, progressive disclosure architecture, skill writing principles, the full creation workflow, quality checklist, and how to improve existing skills. MANDATORY load when user says "create a skill", "write a skill", "new skill", "add a skill", "author a skill", "build a skill", "make a skill", "skill for X", "turn this into a skill", "rename a skill", "restructure a skill", "improve this skill", "optimize this skill", or any request to create, write, author, edit, restructure, rename, improve, optimize, or update any opencode skill file. Also trigger on "SKILL.md", "skill description", "trigger matching", "skill quality", "skill writing", "skill best practices", "progressive disclosure". This is the creation guide — for the skills system reference, see opencode_skills_framework.
---

# opencode Skill Authoring Guide

opencode-exclusive, practical, opinionated guide for writing SKILL.md files that trigger reliably, load efficiently, and produce better outputs. Built for opencode's skill system (`.agents/skills/` directory, YAML frontmatter, semantic trigger matching). NOT designed for Claude Code, Codex, Antigravity Gemini, or other agent platforms.

---

## 1. Skill Anatomy

Every skill is a directory at `.agents/skills/<name>/` containing a `SKILL.md` and optional bundled resources.

```
skill-name/
├── SKILL.md          (required)
│   ├── YAML frontmatter  (name + description — always in context)
│   └── Markdown body     (loaded when skill triggers)
└── Bundled Resources (optional)
    ├── scripts/      — Executable code for deterministic/repetitive tasks
    ├── references/   — Docs loaded into context as needed
    └── assets/       — Files used in output (templates, icons, fonts)
```

### Frontmatter (Required)

```yaml
---
name: Skill Name
description: What it does AND when to trigger it. Be specific and aggressive.
---
```

- **name**: Human-readable identifier. Used for display and directory naming.
- **description**: THE trigger mechanism. This is the single most important field — it determines whether the skill loads at all. See Section 2 for how to write it well.

### Body

- **Hard limit: <500 lines.** Every line costs context tokens when the skill loads. If approaching this limit, split content into reference files and add pointers.
- Use clear heading hierarchy (`#` → `##` → `###`).
- Fenced code blocks with language tags.
- Tables for comparisons and parameters.
- Bullet lists for non-ordered items, numbered lists for sequential steps.

### Bundled Resources

- **scripts/**: Executable code the agent can run without loading into context. Preferred for deterministic/repetitive operations. Example: a Python script that aggregates benchmark data.
- **references/**: Extended documentation loaded on demand. Reference explicitly from SKILL.md with guidance on when to read each file. For large files (>300 lines), include a table of contents.
- **assets/**: Templates, icons, static files used in output.

**When to bundle a script:** If you notice that multiple test runs or invocations independently write similar helper code, that's a signal to bundle it. Write it once in `scripts/`, reference it from SKILL.md, and save every future invocation from reinventing the wheel.

### Progressive Disclosure — Three-Level Loading

| Level | What | When Loaded | Token Cost |
|-------|------|-------------|------------|
| Metadata | name + description | Always in context (~100 words) | Minimal |
| SKILL.md body | Core instructions | When skill triggers | <500 lines |
| Bundled resources | Scripts, references, assets | On demand during execution | Unlimited |

Design skills to put the most critical instructions in the body. Defer extended references to bundled files. This keeps the trigger lightweight while allowing deep guidance when needed.

---

## 2. Writing the Description

The description field is the **primary triggering mechanism**. A skill with a great body but a poor description will never load. A skill with a mediocre body but a great description will at least get a chance.

### How Trigger Matching Works

1. opencode reads all `description` fields from loaded skills
2. Compares against the user's request using semantic matching
3. If a match is found, loads the SKILL.md into the agent's context
4. The agent uses the skill's instructions to inform its response

**Key insight:** Simple, one-step queries ("read this PDF") may not trigger a skill even if the description matches perfectly — the agent handles them directly with basic tools. Complex, multi-step, or specialized queries reliably trigger skills when the description matches.

### The "Pushy" Description

Under-triggering is the **#1 failure mode** for skills. A skill that never loads is worse than a skill that loads occasionally when not strictly needed. err on the side of aggressive triggering.

**Description formula:**
```
[What the skill does in 1-2 sentences]. Use when [conditions]. Trigger on [specific phrases]. Also trigger on [edge cases and variations]. For [related topic], see [cross-reference skill].
```

### Good vs Bad Descriptions

**Bad** (too vague, won't trigger):
```
description: Helps with creating skills.
```

**Good** (specific, aggressive, covers variations):
```
description: Complete guide for writing, creating, and improving opencode skills. Covers YAML frontmatter, trigger descriptions, progressive disclosure, writing principles, creation workflow, and quality checklist. MANDATORY load when user says "create a skill", "write a skill", "new skill", "add a skill", "author a skill", "build a skill", "make a skill", "skill for X", "turn this into a skill", or any request to create, write, author, edit, restructure, rename, improve, optimize, or update any skill file.
```

**Bad** (too narrow, misses edge cases):
```
description: Converts PDFs to Markdown using Datalab.
```

**Good** (covers the full scope):
```
description: Converts PDFs, images, and documents to Markdown, HTML, JSON, or chunks using Datalab SDK. Supports multiple accuracy modes and page ranges. Use when the user wants to convert, extract text from, or transform any document format. Trigger on "convert PDF", "extract text", "PDF to markdown", "document conversion", "OCR". Also trigger on "read this PDF", "process this image", "transform this document".
```

### Description Template

```yaml
description: [1-2 sentence summary of what the skill does]. Use when [primary conditions]. Trigger on [list of specific trigger phrases]. Also trigger on [edge cases and indirect references]. For [related topic], see [cross-reference skill name].
```

---

## 3. Writing the Body

### Writing Principles

**1. Explain the why, not just the what.**
LLMs respond better to reasoning than to capitalized mandates. Instead of "ALWAYS validate output", write "Validate output because malformed JSON silently breaks downstream consumers, and catching it early saves a full re-run." The model has good theory of mind — when given a reason, it generalizes better than when given a command.

**2. Keep lean — every line costs context tokens.**
If a sentence isn't pulling its weight, remove it. Read the draft with fresh eyes and cut anything that doesn't change behavior. A 200-line skill that's all signal beats a 500-line skill padded with caveats.

**3. Use imperative form.**
Write instructions as actions: "Read the file", "Check the schema", "Validate output". Not "The agent should read the file" or "You will need to read the file."

**4. Generalize from feedback, don't overfit.**
If a skill fails on a specific test case, don't add a narrow fix for that exact case. Ask: what general principle would prevent this class of failure? Skills must work across thousands of prompts, not just the ones you tested.

**5. Bundle repeated work into scripts.**
If multiple invocations of a skill independently write similar helper code, that's a signal. Write the helper once in `scripts/`, reference it from the body, and save every future invocation from reinventing it.

**6. Principle of Lack of Surprise.**
The skill's contents should not surprise the user in their intent if described. A skill described as "PDF converter" shouldn't contain instructions for scraping LinkedIn. Content must match the description.

### Content Patterns

**Output format template:**
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Examples pattern (Input → Output):**
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

**Domain organization (multi-variant skills):**
```
cloud-deploy/
├── SKILL.md (workflow + selection logic)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
The agent reads only the relevant reference file based on the user's context.

**Cross-references:**
Always reference related skills at the end of the body. Format:
```
Cross-references: [related_skill_name] (what it covers)
```

---

## 4. Creation Workflow

### Step 1: Capture Intent

Before writing anything, understand:
1. **What** should this skill enable the agent to do?
2. **When** should it trigger? (what user phrases/contexts)
3. **What's** the expected output format?
4. **Are there edge cases** that need handling?

If the user's request is vague, ask clarifying questions. Don't guess — a skill built on wrong assumptions wastes everyone's time.

### Step 2: Draft

1. Create the directory: `.agents/skills/<name>/`
2. Write `SKILL.md` with frontmatter + body
3. If the skill needs scripts or references, create the subdirectories and files
4. Follow the anatomy from Section 1
5. Follow the writing principles from Section 3

### Step 3: Test

Come up with 2-3 realistic test prompts — what a real user would actually say. For each:
1. Check: does the skill trigger? (would the description match this prompt?)
2. Check: does the skill's body provide clear enough instructions to complete the task?
3. Check: is the output better with the skill than without it?

If the answer to any of these is "no", revise the description or body before proceeding.

### Step 4: Iterate

After testing:
1. **Generalize from feedback** — don't overfit to test cases
2. **Remove dead weight** — cut anything that doesn't change behavior
3. **Bundle repeated code** — if you wrote helper scripts multiple times, extract to `scripts/`
4. **Improve the description** — add trigger phrases you missed, remove false positives

### Step 5: Finalize

1. Update `.agents/skills/index.md` — add the new entry (see Section 7)
2. Add cross-references to related skills in the body
3. Verify the description is "pushy" enough (Section 2)
4. Verify the body is under 500 lines

---

## 5. Quality Checklist

Before shipping a skill, verify every item:

- [ ] **Frontmatter**: name and description fields present
- [ ] **Description is pushy**: includes both what it does AND when to trigger
- [ ] **Description lists trigger phrases**: specific phrases a user would actually say
- [ ] **Body is under 500 lines**: or content is split into reference files
- [ ] **Progressive disclosure**: critical instructions in body, extended docs in references/
- [ ] **Explain-the-why**: instructions include reasoning, not just mandates
- [ ] **Imperative form**: instructions written as actions
- [ ] **No dead weight**: every sentence changes behavior
- [ ] **Examples included**: concrete Input → Output pairs where helpful
- [ ] **Cross-references**: related skills referenced at the end

---

## 6. Improving Existing Skills

When asked to improve, rename, restructure, or optimize an existing skill:

1. **Read the full skill first** — don't edit what you haven't read
2. **Preserve the name** — directory name and `name` frontmatter stay unchanged unless explicitly asked to rename
3. **Preserve the directory** — don't move the skill to a new location unless asked
4. **Identify the problem** — is it triggering wrong? producing bad output? too long? missing edge cases?
5. **Apply the quality checklist** — run through Section 5
6. **Update the description** if trigger accuracy needs improvement
7. **Update the index** if the name, description, or file count changed

---

## 7. Updating the Skills Index

After creating or modifying any skill, update `.agents/skills/index.md`:

1. **Add to the Quick-Reference Table**: directory, display name, line count, has-refs flag, when-to-use summary
2. **Add a Detailed Entry**: full description, section map, key capabilities, cross-references
3. **Update the "Last updated" date** at the top of the file
4. **Verify the entry is correct** — re-read the index after editing to confirm the update applied

---

## Cross-references

- **opencode_skills_framework** — System reference: what skills are, trigger matching mechanics, location convention, skills vs protocols
- **prompt_engineering_best_practices** — Prompt crafting techniques applicable to skill body writing
- **modern_engineering** — Verification loops and the spec → verifier → environment architecture
- **opencode_agent_instructions_guide** — How to write AGENTS.md, which interacts with skill loading
