from __future__ import absolute_import, unicode_literals, print_function

import pytest

@pytest.fixture
def tr():
    return TestResource()

class TestResource(object):

    CHESS_PIECES = 'KING QUEEN ROOK BISHOP KNIGHT PAWN'

    def dump(self, val = None, label = None):
        if label:
            msg = '\n{} =>'.format(label)
            print(msg)
        else:
            print()
        print(val)
        print()

