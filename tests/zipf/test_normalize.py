from zipf import zipf

def test_normalize():
    z = zipf({"one":1, "two":1})
    assert z.normalize() == zipf({"one":0.5, "two":0.5})