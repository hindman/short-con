from __future__ import absolute_import, unicode_literals, print_function

import attr
import pytest
import sys

from short_con import constants, cons
from short_con.main import ERR_TYPE, ERR_VALUE

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

def test_cons(tr):
    d = tr.PIECE_VALUES
    PVals = cons('PVals', **d)
    assert dict(PVals) == d

def test_dict_methods_added(tr):
    d = tr.PIECE_VALUES
    PVals = cons('PVals', **d)
    # keys() and values().
    ks = PVals.keys()
    vs = PVals.values()
    assert isinstance(ks, tuple)
    assert isinstance(vs, tuple)
    assert sorted(ks) == sorted(d)
    assert sorted(vs) == sorted(d.values())
    # get().
    assert PVals.get('QUEEN') == d['QUEEN']
    assert PVals.get('blort', 123) == 123
    assert PVals.get('blort') is None
    # Get item.
    assert PVals['ROOK'] == d['ROOK']
    with pytest.raises(KeyError):
        PVals['blort']
    # Length.
    assert len(PVals) == len(d)
    # Contains.
    assert 'ROOK' in PVals
    assert 'blort' not in PVals

def test_dict_methods_not_added(tr):
    # In this case, keys(), values(), get() are not added to the class.
    d = dict(tr.PIECE_VALUES)
    d.update(keys = 11, values = 22, get = 33)
    PVals = cons('PVals', **d)
    assert PVals.keys == 11
    assert PVals.values == 22
    assert PVals.get == 33

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

