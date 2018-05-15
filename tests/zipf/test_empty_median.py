from zipf import zipf
from utils import fail_empty
def test_empty_median():
    errors = fail_empty(zipf.median)
    assert not errors, "errors occured:\n{}".format("\n".join(errors))