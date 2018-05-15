from zipf import zipf

def test_truediv():
    z = zipf({"one":0.5, "two":0.5})
    try:
        r = z/0
        assert False
    except ValueError as e:
        pass
    z2 = zipf({"one":1, "two":1})
    z3 = zipf({"one":1})
    assert (
        zipf({"one":0.25, "two":0.25}),
        z,
        zipf({"one":0.5}),
    ) == (
        z/2,
        z/z2,
        z/z3
    )