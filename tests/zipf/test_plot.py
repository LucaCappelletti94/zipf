import pytest
from zipf import Zipf
import matplotlib.pyplot

@pytest.mark.skip(reason="Plot will fail on travis")
def test_plot():
    z = Zipf({"one":0.2, "two":0.25, "three":0.6})
    try:
        z.plot(show = False)
    except Exception as e:
        fail()

    assert True