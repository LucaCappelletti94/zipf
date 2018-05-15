from zipf import Zipf

def test_str():
    z = Zipf({"one":1, "two":1})
    assert (
        z,
        Zipf({"one":-1, "two":-1})
    ) == (
        -(-z),
        -z
    )