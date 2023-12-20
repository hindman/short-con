
import sys
from dataclasses import make_dataclass
from kwexception import Kwexception

####
# Constants.
####

DEFAULT_CLS_NAME = 'ShortCon'

ERR_MULTIPLE = 'Provide positional or keyword arguments, not both'
ERR_NONE = 'No names/values given'
ERR_TYPE = 'contants() argument must be a dict, str, list, or tuple'

####
# Error class.
####

class ShortConError(Kwexception):
    '''
    Exception class for short-con library.
    '''
    pass

####
# Utility function.
####

def _tup_to_names(tup):
    # Takes a tuple of strings.
    # Returns the names after splitting the strings.
    return [
        name
        for s in tup
        for name in s.split()
    ]

####
# The libary's user-facing functions.
#
# - constants(): does most of the work; allows user to control
#   name of underlying dataclass and to supply a function to compute
#   values from names.
#
# - cons(): offers the simplest usage pattern but no customization;
#   accepts positional arguments (names only, with values to
#   be set equal to names) or keyword arguments (names and values),
#   not both.
#
# - enumcons(): similar to cons in offering simple usage; computes
#   values in an enum-like fashion.
####

def cons(*names, **kws):
    '''
    Returns a ShortCon collection of constants.

    Arguments:
    *names -- Attribute names (values will equal the names).
    **kws -- Mapping of attribute names to values.
    '''
    if names and kws:
        raise ShortConError(ERR_MULTIPLE, names = names, kws = kws)
    elif kws:
        return constants(kws)
    else:
        names = _tup_to_names(names)
        return constants(names)

def enumcons(*names, start = 1, step = 1, **kws):
    '''
    Returns a ShortCon collection of constants.

    Arguments:
    *names -- Attribute names.
    start -- First enum value.
    step -- Step used to compute subsequent enum values.
    '''
    names = _tup_to_names(names)
    d = {
        nm : start + step * i
        for i, nm in enumerate(names)
    }
    return constants(d, **kws)

def constants(attrs, cls_name = None, val_func = None):
    '''
    Returns a ShortCon collection of constants.

    Arguments:
    attrs -- Dict mapping names to values or a tuple/list/string of names.
    cls_name -- Class name for the underlying dataclass instance.
    val_func -- Callable to take a name and return corresponding value.
    '''
    # Set up two parallel lists: attribute names and instance values.
    if isinstance(attrs, dict):
        # For dict, user specifies them directly.
        names = list(attrs.keys())
        vals = list(attrs.values())
    else:
        # For string or sequence, we start with the names.
        if isinstance(attrs, str):
            names = attrs.split()
        elif isinstance(attrs, (list, tuple)):
            names = attrs
        else:
            raise ShortConError(ERR_TYPE, attrs = attrs)

        # Then create the values.
        if val_func:
            vals = [val_func(nm) for nm in names]
        else:
            vals = names

    # Raise if given no names/vals.
    if not names:
        raise ShortConError(ERR_NONE, attrs = attrs)

    # Define the dataclass.
    cls = make_dataclass(
        cls_name = cls_name or DEFAULT_CLS_NAME,
        fields = names,
        frozen = True,
    )

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

