from zipf import Zipf

def test_str():
    z = Zipf({"g":1})
    assert (
        str(z),
        str(Zipf()),
        str(z),
        str(Zipf())
    ) == (
        '{\n  "g": 1\n}',
        '{}',
        repr(z),
        repr(Zipf())
    )