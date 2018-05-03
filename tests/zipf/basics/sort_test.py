from zipf import zipf

def test_answer():
    z1 = zipf({"a":0.5, "b":1})
    z2 = zipf({"b":1, "a":0.5})
    assert z1.sort() == z2