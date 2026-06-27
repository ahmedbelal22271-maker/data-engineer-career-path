# UNIVERSAL_PROTOCOL_IMPLEMENTATION_PROMPT

## Overview
This template provides the execution vehicle for integrating any newly-approved protocol (such as PDPP Stage 5 or one-off protocol adoptions) into the L1–L5/AGENTS.md architecture.

## Execution Steps

1. **Determine target L-file**: Analyze the protocol's scope and purpose to select the appropriate existing instruction file (AGENTS.md or L1–L5) for the new directive.
2. **Backup target file**: Use the IFMP sliding-window backup sequence to create a `_v3` snapshot of the target L-file before any modifications.
3. **Backup AGENTS.md**: Use the IFMP sliding-window backup sequence to create a `_v3` snapshot of `instructions/AGENTS.md`.
4. **Append protocol text verbatim**: Write the full text of the approved protocol into its designated `/protocols/` file exactly as authored, without summarization or omission.
5. **Validate size increase**: Perform a byte-size comparison on the newly written protocol file to confirm it is larger than its expected baseline size.
6. **Draft condensed AGENTS.md entry**: Write a single-sentence summary directive for `AGENTS.md` containing the protocol's purpose and a clear breach condition.
7. **Get user confirmation**: Present the drafted directive to the user and stop execution to await their explicit approval.
8. **Append to AGENTS.md**: Upon receiving approval, append the confirmed directive text to `AGENTS.md` without altering existing directives.
9. **Validate**: Perform a byte-size comparison on `AGENTS.md` to confirm the size increased and no existing content was truncated.
10. **Log to GLOBAL_HUB_SYNC_LOG.md**: Append an entry to the sync log detailing the appended directive, its purpose, and the pre/post byte sizes.
11. **Final report**: Generate a comprehensive execution report summarizing all actions, validated byte sizes, and log updates.
