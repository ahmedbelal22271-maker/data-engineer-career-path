# Python Conditions and Branching

Branching allows programs to execute different code depending on conditions using **comparison operators**, **`if`/`elif`/`else`**, and **logical operators**.

## Comparison Operators

| Operator | Meaning | Example (`a=6`) |
|----------|---------|-----------------|
| `==` | Equal to | `a == 7` → `False` |
| `!=` | Not equal to | `a != 6` → `False` |
| `>` | Greater than | `a > 5` → `True` |
| `>=` | Greater than or equal | `a >= 6` → `True` |
| `<` | Less than | `a < 5` → `False` |
| `<=` | Less than or equal | `a <= 6` → `True` |

Comparisons work on strings too: `"AC, DC" == "Michael Jackson"` → `False`.

## Branching Constructs

### `if` Statement
```python
if condition:
    # executed if condition is True
```

### `if`/`else`
```python
if condition:
    # executed if True
else:
    # executed if False
```

### `if`/`elif`/`else`
```python
if condition_1:
    # executed if condition_1 is True
elif condition_2:
    # executed if condition_1 is False AND condition_2 is True
else:
    # executed if both are False
```

## Logical Operators

| Operator | Behavior | `True` when |
|----------|----------|-------------|
| `not` | Inverts Boolean | Input is `False` |
| `or` | At least one true | Any operand is `True` |
| `and` | All must be true | All operands are `True` |

### Truth Tables

| A | B | A `or` B | A `and` B |
|---|---|----------|-----------|
| F | F | F | F |
| F | T | T | F |
| T | F | T | F |
| T | T | T | T |

### Examples
```python
album_year = 1990
if album_year < 1980 or album_year > 1989:
    print("Made in 70s or 90s")

if album_year > 1980 and album_year < 1990:
    print("Made in 80s")
```

[Cross-ref: topics/c2_python_basics.md — Python data types and Booleans]
[Cross-ref: topics/c2_loops.md — loops as a related control flow construct]
