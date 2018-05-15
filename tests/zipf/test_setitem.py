from zipf import Zipf
from utils import fail_types_no_num

def test_setitem():
    z = Zipf()
    z["my_key"] = 0.5

    assert z == Zipf({"my_key":0.5})