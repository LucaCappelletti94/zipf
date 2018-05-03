from zipf import zipf

def test_answer():
    z = zipf.load("test_zipf.json")
    assert z.mean() == 0.01123595505617977