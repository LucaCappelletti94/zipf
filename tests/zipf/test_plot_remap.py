from zipf import zipf
import matplotlib.pyplot

@pytest.mark.skip(reason="Plot will fail on travis")
def test_plot_remap():
    z = zipf({"one":0.2, "two":0.25, "three":0.6})
    remapper = zipf({"three":0.7, "one":0.2})
    try:
        z.plot_remap(remapper, show = False)
    except Exception as e:
        fail()

    assert True