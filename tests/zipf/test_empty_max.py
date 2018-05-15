from zipf import Zipf
from utils import fail_empty
def test_empty_max():
    errors = fail_empty(Zipf.max)
    assert not errors, "errors occured:\n{}".format("\n".join(errors))