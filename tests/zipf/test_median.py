from zipf import Zipf

def test_median():
    z = Zipf({"one":0.2, "two":0.25, "three":0.6})

    assert (
        z.median()
    ) == (
        0.25
    )