from zipf.factories import ZipfFromText
from factory_utils import factory_fails


def test_text_factory():
    errors = factory_fails(ZipfFromText, "text")
    assert not errors, "errors occured:\n{}".format("\n".join(errors))
