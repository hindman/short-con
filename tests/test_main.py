from __future__ import absolute_import, unicode_literals, print_function

import pytest

from short_con.main import constants

def test_constants(tr):
    exp = 42
    got = constants()
    assert exp == got

