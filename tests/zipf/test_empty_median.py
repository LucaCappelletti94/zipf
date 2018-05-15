from zipf import Zipf
from utils import fail_empty
def test_empty_median():
    errors = fail_empty(Zipf.median)
    assert not errors, "errors occured:\n{}".format("\n".join(errors))