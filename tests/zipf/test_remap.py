from zipf import Zipf

def test_remap():
    z = Zipf({"one":0.2, "two":0.25, "three":0.6})
    remapper = Zipf({"three":0.7, "one":0.2})

    assert Zipf({"three":0.6, "one":0.2}) == z.remap(remapper)