import pytest
from zipf.factories import ZipfFromDir
from factory_utils import factory_fails


def prep(options):
    factory = ZipfFromDir(options=options)
    factory.set_interface(lambda f: f.read())
    return factory


def prep_word_filter(options):
    factory = ZipfFromDir(options=options)
    factory.set_interface(lambda f: f.read())
    factory.set_word_filter(lambda w: True)
    return factory


def prep_cli(options):
    factory = ZipfFromDir(options=options, use_cli=True)
    factory.set_interface(lambda f: f.read())
    return factory


def cli_no_interface(options):
    factory = ZipfFromDir(options=options, use_cli=True)
    return factory


def run(factory, data):
    return factory.run(data, ["txt"])


def enrich(factory, data, zipf):
    return factory.enrich(data, zipf, ["txt"])


# @pytest.mark.skip(reason="Test is too slow but working, currently disabled.")
def test_dir_factory():
    errors = []
    for d in ["dir"]:  # ["dir", "multi_dir", "multi_paths"]:
        # [None, prep, prep_word_filter, prep_cli, cli_no_interface]:
        for pr in [None]:
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
