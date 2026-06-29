# Python Exception Handling

Exception handling allows a program to respond to errors **gracefully** — outputting a meaningful message and continuing — rather than crashing.

## The `try…except` Statement

```python
try:
    file = open("data.txt", "r")
    data = file.read()
except IOError:
    print("Unable to open or read the data in the file.")
```

## Multiple `except` Clauses

```python
try:
    file = open("data.txt", "r")
    data = file.read()
except IOError:
    print("Unable to open or read the file.")
except:
    print("An error occurred.")
```

**Best practice:** Always specify the exception type. Bare `except:` catches everything but provides no debugging information.

## `else` and `finally`

| Clause | Runs when |
|--------|-----------|
| `else` | `try` block completes **without any exception** |
| `finally` | **Always** — used for cleanup (e.g., closing files) |

```python
try:
    file = open("data.txt", "w")
    file.write("Some data")
except IOError:
    print("Unable to open or read the file.")
else:
    print("File written successfully.")
finally:
    file.close()
```

## Common Exceptions

| Exception | Raised when |
|-----------|-------------|
| `ZeroDivisionError` | Dividing by zero |
| `ValueError` | Inappropriate value (e.g., `int("abc")`) |
| `FileNotFoundError` | Accessing a non-existent file |
| `IndexError` | List index out of range |
| `KeyError` | Non-existent dictionary key |
| `TypeError` | Incompatible type operation (e.g., `"hello" + 5`) |
| `AttributeError` | Accessing non-existent attribute/method |
| `ImportError` | Importing unavailable module |

[Cross-ref: topics/c2_functions.md — functions as context for exception handling]
