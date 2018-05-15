from zipf import zipf
from utils import fail_empty
def test_empty_min():
    errors = fail_empty(zipf.min)
    assert not errors, "errors occured:\n{}".format("\n".join(errors))