import pytest

@pytest.fixture
def tr():
    return TestResource()

class TestResource:

    @classmethod
    def dump(cls, val = None, label = 'dump()', iterate = False):
        fmt = '\n--------\n# {label} =>\n{val}'
        msg = fmt.format(label = label, val = '' if iterate else val)
        print(msg)
        if iterate:
            for x in val:
                print(x)

    @classmethod
    def dumpj(cls, val = None, label = 'dumpj()', indent = 4):
        val = json.dumps(val, indent = indent)
        cls.dump(val, label)

