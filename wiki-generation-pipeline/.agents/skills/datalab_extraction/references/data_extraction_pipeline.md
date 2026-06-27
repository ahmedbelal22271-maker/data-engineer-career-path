# Data Extraction & Form-Filling Pipelines: Robust Unstructured-to-Structured Mapping

## The Core Risk

Extracting structured data from unstructured sources (free text, scanned documents, inconsistent spreadsheets) and mapping it into a strict schema has one dominant failure mode: **confident incorrect extraction** — a field gets populated with a plausible-looking but wrong value, and because it's not empty, downstream validation that only checks "is this field present" doesn't catch it. The pipeline must be designed around catching *wrong* values, not just *missing* ones.

## Pipeline Architecture: Extract → Validate → Reconcile → Commit

Never extract directly into the destination schema/database in one step. Use an intermediate staging representation that preserves provenance, so every extracted value can be traced back to where it came from and how confident the extraction was.

```
Raw source → Extraction (with confidence + provenance) → Validation layer
   → Reconciliation (missing/ambiguous handling) → Commit to destination schema
```

### Staging record format
Every extracted field should carry more than just its value:

```json
{
  "field": "invoice_total",
  "value": 1542.30,
  "raw_text_span": "Total Due: $1,542.30",
  "source_location": "page_3, line_14",
  "extraction_method": "regex_currency_pattern",
  "confidence": 0.94,
  "ambiguous_alternatives": []
}
```

This is the same principle as the "confirmed contract" documentation in API reversing — provenance and confidence travel with the value, so later stages (and any human review) can act on *how* a value was derived, not just what it is.

## Step 1: Extraction — Prefer Deterministic Methods, Escalate Only When Needed

Order extraction methods by reliability, falling back only when a more deterministic method genuinely can't apply:

1. **Structured source parsing** (if the source has any inherent structure — table cells in a PDF, key-value pairs in a form, JSON/XML) — parse this structure directly rather than flattening it to plain text first and re-extracting. Flattening throws away free positional/structural signal that a pattern-based or model-based extractor then has to re-infer.
2. **Pattern-based extraction** (regex, fixed-format parsers) for fields with a reliable, consistent format (dates in a known format, currency amounts, ID numbers with a fixed pattern). Deterministic and exactly reproducible — prefer this whenever the field's format is actually consistent across the source set.
3. **Model-based / NLP extraction** for genuinely unstructured free text (extracting an entity name from a paragraph, classifying intent). Necessary when no structural or pattern regularity exists, but inherently probabilistic — always attach a confidence score, and treat the output as a *candidate*, not a fact, until validated.

**Never apply model-based extraction to a field that pattern-based extraction could handle deterministically.** A date in `MM/DD/YYYY` format should be extracted via a date-pattern parser, not by asking a model to "find the date" — the deterministic method is faster, free of model-specific failure modes, and exactly reproducible across re-runs.

## Step 2: Validate Against the Destination Schema's Actual Constraints — Not Just Type

Schema validation needs to check more than "is this a string/number":

- **Type validation**: does the value parse as the declared type without silent coercion errors? (e.g., does `"1,542.30"` actually convert to a clean float, or does the comma break a naive `float()` call in some locales?)
- **Range/format validation**: does the value satisfy the schema's actual constraints (a percentage between 0-100, a date that isn't in the future for a "date of birth" field, a string matching a required ID pattern)?
- **Cross-field consistency validation**: do related extracted fields agree with each other? (e.g., if both "subtotal," "tax," and "total" were extracted independently, does `subtotal + tax == total` within rounding tolerance? A mismatch here is one of the highest-signal indicators that at least one of the three was extracted wrong, even though each individually looks plausible.)
- **Referential validation against existing data**, if applicable: does an extracted "customer ID" actually exist in the destination system, or extracted "country" match an actual valid enum value rather than a near-miss string like `"USA "` with trailing whitespace or `"U.S.A."` needing normalization?

Cross-field consistency checks are disproportionately valuable relative to their implementation cost — they catch a class of error (individually plausible, jointly impossible) that field-by-field validation structurally cannot catch.

## Step 3: Handle Missing Fields Safely — Never Silently Default

The single most dangerous pattern in form-filling pipelines is silently substituting a default value for a missing field, because downstream consumers then can't distinguish "this field was genuinely zero/empty" from "extraction failed to find it."

### Explicit missingness representation
Use a distinct sentinel (a real `null`/`None`, or an explicit `"extraction_failed"` status field) — never a placeholder value that's also a plausible real value (e.g., never default a missing numeric field to `0`, never default a missing date to today's date, never default a missing name field to an empty string if the schema elsewhere treats empty string as "explicitly blank").

### Required vs optional field handling differs
- For schema-required fields that are missing in the source: do not commit the record. Route to a human-review queue or a reconciliation step, with the specific missing field and the source location searched flagged explicitly. Committing a required field with a guessed value is worse than not committing at all.
- For optional fields: missing is a valid, normal outcome — commit as explicit null, don't flag as an error, but still record *that* extraction was attempted and came back empty (vs. extraction not being attempted at all) for audit purposes.

### Distinguish "not present in source" from "present but unparseable"
These need different handling: a genuinely absent field is a data-completeness issue; a present-but-malformed field (e.g., a date field containing the literal text "TBD") is a data-quality issue in the source and should be flagged differently, since blindly retrying extraction on it won't help — the source itself needs correction or special-case handling.

## Step 4: Deterministic Conversion — Normalize Before Validating, Not After

Type/format conversion should happen in a single, deterministic, well-tested normalization layer, applied consistently to every extracted value before it reaches validation — not scattered as ad hoc fixes wherever a particular format issue happens to be noticed.

### Common normalization traps
- **Locale-dependent number formats**: `1.542,30` (European) vs `1,542.30` (US) — never assume a single locale; detect or require explicit declaration of source locale before parsing numbers/dates, since silently guessing wrong produces a value that's off by a factor of 1000 with no error raised.
- **Date ambiguity**: `03/04/2026` is March 4 or April 3 depending on locale convention — if the source format is ambiguous and no other signal (a day value >12 in another date from the same source) resolves it, flag as ambiguous rather than guessing the more "common" interpretation.
- **Unit ambiguity**: a bare numeric weight/measurement field without an explicit unit captured alongside it is incomplete, not just "a number" — always extract the unit as part of the same field, never assume a default unit silently.
- **Encoding and whitespace**: normalize Unicode (NFKC), strip/collapse whitespace, and standardize smart quotes/dashes from source documents before any string-equality or pattern matching — silent mismatches here look exactly like genuine data inconsistency and are a common source of false "this doesn't match" validation failures.

### Conversion must be idempotent and reversible where possible
Running the normalization step twice on already-normalized data should produce the same result (idempotent), and ideally the original raw value is retained alongside the normalized one (not overwritten) so any normalization bug discovered later can be corrected by re-running on preserved raw data rather than needing to re-extract from the original source entirely.

## Step 5: Reconciliation — The Human/Review Escalation Boundary

Define explicit, mechanical thresholds for what gets auto-committed vs. escalated — don't leave this as a vague judgment call made differently each run:

```markdown
## Auto-commit criteria (ALL must hold)
- confidence >= 0.9 for every extracted field in the record
- all required fields present and individually valid
- all cross-field consistency checks pass within tolerance
- no ambiguous_alternatives present on any field

## Escalate to review queue if ANY of:
- any required field missing
- any field confidence < 0.9
- any cross-field consistency check fails
- any field has unresolved ambiguous_alternatives (e.g., date format ambiguity)
```

Log every escalation with the specific reason (not just "needs review") — this is what allows patterns to be noticed across many escalated records (e.g., "80% of escalations are the same date-ambiguity issue from one specific source format") and fixed systemically rather than reviewed one-by-one indefinitely.

## Step 6: Commit With an Audit Trail, Never in Place of the Staging Record

Commit validated records to the destination schema, but retain the staging record (raw extraction + provenance + confidence) rather than discarding it once committed. If a downstream consumer later reports a wrong value, the staging record is what lets you determine whether the error originated in extraction, normalization, or the destination system itself — without it, root-causing a bad committed value means re-deriving the entire extraction process from scratch with no record of what actually happened the first time.

## Anti-Patterns

| Anti-pattern | Why it fails |
|---|---|
| Extracting directly into the destination schema with no staging/provenance layer | No way to trace a bad value back to its source or extraction method when errors surface later |
| Defaulting missing fields to a plausible-looking value (0, today's date, empty string) | Makes "missing" indistinguishable from "genuinely zero/blank," corrupting downstream logic that depends on that distinction |
| Validating fields independently with no cross-field consistency checks | Misses the class of error where each field looks individually fine but the record is jointly impossible |
| Using model-based extraction for fields with a deterministic, consistent format | Introduces unnecessary non-determinism and failure surface where a regex/parser would be exact and reproducible |
| Silently guessing on locale/date ambiguity rather than flagging it | A confidently wrong value is worse than an explicitly flagged uncertain one — it passes naive validation and corrupts data quietly |
