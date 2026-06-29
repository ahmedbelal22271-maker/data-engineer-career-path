# Python Sets

Sets are **unordered collections of unique elements**. Useful for removing duplicates and performing mathematical set operations.

## Properties

| Property | Set |
|----------|-----|
| Ordered | No |
| Duplicates allowed | No |
| Mutable | Yes |

## Creating a Set

```python
A = {"ACDC", "BackInBlack", "inSync"}  # curly braces
my_set = set(my_list)                   # typecast list to set (removes duplicates)
```

## Operations

| Operation | Syntax | Description |
|-----------|--------|-------------|
| Add element | `s.add(x)` | No effect if element already present |
| Remove element | `s.remove(x)` | Removes element; error if missing |
| Membership | `x in s` | Returns `bool` |
| Intersection | `s1 & s2` | Elements in **both** sets (AND) |
| Union | `s1 \| s2` | All elements from **either** set |
| Subset check | `s1.issubset(s2)` | `True` if all of `s1` is in `s2` |

```python
AlbumSet3 = AlbumSet1 & AlbumSet2           # intersection
AlbumSetUnion = AlbumSet1 | AlbumSet2        # union
AlbumSet3.issubset(AlbumSet1)                # True
```

[Cross-ref: topics/c2_lists_and_tuples.md — ordered collections]
[Cross-ref: topics/c2_dictionaries.md — key-value collections]
