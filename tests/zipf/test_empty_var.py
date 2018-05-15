from zipf import zipf
from utils import fail_empty
def test_empty_var():
    errors = fail_empty(zipf.var)
    assert not errors, "errors occured:\n{}".format("\n".join(errors))