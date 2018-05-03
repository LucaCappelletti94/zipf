from zipf import zipf

def test_answer():
    z1 = zipf({"a":0.5, "b":0.5})
    z2 = zipf({"a":1, "b":1})
    assert (z2/0.5, z1/z2) == (z2, z1)