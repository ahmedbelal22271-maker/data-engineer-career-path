# Python Objects and Classes

Everything in Python is an **object** — every object has a **type**, an **internal representation**, and **methods** to interact with it.

## Classes and Instances

A **class** is a blueprint. An **object** is an instance of a class.

```python
class Circle(object):
    def __init__(self, radius, color):
        self.radius = radius
        self.color = color

class Rectangle(object):
    def __init__(self, height, width, color):
        self.height = height
        self.width = width
        self.color = color
```

In Python 3, explicitly inheriting from `object` is optional (all classes inherit from `object` implicitly).

## Creating Objects

```python
red_circle = Circle(4, "red")
blue_rect = Rectangle(2, 2, "blue")
```

Access attributes with dot notation: `red_circle.radius` → `4`.

## Methods

Methods are functions defined on a class that interact with the object's data.

```python
class Circle(object):
    def __init__(self, radius, color):
        self.radius = radius
        self.color = color

    def add_radius(self, r):
        self.radius += r
```

- `self` refers to the instance itself.
- `self` is not passed manually when calling the method.
- Methods can modify data attributes directly.

## The `dir()` Function

`dir(object)` returns a list of all attributes and methods on an object.

## Key Concepts

- **Constructor:** `__init__` initializes new instances
- **Data attributes:** variables that define the object's state
- **Methods:** functions that operate on the object
- **Instantiation:** creating an object from a class

[Cross-ref: topics/c2_functions.md — functions are similar to methods]
[Cross-ref: topics/c2_python_basics.md — Python data types as objects]
