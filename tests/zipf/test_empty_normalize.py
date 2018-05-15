from zipf import Zipf
from utils import fail_empty
def test_empty_normalize():
    errors = fail_empty(Zipf.normalize)
    assert not errors, "errors occured:\n{}".format("\n".join(errors))