import os
from zipf import Zipf

def test_save_and_load():
    path = "save_and_load_test.json"
    z1 = Zipf({"one":0.2, "two":0.25, "three":0.6})
    z1.save(path)
    z2 = Zipf.load(path)
    os.remove(path)
    assert z1 == z2