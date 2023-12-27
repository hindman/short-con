## short-con: Constants collections without hassle

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
add some derived constants. We've hardly gotten out of the gate and the journey
already seems tedious.

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

Although there are use cases where such formalism might be desirable, in the
vast majority of practical programming situations the intermediate object is
just a hassle — a form of *robustness theater* rather than an actual best
practice with concrete benefits.

#### An easier way

The short-con project simplifies the creation of constants collections: just
supply names and values via keyword arguments.

```python
from short_con import cons

PIECES = cons(king = 0, queen = 9, rook = 5, bishop = 3, knight = 3, pawn = 1)
```

Behind the scenes `cons()` defines a frozen dataclass and then returns an
instance of that class.

```python
Pieces.queen = 99   # Fails with FrozenInstanceError.
```

The underlying values are directly accessible — no need to interact with a
bureaucratic object standing guard in the middle:

```python
PIECES.queen == 9  # True
```

The object is directly iterable and convertible to other collections, in the
manner of `dict.items()`:

```python
for name, value in PIECES:
    print(name, value)

d = dict(PIECES)
tups = list(PIECES)
```

The object also supports relevant read-only dict behaviors:

```python
# Always supported.
PIECES['queen']      # 9
len(PIECES)          # 6
'queen' in PIECES    # True

# Supported if the attribute names do not conflict with the method names.
PIECES.keys()        # ('king', 'queen', 'rook', 'bishop', 'knight', 'pawn')
PIECES.values()      # (0, 9, 5, 3, 3, 1)
PIECES.get('rook')   # 5
PIECES.get('blort')  # None
```

For situations when the values are the same as the attribute names, usage is
even more compact: just supply names as positional arguments or via one or more
space-delimited strings.

```python
COLORS = cons('black white')
COLORS = cons('black', 'white')

print(COLORS)  # ShortCon(black='black', white='white')
```

#### Easier enums

In the same spirit of reducing hassle, the library supports the creation of
enum-like collections: supply the names and, optionally, start and step
parameters to control the generation of the numeric values.

```python
PETS1 = enumcons('dog cat parrot')
PETS2 = enumcons('dog cat parrot', start = 100, step = -10)

print(PETS1)  # ShortCon(dog=1, cat=2, parrot=3)
print(PETS2)  # ShortCon(dog=100, cat=90, parrot=80)
```

#### More control when needed

The library also provides a `constants()` function that supports (1) the
ability to control the class name of the underlying dataclass, (2) use cases
where the constant values can be computed from the names, and (3) the ability
to control whether the dataclass is frozen (default is true).

```python
COLORS = constants(
    'black white',         # Names/values (dict) or names (list, tuple, str)
    cls_name = 'Colors',
    val_func = str.upper,  # Callable: f(NAME) => VALUE
    frozen = False,
)

COLORS.black += '_'
print(COLORS)  # Colors(black='BLACK_', white='WHITE')
```

#### Quick and dirty dataclasses

Since we are in the business of making dataclasses, the library also provides a
convenience function to create them with a simplicity analogous to the `cons()`
function. The user provides the attributes names and, optionally, a class name
or any other keyword arguments for `dataclasses.make_dataclass()`. The
attributes of the returned dataclass are optional, with a default of `None`,
and have a type of `typing.Any`.

```python
Person = dc('name age hobby')
p = Person(name = 'Billy', age = 42)
print(p)  # ShortCon(name='Billy', age=42, hobby=None)

Soldier = dc('name', 'rank', 'serial', cls_name = 'Soldier', frozen = True)
s = Soldier(name = 'Leonard', rank = 'Private')
print(s)  # Soldier(name='Leonard', rank='Private', serial=None)
```

----

[enum_url]: https://docs.python.org/3/library/enum.html

