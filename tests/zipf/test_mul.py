from zipf import Zipf


def test_mul():
    z = Zipf({"one": 0.75, "two": 0.5})
    z2 = Zipf({"one": 1.0, "two": 1.0})
    z3 = Zipf({"one": 1.0})

    assert (
        Zipf({"one": 1.5, "two": 1.0}),
        z,
        Zipf({"one": 0.75}),
    ) == (
        z*2,
        (z*z2).sort(),
        (z*z3).sort()
    )
