from zipf import zipf

def test_answer():
    z1 = zipf({"a":1})
    z2 = zipf({"a":1})
    assert z1 == z2