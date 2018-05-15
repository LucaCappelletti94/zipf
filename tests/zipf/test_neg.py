from zipf import zipf

def test_str():
    z = zipf({"one":1, "two":1})
    assert (
        z,
        zipf({"one":-1, "two":-1})
    ) == (
        -(-z),
        -z
    )