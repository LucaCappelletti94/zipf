from zipf import Zipf
from utils import fail_empty
def test_empty_min():
    errors = fail_empty(Zipf.min)
    assert not errors, "errors occured:\n{}".format("\n".join(errors))