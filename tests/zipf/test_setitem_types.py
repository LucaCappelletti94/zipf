from utils import fail_types_no_num
def test_setitem_types():
    errors = fail_types_no_num(lambda z,v: z.__setitem__(0,v))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))