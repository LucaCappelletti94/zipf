import os
import json
import pytest
from zipf import Zipf

_options_for_tests = {}

def _get_options_for(test_name):
    global _options_for_tests
    if test_name in _options_for_tests:
        return _options_for_tests[test_name]
    return {}

def factory_fails(Factory, path):
    current_path = os.path.dirname(__file__)
    errors = []
    for test in ["default", "empty"]:
        data_path_json = os.path.join(current_path, "%s/%s.json"%(path, test))
        data_path_text = os.path.join(current_path, "%s/%s.txt"%(path, test))
        result_path = os.path.join(current_path, "expected_results/%s.json"%test)
        if os.path.isfile(data_path_json):
            with open(data_path_json, "r") as f:
                data = json.load(f)
        elif os.path.isfile(data_path_text):
            with open(data_path_text, "r") as f:
                data = f.read()
        else:
            pytest.skip("While testing %s, data for testing '%s' was not found in %s or %s."%(Factory.__name__, test, data_path_text, data_path_json))
        if not os.path.isfile(result_path):
            pytest.skip("While testing %s, result for testing '%s' was not found in %s."%(Factory.__name__, test, result_path))
        result = Zipf.load(result_path)
        factory = Factory(_get_options_for(test))

        if result != factory.run(data):
            errors.append("%s has not expected result on run test '%s'"%(Factory.__name__, test))
        if result != factory.enrich(data, Zipf()).sort():
            errors.append("%s has not expected result on enrich test '%s'"%(Factory.__name__, test))
    return errors