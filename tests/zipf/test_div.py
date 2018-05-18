from zipf import Zipf


def test_truediv():
    z = Zipf({"one": 1, "two": 0.5})
    try:
        r = z/0
        assert False
    except ValueError as e:
        pass
    z2 = Zipf({"one": 1, "two": 1})
    z3 = Zipf({"one": 1})
    assert (
        Zipf({"one": 0.5, "two": 0.25}),
        z,
        Zipf({"one": 1}),
    ) == (
        z/2,
        (z/z2).sort(),
        (z/z3).sort()
    )
