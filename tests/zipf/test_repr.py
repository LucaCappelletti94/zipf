from zipf import zipf

def test_repr():
    z = zipf({"g":1})
    assert (
        repr(z),
        repr(zipf()),
        repr(z),
        repr(zipf())
    ) == (
        '{\n  "g": 1\n}',
        '{}',
        str(z),
        str(zipf())
    )