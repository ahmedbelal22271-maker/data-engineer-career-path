# Python Dictionaries

Dictionaries store data as **key-value pairs**. They are a built-in collection type in Python for fast lookup by key.

## Keys and Values

| Property | Requirement |
|----------|-------------|
| **Keys** | Must be **immutable** (strings, integers, floats, tuples); must be **unique** |
| **Values** | Can be **any type** (immutable or mutable); **duplicates allowed** |

## Creating a Dictionary

Use curly braces `{}` with colon-separated key-value pairs:

```python
album_releases = {
    "Thriller": 1982,
    "Back in Black": 1980,
    "The Dark Side of the Moon": 1973,
}
```

## Operations

| Operation | Syntax | Description |
|-----------|--------|-------------|
| Look up value | `d[key]` | Returns value for given key |
| Add entry | `d[new_key] = value` | Adds new key-value pair |
| Delete entry | `del d[key]` | Removes key and its value |
| Check key exists | `key in d` | Returns `True` or `False` (checks keys only) |
| Get all keys | `d.keys()` | Returns `dict_keys` view object |
| Get all values | `d.values()` | Returns `dict_values` view object |

In Python 3, `.keys()` and `.values()` return **view objects**, not lists. Wrap with `list()` to convert: `list(d.keys())`.

**Key constraint:** keys must be immutable (strings, integers, tuples). Values have no type restriction.

[Cross-ref: topics/c2_lists_and_tuples.md — other collection types]
[Cross-ref: topics/c2_sets.md — sets as another unordered collection]
