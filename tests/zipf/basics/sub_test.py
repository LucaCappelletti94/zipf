from zipf import zipf

def test_answer():
    z1 = zipf({"a":1})
    z2 = zipf({"b":1})
    z3 = zipf({"a":1, "b":-1})
    assert (z1-z2).sort() == z3