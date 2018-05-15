from zipf import zipf

def test_missing():
    z = zipf()
    assert z.__missing__("my_missing_key") == 0