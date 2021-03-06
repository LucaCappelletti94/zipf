from zipf.factories import ZipfFromKSequence
from zipf import Zipf
import os
import pytest


def test_ksequence_factory():

    errors = []

    try:
        ZipfFromKSequence(-3)
        errors.append("ZipfFromKSequence should fail with k less than zero")
    except Exception as e:
        pass

    k = 5

    factory = ZipfFromKSequence(k)

    current_path = os.path.dirname(__file__)+"/factory_utils"

    zipf = Zipf.load(
        current_path+"/expected_results/sequence.json").sort().round()

    with open(current_path+"/sequence/sequence.txt", "r") as f:
        sequence = f.read()

    factory_run = factory.run(sequence).round()

    if factory_run != zipf:
        errors.append(
            "Sequence zipf run is different than expected: %s != %s" % (zipf, factory_run))

    assert not errors, "errors occured:\n{}".format("\n".join(errors))
