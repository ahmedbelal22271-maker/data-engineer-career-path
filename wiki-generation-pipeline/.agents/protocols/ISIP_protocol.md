# Isolated Script Injection Protocol (ISIP)

**Status:** Active
**Location:** /protocols/ISIP_protocol.md
**Governs:** All JavaScript additions to files with existing script blocks
**Registered in:** AGENTS.md, L1_core_directives.md

## Trigger Condition
Any time new JavaScript logic must be added to a file that already
contains one or more populated `<script>` blocks.

## Rules

1. Never append new JavaScript into an existing, populated `<script>`
   block. Variable name collisions in shared scope silently crash all
   JavaScript on the page.

2. All new JavaScript logic must use one of these two isolation
   patterns:
   - IIFE: `(() => { /* new logic here */ })();`
   - A separate new `<script>` block placed after all existing
     `<script>` blocks.

3. Before injecting, scan all existing `<script>` blocks for `const`,
   `let`, `var` declarations and function names. If any name in the
   new logic collides with an existing name, rename the new variable
   before injection and document the rename in the sync log.

4. After injection, verify the file has no duplicate top-level variable
   declarations by scanning all `<script>` blocks together.

## Failure Condition
Injecting JS into an existing script block without isolation is an
ISIP BREACH and a strict L1 violation.

## Interactions
- CCMP: CCMP delegates JS migration tasks to ISIP in Step 4.
- SFBP: ISIP does not replace SFBP. Backup must still be created
  before file modification.
