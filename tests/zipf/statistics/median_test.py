from zipf import zipf

def test_answer():
    z = zipf.load("test_zipf.json")
    assert z.median() == 0.008064516129032258