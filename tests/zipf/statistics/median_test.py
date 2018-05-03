import os
from zipf import zipf

def test_answer():
    path = os.path.join(os.path.dirname(__file__), "test_zipf.json")
    z = zipf.load(path)
    assert z.median() == 0.008064516129032258