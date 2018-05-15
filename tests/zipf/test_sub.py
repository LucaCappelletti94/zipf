from zipf import zipf

def test_sub():
    z = zipf({"one":0.5, "two":0.5})
    z2 = zipf({"one":0.25, "four":0.25})
    z3 = zipf({"three":1})
    assert (
        zipf(),
        zipf({"one":0.25, "two":0.5, "four":-0.25}).sort(),
        zipf({"one":0.25, "two":0.5, "three":-1, "four":-0.25}).sort(),
    ) == (
        z-z,
        (z-z2).sort(),
        (z-z2-z3).sort()
    )