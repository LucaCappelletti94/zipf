from zipf.factories import ZipfFromList
from factory_utils import factory_fails


def test_list_factory():
    errors = factory_fails(ZipfFromList, "list")
    assert not errors, "errors occured:\n{}".format("\n".join(errors))
