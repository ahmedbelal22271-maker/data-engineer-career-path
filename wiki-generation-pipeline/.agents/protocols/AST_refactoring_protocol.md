# AST-Driven Refactoring: Safe Mass Code Modification

## Why Regex/String Replacement Fails Catastrophically

String-based find-and-replace operates on text, not on meaning. It cannot distinguish:
- A function call `process(x)` from a comment mentioning `process(x)`, a string literal containing the text `"process(x)"`, or a different `process` method on an unrelated class.
- A variable named `data` in scope A from an unrelated variable also named `data` in scope B.
- A function signature change that needs to propagate to *call sites* (which need different edits than the *definition*).

The failure mode is silent: the script reports "47 replacements made" and the codebase doesn't compile, or worse, compiles but is semantically wrong in a way that only shows up at runtime. **Treat any mass refactor that touches more than a handful of call sites as an AST problem, not a text problem, by default.**

## Core Principle: Parse, Transform, Re-emit — Never Edit Text Directly

The safe pipeline is always:
1. Parse source into an AST (or concrete syntax tree, which preserves formatting).
2. Identify target nodes using structural queries (not string matches).
3. Mutate the tree (or generate a structured edit/codemod instruction).
4. Re-emit source from the mutated tree.
5. Diff the re-emitted source against the original to confirm only intended changes occurred.

Never use the AST purely for *finding* locations and then fall back to a text-replace at those locations — line/column numbers shift as soon as any single edit changes line length, invalidating all subsequent offsets computed before the edit. Apply edits via the tree's own mutation/codegen API, or apply text edits in a single pass from bottom-of-file to top-of-file so earlier offsets remain valid.

## Tool Selection by Language

| Language | Tool | Notes |
|---|---|---|
| Python | `libcms`/`LibCST` | Preserves formatting/comments exactly (concrete syntax tree) — critical for not nuking code style in a diff. Prefer over stdlib `ast` for transforms (stdlib `ast` round-trips poorly). |
| Python (simpler cases) | `rope` | Built specifically for refactoring (rename, extract method, move). Good for signature changes with call-site updates. |
| JavaScript/TypeScript | `jscodeshift` (built on Babel) or `ts-morph` | `ts-morph` is strongly preferred when type information matters (e.g., distinguishing overloads) since it uses the actual TypeScript compiler API. |
| Java | OpenRewrite, or Eclipse JDT | OpenRewrite has prebuilt "recipes" for many common refactors — check before hand-rolling. |
| Go | `gofmt -r`, or `go/ast` + `astutil` | Go's tooling is unusually refactor-friendly natively. |
| Multi-language / quick structural search | `ast-grep` or `semgrep` | Good for the *search* phase even if codegen happens elsewhere — pattern syntax matches code structurally, ignoring whitespace/variable naming. |
| Cross-language, fallback | Tree-sitter | Useful when no language-specific high-level tool exists; gives a concrete syntax tree usable for both search and careful text-span edits. |

**Default rule:** if a dedicated codemod tool with prebuilt recipes exists for the operation (rename symbol, change signature, move file), use it before hand-writing an AST transform. Hand-rolled transforms are for cases the existing tooling doesn't cover.

## Step-by-Step Protocol for a Signature Change

Example: changing `def process(data)` to `def process(data, options=None)` across a codebase.

### Step 1: Find the definition, not just the name
Confirm there is exactly one definition matching the target (or enumerate all of them if the name is overloaded/duplicated across classes/modules). A naive grep for `def process(` will also match unrelated `process` methods on unrelated classes — use the AST to confirm each match's enclosing class/module matches the actual target.

### Step 2: Enumerate every call site structurally, not textually
Query the AST for call expressions where the *resolved* callee matches the target function — not just where the text matches. For dynamically-typed languages without full type inference, this resolution can be ambiguous (see Step 5). For statically-typed languages, use the language server / compiler API to resolve symbols precisely (e.g., `ts-morph`'s `getReferences()`, Java's JDT `searchEngine`).

### Step 3: Classify each call site before editing
Not all call sites need the same edit:
- Direct calls with positional args: insert the new arg or leave as-is (if it's optional with a default, existing calls may not need changes at all).
- Calls via `*args`/`**kwargs` forwarding, or reflection/dynamic dispatch (`getattr(obj, "process")(...)`): these will NOT be caught by a structural call-site search and need a separate manual review pass — flag them explicitly rather than silently missing them.
- Calls where the function is passed as a value (callback, decorator, stored in a dict) rather than called directly: signature changes here affect the *type*/contract, not a literal call site — these need their own search (look for the bare function name used as a value, not as a call).

### Step 4: Apply the edit via the tree's mutation API
For LibCST/ts-morph/etc., use the library's structured insert/replace operations on the matched nodes, not manual string slicing — this guarantees syntactic validity post-edit (e.g., correct comma placement) in a way manual slicing doesn't.

### Step 5: Handle dynamic/ambiguous cases explicitly — never guess
If a call site's target can't be resolved with certainty (e.g., dynamic dispatch, duck-typed interfaces, `eval`-constructed calls), do not apply an automated edit. Collect these into an explicit "needs manual review" list and surface it — silently skipping them is how regressions get introduced, and silently "fixing" them via guesswork is worse.

### Step 6: Re-emit and diff
Regenerate source files from the mutated tree and diff against the original. The diff should contain *only* the intended structural change — if whitespace/formatting/comments shifted in regions you didn't intend to touch, the tool's re-emission isn't preserving the original concrete syntax faithfully; investigate before proceeding (this is precisely why concrete-syntax-tree tools like LibCST are preferred over plain ASTs that discard formatting).

### Step 7: Compile/parse-check every touched file before running tests
A syntactically valid individual edit can still produce a file that fails to parse if, e.g., an import needs adding for a new default value's type. Run a parse/compile pass (not full tests yet) across every touched file first — this catches mechanical errors fast and cheaply before burning time on a full test run.

### Step 8: Run the full test suite, not just affected-file tests
Signature changes frequently affect callers in files the structural search didn't have to touch (e.g., a caller relying on the *old* arity erroring out is itself a valid test signal) — run the complete suite, not a filtered subset, after a mass refactor.

## Edge Cases That Break Naive AST Tooling

| Edge case | Why it's dangerous | Mitigation |
|---|---|---|
| Metaprogramming (decorators that wrap signatures, `functools.wraps`, macros) | The "real" call site may be inside generated code invisible to static AST search | Grep separately for decorator usage on the target function and manually inspect each |
| String-embedded code (`eval`, dynamically built SQL/code strings, template-rendered code) | AST tools don't parse inside string literals | Flag any string literal containing the function name as needing manual review |
| Multiple inheritance / duck-typed polymorphism | A call site might resolve to *several* possible implementations depending on runtime type | Don't auto-edit polymorphic call sites without confirming all implementers share the same new contract |
| Generated/vendored code (protobuf stubs, ORM-generated models) | Editing generated files directly will be overwritten on next codegen run | Identify and exclude generated-code directories from the refactor; edit the source schema/template instead |
| Cross-file name shadowing | A local variable named the same as the target function shadows it in some scope | Always resolve via the AST's scope/symbol table, never by bare name match |

## Final Safety Rule

Never run an AST-based mass edit directly against the working tree without a reviewable diff step in between. Generate the transform, emit a diff, and treat that diff as the actual deliverable to inspect — applying hundreds of structurally-correct-but-unreviewed edits in one shot removes the last human/agent checkpoint that catches a wrong structural assumption before it ships.
