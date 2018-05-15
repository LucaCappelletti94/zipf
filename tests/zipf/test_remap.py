from zipf import zipf

def test_remap():
    z = zipf({"one":0.2, "two":0.25, "three":0.6})
    remapper = zipf({"three":0.7, "one":0.2})

    assert zipf({"three":0.6, "one":0.2}) == z.remap(remapper)