---
name: Modern Engineering (Karpathy Method)
description: The three-layer architecture for 10x faster AI building. Agile Specking, Verification Protocols, and Optimized Environment.
---

# Modern Engineering (Karpathy Method)

This skill dictates the overarching architecture of how to interact with AI models successfully, breaking it down into three mandatory layers: The Spec, The Verifier, and The Environment.

## Layer 1: The Spec (Agile Specking)
Do not use "Waterfall" prompting (dumping everything at once and expecting a final product). Use "Agile Specking".
1. **Uncover the Goal:** Have the AI interview you to identify the core goal of the project before building.
2. **Tight Scope & Clear Checkpoints:** Bias towards smaller, compartmentalized specs. Review the output, adjust, and repeat.
3. **Be Precise & Use Your Brain:** Explicitly instruct the AI: `"Make me verify key decisions explicitly to ensure nothing is missed."` Every assumption an AI makes is a drift from the final product.

## Layer 2: The Verifier (Animals vs Ghosts)
AI models are statistical simulation circuits ("Ghosts" or "Robot Librarians"), not "Animals". You cannot motivate them by yelling or pleading. You must manage them through strict verification.
1. **Set Evaluation Criteria Upfront:** Before touching a task, define what good looks like with mathematical precision. Add this to prompts: `"Outline the evaluation criteria you will use to ensure a high-quality final product. Be precise."`
2. **Use a Second AI Model as a Critic:** Use a secondary system or plugin to independently grade the output of the first model.
3. **Pull External Signals:** Connect the AI to real-world data (like deployment status or historical reports) so it can independently verify if it succeeded, rather than guessing.

## Layer 3: The Environment (Workshop Infrastructure)
You must build an optimized workspace that improves over time so you don't start from scratch every session.
1. **The System Prompt (claude.md / AGENTS.md):** Ingest key working rules automatically. E.g., `multi-step: include a verification plan`. Outline how the repo works, custom skills routing, and knowledge architecture.
2. **LLM Knowledge Base:** Create a structured folder system to ingest your own training data. This is your intellectual moat.
3. **Custom Skills:** If you do something repeatedly, create a custom skill handbook. The more you use a skill, the tighter it becomes.
4. **Rule-Based Guardrails (Pre-Tool Hooks):** Establish concrete rules enforced at the tool level, not just the prompt level. Bucket tasks into three groups:
   - **Always Do:** AI runs on autopilot.
   - **Ask First:** Double-check required.
   - **Never Do:** Absolute critical boundaries enforced by pre-tool hooks (e.g., cannot edit `/important_dont_edit` folders).
