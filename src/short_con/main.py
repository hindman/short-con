import dataclasses
import typing

from kwexception import Kwexception

####
# The libary's user-facing functions to create constants collections:
#
# - constants(): Does most of the work. Allows user to control
#   name of underlying dataclass, to supply a function to compute
#   values from names, to control whether the class is frozen.
#
# - cons(): Offers the simplest usage pattern, but no customization.
#   Accepts positional arguments (names only, with values to
#   be set equal to names) or keyword arguments (names and values),
#   not both.
#
# - enumcons(): Similar to cons in offering simple usage. Computes
#   values in an enum-like fashion, with optional start/step values.
#
# - fmtcons(): Similar to cons in offering simple usage. Values can be
#   Python format strings: the ultimate values are created via an
#   iterative process using str.format(). Useful when some values need to
#   be built from other values (eg a group of paths where some paths are
#   built via other paths in the collection).
####

def cons(*names, **kws):
    '''
    Returns a ShortCon collection of constants.

    Arguments:
    *names -- Attribute names.
    **kws -- Mapping of attribute names to values.
    '''
    if names and kws:
        raise ShortConError(ERR_MULTIPLE, names = names, kws = kws)
    elif kws:
        return constants(kws)
    else:
        return constants(names)

def enumcons(*names, start = 1, step = 1, **kws):
    '''
    Returns a ShortCon collection of constants.

    Arguments:
    *names -- Attribute names.
    start -- First enum value.
    step -- Step used to compute subsequent enum values.
    '''
    d = {
        nm : start + step * i
        for i, nm in enumerate(_names_from_args(names))
    }
    return constants(d, **kws)

def fmtcons(**kws):
    '''
    Returns a ShortCon collection of constants.

    Arguments:
    **kws -- Mapping of attribute names to values/format-strings.
    '''
    return constants(kws, fmt = True)

def constants(attrs, cls_name = None, val_func = None, frozen = True, fmt = False):
    '''
    Returns a ShortCon collection of constants.

    Arguments:
    attrs -- Dict mapping names to values, or a tuple/list/str of names.
    cls_name -- Class name for the underlying dataclass instance.
    frozen -- Bool controlling whether the dataclass will be frozen.
    val_func -- Callable to take a name and return corresponding value.
    fmt -- Bool controlling whether to resolve format string values.
    '''
    # Set up two parallel lists: attribute names and instance values.
    if isinstance(attrs, dict):
        # For dict, user specifies them directly, optionally with format strings.
        if fmt:
            attrs = _formatted(attrs)
        names = list(attrs.keys())
        vals = list(attrs.values())
    else:
        # Raise if user set fmt True but did not supply a dict.
        if fmt:
            raise ShortConError(ERR_FMT_TYPE, attrs = attrs)

        # For str/list/tuple, validate and convert to flat list of names.
        names = _names_from_args(attrs)

        # Then create the values.
        if val_func:
            vals = [val_func(nm) for nm in names]
        else:
            vals = names

    # Raise if given no names/vals.
    if not names:
        raise ShortConError(ERR_NONE, attrs = attrs)

    # Define the dataclass.
    cls = dc(*names, cls_name = cls_name, frozen = frozen)

    # Add support for:
    # - iteration
    # - getting a value by name
    # - length
    # - membership
    cls.__iter__ = lambda self: iter(self.__dict__.items())
    cls.__getitem__ = lambda self, k: self.__dict__[k]
    cls.__len__ = lambda self: len(self.__dict__)
    cls.__contains__ = lambda self, k: k in self.__dict__

    # If no conflicts, add support for read-only dict methods.
    if 'keys' not in names:
        cls.keys = lambda self: tuple(self.__dict__.keys())
    if 'values' not in names:
        cls.values = lambda self: tuple(self.__dict__.values())
    if 'get' not in names:
        cls.get = lambda self, *xs: self.__dict__.get(*xs)

    # Return an instance holding the constants.
    return cls(*vals)

####
# The libary's user-facing function to create dataclasses.
####

def dc(*names, cls_name = None, **kws):
    '''
    Returns a dataclass with default settings and optional attributes.

    Arguments:
    *names -- Attribute names (fields will have typing.Any and default of None).
    cls_name -- Name for the dataclass.
    **kws -- Other keyword arguments passed to dataclasses.make_dataclass().
    '''
    fields = [
        (nm, typing.Any, dataclasses.field(default = None))
        for nm in _names_from_args(names)
    ]
    return dataclasses.make_dataclass(
        cls_name = cls_name or DEFAULT_CLS_NAME,
        fields = fields,
        **kws,
    )

####
# Constants.
####

DEFAULT_CLS_NAME = 'ShortCon'

ERR_MULTIPLE = 'Provide positional or keyword arguments, not both'
ERR_NONE = 'No names/values given'
ERR_UNRESOLVABLE = 'Unresolvable format-string references'
ERR_FMT_TYPE = 'constants() argument must be a dict if fmt=True'
ERR_NAMES_TYPE = 'Name arguments must be strings'

####
# Error class.
####

class ShortConError(Kwexception):
    '''
    Exception class for short-con library.
    '''
    pass

####
# Utility functions.
####

def _names_from_args(args):
    # Takes a str, list, or tuple of names, where the latter are either simple
    # names (eg 'foo') or whitespace-delimited names (eg 'foo bar').
    # Returns a flat list of names.
    if isinstance(args, str):
        return args.split()
    elif isinstance(args, (list, tuple)):
        names = []
        for n in args:
            if not isinstance(n, str):
                raise ShortConError(ERR_NAMES_TYPE, val = n)
            names.extend(n.split())
        return names
    else:
        raise ShortConError(ERR_NAMES_TYPE, attrs = args)

def _formatted(orig_kws):
    # Takes a dict of names and values where some values might
    # be format-strings that depend on other values in the collection.
    #
    # Values are resolved via successive passes. Non-string values are used
    # as-is. For string values, each pass resolves whatever entries are
    # unblocked by kws so far.
    #
    # Format strings blocked by still-missing keys (KeyError below) are
    # retried on the next pass.
    #
    # Raises if a pass makes zero progress, which signals a dependency cycle
    # or a reference to a nonexistent key.

    # Setup: we will return kws.
    todo = dict(orig_kws)
    kws = {}

    # Perform the str.format() conversions of the values.
    # Continue until todo is exhausted or we make no progress.
    while todo:
        progress = False
        for k, v in tuple(todo.items()):
            if isinstance(v, str):
                # String values. Try to run them through the formatting
                # process. KeyError means we still lack the needed values
                # to succeed, so we'll retry on a subsequent pass.
                try:
                    kws[k] = v.format(**kws)
                    del todo[k]
                    progress = True
                except KeyError:
                    pass
            else:
                # Non-string values: use as-is.
                kws[k] = v
                del todo[k]
                progress = True
        if not progress:
            raise ShortConError(ERR_UNRESOLVABLE, todo = todo)

    # Return a dict in the declaration order of the original data.
    return {k: kws[k] for k in orig_kws}

