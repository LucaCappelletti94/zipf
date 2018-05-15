from zipf import zipf

def test_var():
    z = zipf({"one":0.2, "two":0.25, "three":0.6})

    assert (
        z.var()
    ) == (
        0.03166666666667
    )