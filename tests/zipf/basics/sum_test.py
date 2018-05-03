from zipf import zipf

def test_answer():
    z1 = zipf({"a":1})
    z2 = zipf({"b":0.5})
    z3 = zipf({"a":1, "b":0.5})
    assert (z1+z2).sort() == z3