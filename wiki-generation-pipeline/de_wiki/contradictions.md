# Contradictions

*All conflicts flagged during processing. Each entry is RESOLVED or UNRESOLVED.*

### [C-1] Python int precision: source says "finite range" vs Python 3 arbitrary precision
Earlier: c2_m1_types.md states "there is a finite range of integers but it is quite large" | Source: Line 39
Later: Python 3 ints have arbitrary precision (unbounded beyond memory) — the source description reflects Python 2 behavior | Source: established Python 3 documentation
Resolution status: RESOLVED
Later content supersedes earlier. Python 3 integers have arbitrary precision.

### [C-2] Float precision: source says "quite small" without specifics
Earlier: c2_m1_types.md states float precision limit is "quite small" | Source: Line 48
Later: IEEE 754 double-precision provides ~15–17 significant decimal digits | Source: established standards
Resolution status: RESOLVED
IEEE 754 reference provides the specific precision limit absent from the source.

### [C-3] Boolean casting: source only shows 1→True/0→False but summary correctly generalizes
Earlier: c2_m1_types.md only demonstrates bool(1)→True and bool(0)→False | Source: Lines 119-133
Later: c2_m1_summary_python_basics.md correctly states "any non-zero integer or float casts to True" | Source: Line 22
Resolution status: RESOLVED
Later summary generalizes correctly — all non-zero values cast to True.

