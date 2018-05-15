from zipf import Zipf

def test_missing():
    z = Zipf()
    assert z.__missing__("my_missing_key") == 0