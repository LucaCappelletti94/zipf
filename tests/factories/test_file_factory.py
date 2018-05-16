from zipf.factories import ZipfFromFile
from factory_utils import factory_fails
import os

def test_list_factory():
    errors = factory_fails(ZipfFromFile, "file")
    assert not errors, "errors occured:\n{}".format("\n".join(errors))