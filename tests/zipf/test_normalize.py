from zipf import Zipf

def test_normalize():
    z1 = Zipf({"one":1, "two":1})
    z2 = Zipf({"one":1})
    assert (
        z1.normalize(),
        z2.normalize()
    ) == (
        Zipf({"one":0.5, "two":0.5}),
        z2
    )