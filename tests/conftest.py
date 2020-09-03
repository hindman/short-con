from __future__ import absolute_import, unicode_literals, print_function

import pytest

@pytest.fixture
def tr():
    return TestResource()

class TestResource(object):

    def __init__(self):
        pass

    def dumpj(self, val = None, label = None):
        val = to_json(val, indent = 4)
        self.dump(val, label)

    def dump(self, val = None, label = None):
        if label:
            msg = '\n{} =>'.format(label)
            print(msg)
        else:
            print()
        print(val)
        print()

