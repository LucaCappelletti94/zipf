from zipf import zipf

def test_mul():
    z = zipf({"one":0.5, "two":0.5})
    z2 = zipf({"one":1, "two":1})
    z3 = zipf({"one":1})
    assert (
        zipf({"one":1, "two":1}),
        z,
        zipf({"one":0.5}),
    ) == (
        z*2,
        z*z2,
        z*z3
    )