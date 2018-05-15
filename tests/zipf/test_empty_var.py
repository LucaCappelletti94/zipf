from zipf import Zipf
from utils import fail_empty
def test_empty_var():
    errors = fail_empty(Zipf.var)
    assert not errors, "errors occured:\n{}".format("\n".join(errors))