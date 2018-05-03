from zipf import zipf

def test_answer():
    z1 = zipf({"a":1})
    assert "a" in z1