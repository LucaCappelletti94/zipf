from utils import fail_types_no_num
def test_mul_types():
    errors = fail_types_no_num(lambda z,v: z*v)
    assert not errors, "errors occured:\n{}".format("\n".join(errors))