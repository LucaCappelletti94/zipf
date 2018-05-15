from zipf import Zipf

def test_repr():
    z = Zipf({"g":1})
    assert (
        repr(z),
        repr(Zipf()),
        repr(z),
        repr(Zipf())
    ) == (
        '{\n  "g": 1\n}',
        '{}',
        str(z),
        str(Zipf())
    )