from zipf import zipf

def test_getitem():
    z = zipf({"g":1})
    assert (
        z.__getitem__("g"),
        z.__getitem__("no_key"),
        z.__getitem__("g")
    ) == (
        1,
        0,
        z["g"]
    )