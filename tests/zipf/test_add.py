from zipf import Zipf


def test_add():
    z = Zipf({"one": 0.5, "two": 0.4})
    z2 = Zipf({"one": 0.25, "four": 0.25})
    z3 = Zipf({"three": 1})
    assert (
        Zipf({"one": 1, "two": 0.8}),
        Zipf(),
        Zipf({"one": 0.75, "two": 0.4, "four": 0.25}),
        Zipf({"three": 1, "one": 0.75, "two": 0.4, "four": 0.25}),
    ) == (
        (z+z).sort(),
        (z+(-z)).sort(),
        (z+z2).sort(),
        (z+z2+z3).sort()
    )
