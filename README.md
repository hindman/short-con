## short-con: Constants without boilerplate


#### Motivation

When your Python code needs constants, the process often starts simply enough
with the worthy goal of getting the magic strings and numbers out of your code.

    KING = 'king'
    QUEEN = 'queen'
    ROOK = 'rook'
    BISHOP = 'bishop'
    KNIGHT = 'knight'
    PAWN = 'pawn'

At some point, you might need to operate on those constants in groups, so you
add some derived constants:

    PIECES = (KING, QUEEN, ROOK, BISHOP, KNIGHT, PAWN)

We've hardly gotten out of the gate and the process already seems a bit tedious.

In addition, since none of those entities are very constant-like, clever Python
programmers have created [many ways][stackoverflow_url] to create constants
beyond those simple approaches. Usually, the focus of those efforts is on
ratcheting up immutability. But achieving truly constant values is somewhat
beside the point in Python. The real annoyances have always more practical in
nature.

Starting in Python 3.4, the [enum library][enum_url] became available, and it
helps a lot:

    from enum import Enum

    # A simple Enum with values from 1 through N.
    Pieces = Enum('Pieces', 'KING QUEEN ROOK BISHOP KNIGHT PAWN')

    # Or an Enum with custom values.
    d = dict(KING = 'king', QUEEN = 'queen', ROOK = 'rook', BISHOP = 'bishop', KNIGHT = 'knight', PAWN = 'pawn')
    Pieces = Enum('Pieces', d)

But even that solution is more than one usually wants. We started with the very
simple goal of removing magic strings, numbers, and other simple values from
the code and grouping those values in meaningful ways. But we ended up being
forced to deal with an intermediate object that serves almost no purpose. Every
time you want access to an underlying value, you have to dig down an extra
level: for example, `Pieces.QUEEN.value` as opposed to just `Pieces.QUEEN`. The
primitive value (an immutable string) is already constant-enough and
robust-enough for the vast majority of use cases. Very little is gained by
forcing coders to interact with an intermediate `enum` object that was never a
goal to begin with.


#### An easier way

A better approach is to take inspiration from the excellent [attrs
library][attrs_url], which helps Python programmers create "classes without
boilerplate". The short-con project provides a small convenience wrapper around
[attr.make_class][make_class_url] to create handy vehicles for constants.

Attribute names can be supplied in the form of a list, tuple, or
space-delimited string.

    from short_con import constants

    NAMES = 'KING QUEEN ROOK BISHOP KNIGHT PAWN'
    xs = NAMES.split()

    # All of these do the same thing.
    Pieces = constants('Pieces', NAMES)
    Pieces = constants('Pieces', xs)
    Pieces = constants('Pieces', tuple(xs))

By default, `constants()` creates a frozen attrs-based class of the given name
and returns an instance of it. That instance is immutable enough for most use
cases:

    Pieces.QUEEN = 'foobar'   # Fails with attrs.FrozenInstanceError.

The underlying values are directly accessible -- no need to interact with some
bureaucratic object sitting in the middle:

    assert Pieces.QUEEN == 'QUEEN'

The object is directly iterable and convertible to other collections:

    for name, value in Pieces:
        print(name, value)

    d = dict(Pieces)
    tups = list(Pieces)

Various stylistic conventions are supported:

    NAMES = 'KING QUEEN ROOK BISHOP KNIGHT PAWN'
    names = NAMES.lower()

    # Uppercase names, lowercase values.
    Pieces = constants('Pieces', NAMES, value_style = 'lower')

    # Or the reverse.
    Pieces = constants('Pieces', names, value_style = 'upper')

    # An enumeration from 1 through N.
    Pieces = constants('Pieces', NAMES, value_style = 'enum')

Values can be declared explicitly in two ways:

    # A dict.
    d = dict(king = 0, queen = 9, rook = 5, bishop = 3, knight = 3, pawn = 1)
    Pieces = constants('Pieces', d)

    # A callable taking an INDEX and NAME and returning a VALUE.
    f = lambda i, name: '{}-{}'.format(name.lower(), i + 1)
    Pieces = constants('Pieces', NAMES, value_style = f)

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

