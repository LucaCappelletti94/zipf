from zipf.factories import ZipfFromUrl
from factory_utils import factory_fails

def prepare(options):
    factory = ZipfFromUrl(options)
    factory.set_interface(lambda r: r.text)
    return factory

def test_url_factory():
    errors = factory_fails(ZipfFromUrl, "url", prepare)
    assert not errors, "errors occured:\n{}".format("\n".join(errors))