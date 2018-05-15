from zipf import zipf

def test_mean():
    z = zipf({"one":0.2, "two":0.25, "three":0.6})

    assert (
        z.mean()
    ) == (
        0.35
    )