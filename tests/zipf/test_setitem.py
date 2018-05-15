from zipf import zipf
from utils import fail_types_no_num

def test_setitem():
    z = zipf()
    z["my_key"] = 0.5

    assert z == zipf({"my_key":0.5})