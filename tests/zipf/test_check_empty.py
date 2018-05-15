from zipf import zipf

def test_check_empty():
    z = zipf({"one":0.2, "two":0.25, "three":0.6})

    raised = False

    try:
        zipf().check_empty()
    except ValueError as e:
        raised = True

    try:
        z.check_empty()
    except ValueError as e:
        raised = False

    assert raised == True