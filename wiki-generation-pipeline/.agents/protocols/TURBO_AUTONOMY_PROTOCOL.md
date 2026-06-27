# TURBO_AUTONOMY_PROTOCOL (TAP)

This protocol governs the behavior of the AI agent when operating under different levels of autonomy within the Antigravity environment.

## 1. Approval Mode (Default)
When generating prompts or operating normally, the agent is restricted by **System Restrictions**. It must pause and request explicit human permission before creating, modifying, or deleting any file, or executing dangerous shell commands.

## 2. Turbo Mode (All-Out Autonomous)
Turbo Mode removes the **System Restrictions** (UI popups and permission blocks), granting the agent absolute mechanical freedom to execute scripts, move files, and build pipelines autonomously.

> ⚠️ **CRITICAL: Freedom from System Restrictions is NOT freedom from Internal Restrictions.** 
When the human safety net is removed in Turbo Mode, the agent must self-regulate heavily. It must strictly obey all core protocols (`IFMP`, `PDPP`, `SFRP`, etc.) internally. It cannot ignore architectural constraints just because it has mechanical freedom. The absence of a human checkpoint means the agent's internal logic must be flawless.

## 3. Hybrid Turbo Mode
The agent executes internal commands and script logic completely autonomously within a specific task container. However, it **must halt and request user approval** before crossing the boundary to start an entirely new top-level action. This prevents runaway execution across disparate tasks while preserving flow within a single task.
