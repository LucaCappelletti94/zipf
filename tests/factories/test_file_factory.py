from zipf.factories import ZipfFromFile
from factory_utils import factory_fails

def test_file_factory():
    errors = factory_fails(ZipfFromFile, "file")
    assert not errors, "errors occured:\n{}".format("\n".join(errors))