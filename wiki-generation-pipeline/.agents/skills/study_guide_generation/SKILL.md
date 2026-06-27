---
name: Study Guide Generation
description: Rules and templates for generating student study guides and exam banks.
---



# Source: study-guide-generation-guidelines.md

# Study Guide Generation Guidelines

## Content Completeness
- When generating a study guide, you **must include the actual slide content** of the course — not just question banks or summaries.
- Do not generate a guide that only references or paraphrases slides; embed the relevant content directly.

## Visual Priority
- Apply the rules in `image-processing-protocol.md` for image handling, formatting, and mandatory inclusion.

## Question Analysis — Critical Subagent Prompt Requirements
When deploying a subagent to analyze or solve questions, the prompt given to that subagent must:

1. Be **very sophisticated** — not a simple instruction to "answer the questions."
2. Require the subagent to **think critically** about the problem before answering.
3. Include a **critical evaluation step**:
   - Is the provided answer (if any) correct or incorrect?
   - Why is it correct, or why is it wrong — with clear reasoning and evidence?
   - If the answer is wrong, the subagent must **not make excuses** — it must clearly state that the answer is wrong, provide the evidence, and demand that the main agent correct it.
4. The subagent must escalate disagreements with provided answers to the main agent with **clear evidence**, not silently accept wrong answers.

## Format Requirements
- Apply the full HTML/CSS style guide (see `html-css-generation-style-guide.md`) to all generated HTML study guides.
- Include a document header with metadata badges and a table of contents (see Section 9 of the style guide).
- Each question or topic must have a unique anchor `id` for TOC navigation.

## Workflow Position
- Image downloading and processing (Datalab pipeline) should be completed **before** HTML generation begins.
- The subagent responsible for question solving should receive its task in **Message 2 or 3** of the session — **never Message 1** (which is reserved for rules/identity initialization only).
