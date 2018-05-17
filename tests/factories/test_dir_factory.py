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


def cli_with_no_interface(options):
    factory = ZipfFromDir(options, use_cli=True)
    return factory


def run(factory, data):
    return factory.run(data, ["txt"])


def enrich(factory, data, zipf):
    return factory.enrich(data, zipf, ["txt"])


def test_dir_factory():
    errors = []
    for d in ["dir", "multi_dir", "multi_paths"]:
        for pr in [None, prepare, prepare_with_cli, cli_with_no_interface]:
            for r in [None, run]:
                for e in [None, enrich]:
                    errors += factory_fails(ZipfFromDir,
                                            d, prepare=pr, run=r, enrich=e)
    try:
        f = ZipfFromDir()
        f.run(None)
        errors.append(
            "Running ZipfFromDir with None paths should raise an exception")
    except ValueError as e:
        pass
    assert not errors, "errors occured:\n{}".format("\n".join(errors))
