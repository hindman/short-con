from __future__ import absolute_import, unicode_literals, print_function

import attr
import pytest
import sys

from short_con.main import constants, ERR_TYPE, ERR_VALUE

def test_basic_creation(tr):
    # Attribute names for some constants: as a str and as a list.
    cps_str = tr.CHESS_PIECES
    cps = cps_str.split()
    cps_tuple = tuple(cps)
    cps_dict = dict(zip(cps, cps))
    exp_list = list(zip(cps, cps))
    exp_dict = dict(zip(cps, cps))

    # We can create a constants() instance using a whitespace-delimited
    # string, a list, or a tuple. And the resulting instance can be
    # directly converted into the expected list or dict.
    for arg in (cps, cps_str, cps_tuple, cps_dict):
        Pieces = constants('Pieces', arg)
        assert Pieces.QUEEN == 'QUEEN'
        assert dict(Pieces) == exp_dict
        assert attr.asdict(Pieces) == exp_dict
        if sys.version_info.major < 3:
            assert sorted(list(Pieces)) == sorted(exp_list)
        else:
            assert list(Pieces) == exp_list

def test_value_styles(tr):
    cps = tr.CHESS_PIECES

    # Lower.
    Pieces = constants('Pieces', cps, value_style = 'lower')
    assert Pieces.QUEEN == 'queen'

    # Upper.
    Pieces = constants('Pieces', cps.lower(), value_style = 'upper')
    assert Pieces.queen == 'QUEEN'

    # Enum.
    Pieces = constants('Pieces', cps, value_style = 'enum')
    assert Pieces.KING == 1
    assert Pieces.PAWN == 6

    # Callable.
    f = lambda i, name: '{}-{}'.format(name.lower(), i + 1)
    Pieces = constants('Pieces', cps, value_style = f)
    assert Pieces.KING == 'king-1'
    assert Pieces.PAWN == 'pawn-6'

def test_invalid_inputs(tr):
    # Bad attrs argument.
    with pytest.raises(TypeError, match = ERR_TYPE) as einfo:
        Pieces = constants('Pieces', 123)

    # Bad value_style.
    with pytest.raises(ValueError, match = ERR_VALUE) as einfo:
        Pieces = constants('Pieces', tr.CHESS_PIECES, value_style = 'fubb')

