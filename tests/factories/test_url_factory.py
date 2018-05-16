from zipf.factories import ZipfFromUrl
from factory_utils import factory_fails
import os

def test_url_factory():
    errors = factory_fails(ZipfFromUrl, "url")
    assert not errors, "errors occured:\n{}".format("\n".join(errors))