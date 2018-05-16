from zipf.factories import ZipfFromFile
from factory_utils import factory_fails

def prepare(options):
    factory = ZipfFromFile(options)
    factory.set_interface(lambda f: f.read())
    return factory

def test_file_factory():
    errors = factory_fails(ZipfFromFile, "file", prepare)
    assert not errors, "errors occured:\n{}".format("\n".join(errors))