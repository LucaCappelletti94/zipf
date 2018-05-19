from collections import OrderedDict
from zipf import Zipf


def _tests_no_num():
    return ["this should fail", True, False, (-1+0j), [], OrderedDict(), None]


def _tests_num():
    return [1, 1.0, -1, -1.0]


def _fail_types(lamb, tests):
    z = Zipf()
    errors = []
    for test in tests:
        try:
            result = lamb(z, test)
            errors.append(
                "Set has not raised exception with value %s" % fail_test)
        except ValueError as e:
            pass
    return errors


def fail_types(lamb):
    return _fail_types(lamb, _tests_num() + _tests_no_num())


def fail_types_no_num(lamb):
    return _fail_types(lamb, _tests_no_num())


def fail_empty(lamb):
    errors = []
    try:
        lamb(Zipf())
        errors.append("Set has not raised exception with empty Zipf")
    except ValueError as e:
        pass
    return errors
