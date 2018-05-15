from zipf import zipf

def test_cut():
    z = zipf({"one":0.2, "two":0.25, "three":0.6})

    assert (
        z.cut(0.2),
        z.cut(0.25),
        z.cut(0.6),
        z.cut(0, 0.6),
        z.cut(0.2, 0.6),
        z.cut(0.25, 0.6),
        z.cut(0.2, 0.25)
    ) == (
        zipf({"two":0.25, "three":0.6}),
        zipf({"three":0.6}),
        zipf(),
        z,
        zipf({"two":0.25, "three":0.6}),
        zipf({"three":0.6}),
        zipf({"two":0.25})
    )