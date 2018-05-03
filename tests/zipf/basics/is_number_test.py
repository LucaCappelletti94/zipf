from zipf import zipf

def test_answer():
    z = zipf()
    n = z._is_number
    assert (
        n(0),
        n(0.1),
        n(True),
        n(False),
        n(None),
        n("ciao"),
        n(zipf()),
        n(z),
        n((-1+0j))
    ) == (
        True,
        True,
        False,
        False,
        False,
        False,
        False,
        False,
        False
    )