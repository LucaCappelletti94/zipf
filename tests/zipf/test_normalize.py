from zipf import Zipf


def test_normalize():
    z1 = Zipf({"one": 3, "two": 1})
    z2 = Zipf({"one": 1})
    assert (
        z1.normalize(),
        z2.normalize()
    ) == (
        Zipf({"one": 0.75, "two": 0.25}),
        z2
    )
