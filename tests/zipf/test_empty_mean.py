from zipf import Zipf
from utils import fail_empty
def test_empty_mean():
    errors = fail_empty(Zipf.mean)
    assert not errors, "errors occured:\n{}".format("\n".join(errors))