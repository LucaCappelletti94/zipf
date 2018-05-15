from zipf import zipf
import matplotlib.pyplot

def test_plot():
    z = zipf({"one":0.2, "two":0.25, "three":0.6})
    try:
        z.plot(show = False)
    except Exception as e:
        fail()

    assert True