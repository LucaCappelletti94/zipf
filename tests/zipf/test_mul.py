from zipf import Zipf

def test_mul():
    z = Zipf({"one":0.5, "two":0.5})
    z2 = Zipf({"one":1, "two":1})
    z3 = Zipf({"one":1})
    assert (
        Zipf({"one":1, "two":1}),
        z,
        Zipf({"one":0.5}),
    ) == (
        z*2,
        z*z2,
        z*z3
    )