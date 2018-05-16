from zipf.factories import ZipfFromDir
from factory_utils import factory_fails

def prepare(options):
    factory = ZipfFromDir(options)
    factory.set_interface(lambda f: f.read())
    return factory

def prepare_with_cli(options):
    factory = ZipfFromDir(options, use_cli=True)
    factory.set_interface(lambda f: f.read())
    return factory

def test_dir_factory():
    errors = factory_fails(ZipfFromDir, "dir", prepare)
    errors += factory_fails(ZipfFromDir, "dir", prepare_with_cli)
    assert not errors, "errors occured:\n{}".format("\n".join(errors))