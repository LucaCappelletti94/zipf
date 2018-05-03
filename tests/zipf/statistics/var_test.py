from zipf import zipf

def test_answer():
    z = zipf.load("test_zipf.json")
    assert z.var() == 6.959332145835021e-05