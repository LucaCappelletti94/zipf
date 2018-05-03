from zipf import zipf

def test_answer():
    z1 = zipf({"a":0.5, "b":0.5})
    z2 = zipf({"a":0.5})
    assert z1[:1] == z2