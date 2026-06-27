# Protocol Conflict Override Matrix (PCOM)

**Status:** Active
**Location:** /protocols/PCOM_protocol.md
**Governs:** Conflicts between user prompts and codified protocol rules
**Registered in:** AGENTS.md, L2_formatting.md

## Trigger Condition
Any time a user prompt explicitly requests a change that would violate,
contradict, or permanently mutate a codified protocol rule.

## Rules

1. The agent must NOT silently execute a user request that would
   destroy or permanently alter a global protocol definition.

2. The agent must surface the conflict explicitly to the user before
   acting, using this exact format:
   > "Your request conflicts with [PROTOCOL NAME] which requires
   > [PROTOCOL RULE]. I will implement your request as a localized
   > exception without modifying the global protocol. Confirm to
   > proceed."

3. Only after explicit user confirmation may the agent proceed.

4. The implementation must create a localized exception class or
   override rule (e.g., `.lthp-override-indigo`) that satisfies the
   user's request without touching the global protocol's baseline
   definition.

5. The localized exception must be documented in the sync log with the
   reason for the override.

## Conflict Hierarchy
- Explicit confirmed user override → Create localized exception
- Silent conflict detected → Surface to user first, do not act
- Global protocol → Remains untouched in all cases

## Failure Condition
Destroying or mutating a global protocol rule without explicit user
confirmation and a localized exception is a PCOM BREACH.

## Interactions
- LTHP: PCOM was introduced specifically to handle LTHP vs. user
  theme conflicts without destroying LTHP's baseline definition.
- All other protocols: PCOM applies universally whenever any protocol
  conflicts with a user prompt.
