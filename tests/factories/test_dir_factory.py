from zipf.factories import ZipfFromDir
from factory_utils import factory_fails

def test_dir_factory():
    errors = factory_fails(ZipfFromDir, "dir")
    assert not errors, "errors occured:\n{}".format("\n".join(errors))