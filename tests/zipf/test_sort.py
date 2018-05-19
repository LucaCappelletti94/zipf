from zipf import Zipf


def test_sort():
    z = Zipf({"one": 0.2, "two": 0.25, "three": 0.6})

    assert (
        Zipf({"three": 0.6, "two": 0.25, "one": 0.2})
    ) == (
        z.sort()
    )
