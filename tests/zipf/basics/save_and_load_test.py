import os
from zipf import zipf

def test_answer():
    path = "save_and_load_test.json"
    z1 = zipf({"a":1})
    z1.save(path)
    z2 = zipf.load(path)
    os.remove(path)
    assert z1 == z2