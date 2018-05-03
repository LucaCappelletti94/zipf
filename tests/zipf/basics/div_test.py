from zipf import zipf

def test_answer():
    z1 = zipf({"a":0.5, "b":0.25})
    z2 = zipf({"a":1, "b":1})
    assert (
        z1/0.5, (z1/z2).sort()
    ) == (
        zipf({"a":1, "b":0.5}), z1
    )