import pytest
from zipf import Zipf
import matplotlib.pyplot

@pytest.mark.skip(reason="Plot will fail on travis")
def test_plot_remap():
    z = Zipf({"one":0.2, "two":0.25, "three":0.6})
    remapper = Zipf({"three":0.7, "one":0.2})
    try:
        z.plot_remap(remapper, show = False)
    except Exception as e:
        fail()

    assert True