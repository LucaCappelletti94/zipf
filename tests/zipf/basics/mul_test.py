from zipf import zipf

def test_answer():
    z1 = zipf({"a":0.5, "b":0.5})
    z2 = zipf({"a":1, "b":0.5})
    assert (
        z1*2, 2*z1, (z1*z2).sort(), (z2*z1).sort()
    ) == (
        zipf([("a", 1), ("b",2)]),
        zipf([("a", 1), ("b",2)]),
        zipf([("a", 0.5), ("b",0.25)]),
        zipf([("a", 0.5), ("b",0.25)])
    )