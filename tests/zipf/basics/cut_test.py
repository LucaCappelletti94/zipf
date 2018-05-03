from zipf import zipf

def test_answer():
    z1 = zipf({"a":0.5, "b":1, "c":0.25})
    assert (
        z1.cut(min=0, max=1),
        z1.cut(min=0),
        z1.cut(max=1),
        z1.cut(max=0.5),
        z1.cut(max=0.25),
        z1.cut(min=0.25),
        z1.cut(min=0.25, max=0.5)
    ) == (
        z1,
        z1,
        z1,
        zipf({"a":0.5, "c":0.25}),
        zipf({"c":0.25}),
        zipf({"a":0.5, "b":1}),
        zipf({"a":0.5})
    )