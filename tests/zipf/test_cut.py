from zipf import Zipf

def test_cut():
    z = Zipf({"one":0.2, "two":0.25, "three":0.6})

    assert (
        z.cut(0.2),
        z.cut(0.25),
        z.cut(0.6),
        z.cut(0, 0.6),
        z.cut(0.2, 0.6),
        z.cut(0.25, 0.6),
        z.cut(0.2, 0.25)
    ) == (
        Zipf({"two":0.25, "three":0.6}),
        Zipf({"three":0.6}),
        Zipf(),
        z,
        Zipf({"two":0.25, "three":0.6}),
        Zipf({"three":0.6}),
        Zipf({"two":0.25})
    )