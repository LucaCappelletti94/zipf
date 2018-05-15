from zipf import Zipf

def test_normalize():
    z = Zipf({"one":1, "two":1})
    assert z.normalize() == Zipf({"one":0.5, "two":0.5})