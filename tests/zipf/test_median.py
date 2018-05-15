from zipf import zipf

def test_median():
    z = zipf({"one":0.2, "two":0.25, "three":0.6})

    assert (
        z.median()
    ) == (
        0.25
    )