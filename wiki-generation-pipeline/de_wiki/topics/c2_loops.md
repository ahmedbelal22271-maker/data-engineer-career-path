# Python Loops

Loops execute a block of code repeatedly. Two types: **`for` loops** (iterate over sequences) and **`while` loops** (repeat while a condition holds).

## The `range()` Function

```python
range(3)        # 0, 1, 2
range(10, 15)   # 10, 11, 12, 13, 14
```

In Python 3, `range()` returns a **range object** (not a list), which behaves like a sequence.

## `for` Loops

### Iterating with Index
```python
squares = ['red', 'yellow', 'green', 'purple', 'blue']
for i in range(5):
    squares[i] = 'white'
```

### Iterating Directly (No Index)
```python
for square in squares:
    print(square)
```

### Using `enumerate()` (Index + Element)
```python
for i, square in enumerate(squares):
    print(i, square)
```

## `while` Loops

Run **as long as a condition is `True`**:

```python
squares = ['orange', 'orange', 'purple', 'orange']
new_squares = []
i = 0
while squares[i] == 'orange':
    new_squares.append(squares[i])
    i += 1
```

## Loop Comparison

| Feature | `for` Loop | `while` Loop |
|---------|-----------|-------------|
| Iterations | Determined by sequence length | Determined by runtime condition |
| Requires sequence | Yes | No |
| Stops when | Sequence exhausted | Condition becomes `False` |
| Index access | Via `range()` or `enumerate()` | Manual increment |

[Cross-ref: topics/c2_conditions_branching.md — conditions used in while loops]
[Cross-ref: topics/c2_functions.md — using loops inside functions]
