from zipf.factories import ZipfFromUrl
from factory_utils import factory_fails
import httpretty

def prepare(options):
    factory = ZipfFromUrl(options)
    factory.set_interface(lambda r: r.text)
    return factory

@httpretty.activate
def test_url_factory():
    with open("tests/factories/factory_utils/dir/default/default.txt", "r") as f:
        data = f.read()
    base_url = "https://raw.githubusercontent.com/LucaCappelletti94/zipf/master/tests/factories/factory_utils/text/"
    httpretty.register_uri(httpretty.GET, base_url+"default.txt", body=data)
    httpretty.register_uri(httpretty.GET, base_url+"empty.txt", body="")
    errors = factory_fails(ZipfFromUrl, "url", prepare)
    assert not errors, "errors occured:\n{}".format("\n".join(errors))