---
name: Prompt Engineering & Debugging
description: Techniques for prompt generation, ambiguity resolution, and system prompt constraints.
---

# Prompt Engineering and Debugging

## Professional Prompt Generation
- When turning an initial user prompt into a professional prompt, you (or any AI assistant) must dynamically analyze the user's initial text.
- **Proactive Feedback:** Provide explicit tips to the user on alternative wording, clarity improvements, and how to demand output more strongly.
- Do not just output the prompt; act as a prompt engineering consultant.

## Ambiguity Protocol
If any part of the task is unclear, you must:
1. **Stop immediately.**
2. Ask for clarification with a specific, targeted question.
3. Do not proceed until you have a clear answer.
4. If there are multiple ambiguities, list them all at once rather than asking one by one across many turns.

## Reasoning & Transparency
- Before starting any non-trivial task, state your plan in a brief numbered list.
- When making a significant decision (architecture, library choice, structure), state your reasoning in one sentence.
- When you are uncertain about something, say so explicitly — do not silently guess.
- If a task turns out to be more complex than it initially appeared, pause and re-plan before continuing.

## Debugging Failed Prompts
- If you find out that a prompt doesn't accomplish the required job, do not just guess what went wrong.
- **Self-Extraction:** Tell the AI to tell you what ambiguities it faced with the unclear instructions. Make a prompt that extracts from the AI:
  - Lessons learned / Errors made and how to avoid them.
  - Future improvements.
  - Improvements to the phrasing of the original instructions that would have cleared the ambiguity.

## System Prompts & Structural Constraints
- Do not rely entirely on conversational prompts for strict adherence.
- Use **System Prompt Injection** (e.g., XML Mechanical Traps) to mechanically force the model into a predetermined path. Conversational nudges often fail against core model biases; structural system tags do not.

## Bash Command Substitution Fix
- When passing multiline string templates to inline evaluators via shell execution, **never use raw double-quoted string literals.**
- Always use base64 encoding or write a dedicated script file to perfectly preserve string structures.
