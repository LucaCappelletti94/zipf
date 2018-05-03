import os
from zipf import zipf

def test_answer():
    path = os.path.join(os.path.dirname(__file__), "test_zipf.json")
    z = zipf.load(path)
    assert z.var() == 6.959332145835021e-05