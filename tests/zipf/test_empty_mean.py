from zipf import zipf
from utils import fail_empty
def test_empty_mean():
    errors = fail_empty(zipf.mean)
    assert not errors, "errors occured:\n{}".format("\n".join(errors))