from zipf import Zipf

def test_getitem():
    z = Zipf({"g":1})
    assert (
        z.__getitem__("g"),
        z["no_key"],
        z.__getitem__("g")
    ) == (
        1,
        0,
        z["g"]
    )