from utils import fail_types
def test_add_types():
    errors = fail_types(lambda z,v: z+v)
    assert not errors, "errors occured:\n{}".format("\n".join(errors))