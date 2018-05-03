import os
from zipf import zipf

def test_answer():
    path = os.path.join(os.path.dirname(__file__), "test_zipf.json")
    z = zipf.load(path)
    assert z.mean() == 0.01123595505617977