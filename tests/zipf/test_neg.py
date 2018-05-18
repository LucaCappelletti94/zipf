from zipf import Zipf


def test_neg():
    z = Zipf({"one": 1, "two": 0.5})
    assert (
        z,
        Zipf({"two": -0.5, "one": -1})
    ) == (
        (-(-z)).sort(),
        (-z).sort()
    )
