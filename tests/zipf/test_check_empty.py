from zipf import Zipf

def test_check_empty():
    z = Zipf({"one":0.2, "two":0.25, "three":0.6})

    raised = False

    try:
        Zipf().check_empty()
    except ValueError as e:
        raised = True

    try:
        z.check_empty()
    except ValueError as e:
        raised = False

    assert raised == True