## short-con: Constants without boilerplate


#### Motivation

When your Python code needs constants, the process often starts simply enough
with the worthy goal of getting the magic strings and numbers out of your code.

    BLACK = 'black'
    WHITE = 'white'

    KING = 0
    QUEEN = 9
    ROOK = 5
    BISHOP = 3
    KNIGHT = 3
    PAWN = 1

At some point, you might need to operate on those constants in groups, so you
add some derived constants. We've hardly gotten out of the gate and the process
already seems a bit tedious.

    COLORS = (BLACK, WHITE)
    PIECES = (KING, QUEEN, ROOK, BISHOP, KNIGHT, PAWN)

Starting in Python 3.4, the [enum library][enum_url] became available:

    from enum import Enum

    Colors = Enum('Colors', 'BLACK WHITE')
    Pieces = Enum('Pieces', dict(KING = 0, QUEEN = 9, ROOK = 5, BISHOP = 3, KNIGHT = 3, PAWN = 1))

Although that library helps a lot, there is one annoyance. We started with the
simple goal of wrangling magic strings and values, but we end up forced to
interact with special `enum` instances:

    Pieces.QUEEN        # Will this give us the number we want? No.
    Pieces.QUEEN.value  # Dig a level deeper, friend.

Although there are use cases where such formalism might be desirable, in
the vast majority of practical programming situations the intermediate object
is just a hassle -- a form of *robustness theater* rather than an actual best
practice with concrete benefits.


#### An easier way

A better approach is to take inspiration from the excellent [attrs
library][attrs_url], which helps Python programmers create *classes without
boilerplate*. The short-con project does the same for constants by providing a
small wrapper around [attr.make_class][make_class_url].

Constant names and values can be declared explicitly in two ways:

    from short_con import constants, cons

    # Via a dict.
    Pieces = constants('Pieces', dict(king = 0, queen = 9, rook = 5, bishop = 3, knight = 3, pawn = 1))

    # Via kwargs, using the cons() utility function.
    Pieces = cons('Pieces', king = 0, queen = 9, rook = 5, bishop = 3, knight = 3, pawn = 1)

By default, `constants()` and `cons()` create an attrs-based class of the given
name and returns a frozen instance of it:

    Pieces.QUEEN = 42   # Fails with attrs.FrozenInstanceError.

The underlying values are directly accessible -- no need to interact with some
bureaucratic object standing guard in the middle:

    assert Pieces.QUEEN == 9

The object is directly iterable and convertible to other collections:

    for name, value in Pieces:
        print(name, value)

    d = dict(Pieces)
    tups = list(Pieces)

For situations when the values are the same as (or can be derived from) the
attribute names, usage is even more compact. Just supply names as a
space-delimited string, list, or tuple.

    NAMES = 'KING QUEEN ROOK BISHOP KNIGHT PAWN'
    nms = NAMES.split()

    Pieces = constants('Pieces', NAMES)      # All of these do the same thing.
    Pieces = constants('Pieces', nms)
    Pieces = constants('Pieces', tuple(nms))

The name-based usages support a few stylistic conventions:

    NAMES = 'KING QUEEN ROOK BISHOP KNIGHT PAWN'
    names = NAMES.lower()

    Pieces = constants('Pieces', NAMES, value_style = 'lower') # Uppercase names, lowercase values.
    Pieces = constants('Pieces', names, value_style = 'upper') # The reverse.
    Pieces = constants('Pieces', NAMES, value_style = 'enum')  # An enumeration from 1 through N.

Or the values can be computed from the names by supplying a two-argument
callable taking an index and name and returning a value:

    Pieces = constants('Pieces', NAMES, value_style = lambda i, name: f'{name.lower()}-{i + 1}')

Other customization of the attrs-based class can be passed through as well. The
`constants()` function has the following signature, and the `bases` and
`attributes_arguments` are passed through to [attr.make_class][make_class_url].

    def constants(name, attrs, value_style = None, bases = (object,), **attributes_arguments):
        ...


----

[stackoverflow_url]: https://stackoverflow.com/questions/2682745
[enum_url]: https://docs.python.org/3/library/enum.html
[attrs_url]: https://www.attrs.org/en/stable/
[make_class_url]: https://www.attrs.org/en/stable/api.html#attr.make_class

