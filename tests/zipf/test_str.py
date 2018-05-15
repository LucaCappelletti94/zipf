from zipf import zipf

def test_str():
    z = zipf({"g":1})
    assert (
        str(z),
        str(zipf()),
        str(z),
        str(zipf())
    ) == (
        '{\n  "g": 1\n}',
        '{}',
        repr(z),
        repr(zipf())
    )