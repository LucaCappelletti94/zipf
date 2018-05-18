from zipf import Zipf


def test_sub():
    z = Zipf({"one": 0.5, "two": 0.5})
    z2 = Zipf({"one": 0.25, "four": 0.25})
    z3 = Zipf({"three": 1})
    assert (
        Zipf(),
        Zipf({"two": 0.5, "one": 0.25, "four": -0.25}),
        Zipf({"two": 0.5, "one": 0.25, "four": -0.25, "three": -1}),
    ) == (
        z-z,
        (z-z2).sort(),
        (z-z2-z3).sort()
    )
