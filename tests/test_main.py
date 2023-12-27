import dataclasses
import pytest
import sys

from short_con import (
    ShortConError,
    cons,
    constants,
    enumcons,
    dc,
)
from short_con.main import (
    DEFAULT_CLS_NAME,
    ERR_MULTIPLE,
    ERR_NONE,
    ERR_TYPE,
)

####
# Chess pieces: data for constants in various formats.
####

# Pieces and their values.
CPS = dict(
    king = 0,
    queen = 9,
    rook = 5,
    bishop = 3,
    knight = 3,
    pawn = 1,
)

# Piece names as dict, tuple, list, one str, or multiple str.
CPS_DICT = dict(zip(CPS, CPS))
CPS_TUP = tuple(CPS)
CPS_LIST = list(CPS)
CPS_STR = ' '.join(CPS)
CPS_STRS = ['king queen', 'rook bishop knight', 'pawn']

####
# Tests.
####

def test_cons(tr):
    # Scenario: exercise cons() via keyword arguments, one str,
    # or multiple str with various arrangements.
    # The results should be the same in all cases.
    scs = [
        cons(**CPS_DICT),
        cons(CPS_STR),
        cons(*CPS_STRS),
        cons(*CPS_LIST),
    ]
    for sc in scs:
        assert dict(sc) == dict(scs[0])

def test_constants(tr):
    # Scenario: exercise constants() via dict, tuple, list, str.
    # The results should be the same in all cases.
    scs = [
        constants(CPS_DICT),
        constants(CPS_TUP),
        constants(CPS_LIST),
        constants(CPS_STR),
    ]
    for sc in scs:
        assert dict(sc) == dict(scs[0])

def test_enumcons(tr):
    # Scenario: exercise enumcons() via one str,
    # or multiple str with various arrangements.
    # The results should be the same in all cases.
    EXP = {nm : i + 1 for i, nm in enumerate(CPS_TUP)}
    scs = [
        enumcons(CPS_STR),
        enumcons(*CPS_STRS),
        enumcons(*CPS_LIST),
    ]
    for sc in scs:
        assert dict(sc) == EXP

def test_enumcons_custom(tr):
    # Scenario: exercise enumcons() via custom start/step.
    EXP = {nm : 100 + i * 5 for i, nm in enumerate(CPS_TUP)}
    sc = enumcons(CPS_STR, start = 100, step = 5)
    assert dict(sc) == EXP

def test_cons_multiple(tr):
    # Scenario: error if we supply both keyword and positional args.
    with pytest.raises(ShortConError) as einfo:
        cons(CPS_STR, **CPS_DICT)
    e = einfo.value
    assert e.msg == ERR_MULTIPLE

def test_no_names(tr):
    # Scenario: error if we supply no names.
    with pytest.raises(ShortConError) as einfo1:
        cons()
    with pytest.raises(ShortConError) as einfo2:
        constants([])
    with pytest.raises(ShortConError) as einfo3:
        enumcons()
    for einfo in (einfo1, einfo2, einfo3):
        e = einfo.value
        assert e.msg == ERR_NONE

def test_constants_custom_name(tr):
    # Scenario: exercise constants() with custom class name.
    CLS_NAME = 'Pieces'
    sc1 = constants(CPS)
    sc2 = constants(CPS, cls_name = CLS_NAME)
    assert type(sc1).__name__ == DEFAULT_CLS_NAME
    assert type(sc2).__name__ == CLS_NAME
    assert dict(sc1) == dict(sc2)

def test_constants_invalid_type(tr):
    # Scenario: error if constants() is given an unsupported type.
    with pytest.raises(ShortConError) as einfo:
        constants(999)
    e = einfo.value
    assert e.msg == ERR_TYPE

def test_dict_methods_added(tr):
    # Confirm that dict-like behaviors are added.
    sc = cons(**CPS)
    # Iteration, keys(), and values().
    assert list(sc) == list(CPS.items())
    assert sc.keys() == tuple(CPS.keys())
    assert sc.values() == tuple(CPS.values())
    # Getting values by name.
    Q = 'queen'
    F = 'fubb'
    assert sc[Q] == sc.queen
    assert sc[Q] == CPS[Q]
    # Length and membership.
    assert len(sc) == len(CPS)
    assert Q in sc
    assert F not in sc
    # get().
    assert sc.get(Q) == sc.queen
    assert sc.get(Q) == CPS[Q]
    assert sc.get(F) is None
    assert sc.get(F, 99) == 99

def test_dict_methods_not_added(tr):
    # Confirm that keys(), values(), get() are not added if they
    # conflict with any of the attribute names.
    d = dict(CPS)
    d.update(keys = 11, values = 22, get = 33)
    sc = cons(**d)
    assert sc.keys == 11
    assert sc.values == 22
    assert sc.get == 33

def test_constants_val_func(tr):
    # Scenario: exercise constants() with custom value function.
    sc1 = constants(CPS_STR)
    sc2 = constants(CPS_STR, val_func = str.upper)
    assert dict(sc1) == CPS_DICT
    assert dict(sc2) == {nm : nm.upper() for nm in CPS_TUP}

def test_constants_frozen(tr):
    # Exercise constants(frozen = __).
    sc1 = constants(CPS_STR)
    sc2 = constants(CPS_STR, frozen = False)
    Q = 'QUEEN!'
    F = 'FOO'

    # Initial assertions.
    assert sc1.queen == sc2.queen
    assert sc1.queen != Q

    # Scenario: by default, ShortCon instances are frozen.
    with pytest.raises(dataclasses.FrozenInstanceError) as einfo:
        sc1.queen = Q

    # Scenario: but with frozen=False, the instance is modifiable.
    sc2.queen = Q
    sc2.foo = F
    assert sc2.queen == Q
    assert sc2.foo == F
    assert sc1.queen != sc2.queen

def test_dc(tr):
    # Exercise dc().
    FIELDS = ['name', 'age', 'power', 'other']
    PARAMS = dict(name = 'Buzz', age = 33, power = 99.8)

    # Setup two classes and instances.
    Person1 = dc(*FIELDS)
    Person2 = dc(*FIELDS, cls_name = 'Person', frozen = True)
    p1 = Person1(**PARAMS)
    p2 = Person2(**PARAMS)

    # Check cls_name and repr().
    assert str(p1) == "ShortCon(name='Buzz', age=33, power=99.8, other=None)"
    assert str(p2) == "Person(name='Buzz', age=33, power=99.8, other=None)"

    # Check mutability.
    N = 100
    p1.age = N
    assert p1.age == N
    with pytest.raises(dataclasses.FrozenInstanceError) as einfo:
        p2.age = N

