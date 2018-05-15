from zipf import Zipf

def test_max():
    z = Zipf({"one":0.2, "two":0.25, "three":0.6})

    assert (
        z.max()
    ) == (
        "three"
    )