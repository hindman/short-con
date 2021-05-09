## short-con: Constants collections without boilerplate

#### Motivation

When your Python code needs constants, the process often starts simply enough
with the worthy goal of getting the magic strings and numbers out of your code.

```python
BLACK = 'black'
WHITE = 'white'

KING = 0
QUEEN = 9
ROOK = 5
BISHOP = 3
KNIGHT = 3
PAWN = 1
```

At some point, you might need to operate on those constants in groups, so you
add some derived constants. We've hardly gotten out of the gate and the process
already seems a bit tedious.

```python
COLORS = (BLACK, WHITE)
PIECES = (KING, QUEEN, ROOK, BISHOP, KNIGHT, PAWN)
```

Starting in Python 3.4, the [enum library][enum_url] became available:

```python
from enum import Enum

Colors = Enum('Colors', 'BLACK WHITE')
Pieces = Enum('Pieces', dict(KING = 0, QUEEN = 9, ROOK = 5, BISHOP = 3, KNIGHT = 3, PAWN = 1))
```

Although that library helps a lot, there is one annoyance. We started with the
simple goal of wrangling magic strings and values, but we end up forced to
interact with special `enum` instances:

```python
Pieces.QUEEN        # Will this give us the value we want? No.
Pieces.QUEEN.value  # Dig a level deeper, friend.
```

Although there are use cases where such formalism might be desirable, in
the vast majority of practical programming situations the intermediate object
is just a hassle — a form of *robustness theater* rather than an actual best
practice with concrete benefits.


#### An easier way

A better approach is to take inspiration from the excellent [attrs
library][attrs_url], which helps Python programmers create *classes without
boilerplate*. The short-con project does the same for constants collections by
providing a small wrapper around [attr.make_class][make_class_url].

Constant names and values can be declared explicitly in two ways:

```python
from short_con import constants, cons

# Via a dict.
Pieces = constants('Pieces', dict(king = 0, queen = 9, rook = 5, bishop = 3, knight = 3, pawn = 1))

# Via kwargs, using the cons() utility function.
Pieces = cons('Pieces', king = 0, queen = 9, rook = 5, bishop = 3, knight = 3, pawn = 1)
```

Both `constants()` and `cons()` create an attrs-based class of the given name
and return a frozen instance of it:

```python
Pieces.queen = 42   # Fails with attrs.FrozenInstanceError.
```

The underlying values are directly accessible — no need to interact with some
bureaucratic object standing guard in the middle:

```python
Pieces.queen == 9   # True
```

The object is directly iterable and convertible to other collections, in the
manner of `dict.items()`:

```python
for name, value in Pieces:
    print(name, value)

d = dict(Pieces)
tups = list(Pieces)
```

The object also supports relevant read-only dict behaviors:

```python
# Always supported.
Pieces['queen']      # 9
len(Pieces)          # 6
'queen' in Pieces    # True

# Supported if the supplied attribute names do not conflict with the method names:
Pieces.keys()        # ('king', 'queen', 'rook', 'bishop', 'knight', 'pawn')
Pieces.values()      # (0, 9, 5, 3, 3, 1)
Pieces.get('rook')   # 5
Pieces.get('blort')  # None
```

For situations when the values are the same as (or can be derived from) the
attribute names, usage is even more compact. Just supply names as a list,
tuple, or space-delimited string.

```python
NAMES = 'KING QUEEN ROOK BISHOP KNIGHT PAWN'
nms = NAMES.split()

Pieces = constants('Pieces', NAMES)      # All of these do the same thing.
Pieces = constants('Pieces', nms)
Pieces = constants('Pieces', tuple(nms))
```

The name-based usages support a few stylistic conventions:

```python
NAMES = 'KING QUEEN ROOK BISHOP KNIGHT PAWN'
names = NAMES.lower()

Pieces = constants('Pieces', NAMES, value_style = 'lower') # Uppercase names, lowercase values.
Pieces = constants('Pieces', names, value_style = 'upper') # The reverse.
Pieces = constants('Pieces', NAMES, value_style = 'enum')  # An enumeration from 1 through N.
```

Or the values can be computed from the names by supplying a two-argument
callable that takes an index and name:

```python
Pieces = constants('Pieces', NAMES, value_style = lambda i, name: f'{name.lower()}-{i + 1}')
```

Other customization of the attrs-based class can be passed through as well. The
`constants()` function has the following signature. The `bases` and
`attr_arguments` are passed directly through to
[attr.make_class][make_class_url]. Note that the `cons()` utility function does
not support such customizations. And neither function allows the user to get a
non-frozen instance, which would be at odds with the purpose of the library.

```python
def constants(name, attrs, value_style = None, bases = (object,), **attr_arguments):
    ...
```

----

[stackoverflow_url]: https://stackoverflow.com/questions/2682745
[enum_url]: https://docs.python.org/3/library/enum.html
[attrs_url]: https://www.attrs.org/en/stable/
[make_class_url]: https://www.attrs.org/en/stable/api.html#attr.make_class

