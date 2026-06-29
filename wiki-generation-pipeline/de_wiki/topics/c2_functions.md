# Python Functions

Functions are **reusable code blocks** that take input, perform tasks, and produce output.

## Benefits

Modularity, reusability, readability, easier debugging, abstraction, collaboration, maintainability.

## Built-In Functions

| Function | Description | Example |
|----------|-------------|---------|
| `len()` | Length of sequence/collection | `len([1,2,3])` → `3` |
| `sum()` | Total of all elements | `sum([10,20,30])` → `60` |
| `max()` | Maximum value | `max([5,12,8])` → `12` |
| `min()` | Minimum value | `min([5,12,8])` → `5` |
| `sorted()` | Returns **new** sorted list | `sorted([3,1,2])` → `[1,2,3]` |
| `.sort()` | Sorts list **in place** | `list.sort()` → `None` |

`sorted()` returns a new list (original unchanged). `.sort()` modifies in place and returns `None`.

## Defining Functions

```python
def add(a):
    """Adds one to a and returns the result."""
    b = a + 1
    return b
```

- Use `def` keyword, function name, parentheses, colon
- **Docstrings** (triple-quoted) document the function
- `return` outputs a value; no `return` → returns `None`
- `pass` is a placeholder for an empty function body

## Parameters

```python
def mult(a, b):
    return a * b

mult(2, 3)                     # 6
mult(2, "Michael Jackson")     # "Michael JacksonMichael Jackson"
```

**Variadic parameters** (`*args`) accept variable arguments, packed into a tuple:

```python
def print_all(*names):
    for name in names:
        print(name)
```

## Variable Scope

| Scope | Description |
|-------|-------------|
| **Global** | Variables defined **outside** functions; accessible everywhere |
| **Local** | Variables defined **inside** functions; only accessible within |
| **Lookup** | Python checks local scope first, then global |

```python
x = "ac"  # global

def add_dc(x):
    x = x + "dc"  # local — does not affect global x
    return x
```

Use `global` keyword inside a function to write to global scope:
```python
def pink_floyd():
    global claimed_sales
    claimed_sales = "45 million"
```

[Cross-ref: topics/c2_loops.md — using loops inside functions]
[Cross-ref: topics/c2_exception_handling.md — error handling in functions]
