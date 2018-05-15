from zipf import Zipf

def test_var():
    z = Zipf({"one":0.2, "two":0.25, "three":0.6})

    assert (
        z.var()
    ) == (
        0.03166666666667
    )