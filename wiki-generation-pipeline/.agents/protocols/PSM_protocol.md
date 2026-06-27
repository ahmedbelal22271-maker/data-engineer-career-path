### Protocol Sourcing Mandate (PSM)

**Scope:** Universal. Applies to every named protocol in every session.

**Trigger Condition:** Any time you are about to execute a named
protocol (e.g., LTHP, SFBP, CCMP, ISIP, PCOM, IFMP, DOMP, or any
other protocol registered in AGENTS.md).

**Rules:**

1. **Mandatory Raw Read Before First Execution:**
   Before executing a named protocol for the first time in a session,
   you must explicitly call `view_file` (or equivalent file-read tool)
   on that protocol's source document in `/protocols/` or
   `/instructions/`. Relying on a summary, a condensed memory, or a
   prior scan result is a PSM BREACH. The raw file must be read.

2. **Mandatory Re-Read After Major Build Steps:**
   If more than one major build step (a completed section, a file
   write, or a tool execution sequence) has passed since you last read
   a protocol's source file, you must re-read it before executing it
   again. Context drift across long sessions is not an excuse for
   protocol deviation.

3. **Mandatory Negative Constraint Extraction:**
   Immediately after reading the protocol file, you must extract and
   write into the sync log every negative constraint found in that
   protocol — meaning every rule that begins with "must never,"
   "must not," "is prohibited," "is a breach," or equivalent language.
   This extraction must appear in the sync log before any execution
   step begins. Skipping this extraction is a PSM BREACH.

   Example sync log entry format:
   `[PSM] LTHP negative constraints loaded:`
   `- Must never be applied to structural layout containers`
   `- Must never use hardcoded yellow or high-luminance solid fill`
   `[PSM] Proceeding to execute LTHP.`

4. **No Execution Without Logged Extraction:**
   If the sync log does not contain the negative constraint extraction
   entry for a protocol, that protocol has not been properly sourced.
   Any output produced under an unsourced protocol is invalid and must
   be redone after proper sourcing.

**Failure Condition:** Executing any named protocol from memory,
from a summary, or without a logged negative constraint extraction
is a strict PSM BREACH and an L1 violation.

**Interaction with all protocols:** PSM wraps every other protocol.
It does not replace any protocol's own rules — it governs how all
protocols are loaded before execution.
