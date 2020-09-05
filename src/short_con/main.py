from __future__ import absolute_import, unicode_literals, print_function

import attr
import six
import sys

ERR_TYPE = 'attrs argument must be a str, list, tuple, or dict.'
ERR_VALUE = "value_style argument must be None, 'upper', 'lower', 'enum', or function."

def constants(name, attrs, value_style = None, bases = (object,), **attributes_arguments):

    # Set up two parallel lists: attribute names and instance values.
    if isinstance(attrs, dict):
        # For dict, user specifies them directly.
        names = list(attrs.keys())
        vals = list(attrs.values())
    else:
        # For string or sequence, we start with the names.
        if isinstance(attrs, six.string_types):
            names = attrs.split()
        elif isinstance(attrs, (list, tuple)):
            names = attrs
        else:
            raise TypeError(ERR_TYPE)

        # Then create values based on value_style.
        if value_style is None:
            vals = names
        elif value_style == 'upper':
            vals = [nm.upper() for nm in names]
        elif value_style == 'lower':
            vals = [nm.lower() for nm in names]
        elif value_style == 'enum':
            vals = [i + 1 for i in range(len(names))]
        elif callable(value_style):
            vals = [value_style(i, nm) for i, nm in enumerate(names)]
        else:
            raise ValueError(ERR_VALUE)

    # Create the attrs class.
    attributes_arguments.setdefault('frozen', True)
    cls_name = name if sys.version_info.major >= 3 else name.encode('utf-8') 
    cls = attr.make_class(cls_name, names, bases, **attributes_arguments)

    # Add support for direct iteration.
    cls.__iter__ = lambda self: iter(attr.asdict(self).items())

    # Return an instance holding the constants.
    return cls(*vals)

