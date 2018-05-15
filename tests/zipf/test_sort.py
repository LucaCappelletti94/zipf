from zipf import zipf

def test_sort():
    z = zipf({"one":0.2, "two":0.25, "three":0.6})

    assert (
        zipf({"three":0.6, "two":0.25, "one":0.2})
    ) == (
        z.sort()
    )