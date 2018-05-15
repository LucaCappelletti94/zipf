from zipf import zipf
from utils import fail_empty
def test_empty_max():
    errors = fail_empty(zipf.max)
    assert not errors, "errors occured:\n{}".format("\n".join(errors))