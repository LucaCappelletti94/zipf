import os
import json
import pytest
from zipf import Zipf

_options_for_tests = {}

def _get_options_for(test_name):
    global _options_for_tests
    if test_name in _options_for_tests:
        return _options_for_tests[test_name]
    return None

def factory_break_options(Factory):
    non_booleans = [1,0,None,[],{},"test",10,15,-16]
    non_naturals = [True, False, -1, -10, "test", 0.5, 0.75, None, [],{}]
    non_characters = [True, False, -1, -10, 0.5, 0.75, None, [],{}]

    booleans = [True, False]
    non_zero_naturals = [1,2,3,4,5,6,7,8,9,10]
    characters = ['', ' ', '1', '-', '\n']

    wrong_options = []
    for key in ["remove_stop_words", "chain_after_filter", "chain_after_clean"]:
        wrong_option = {}
        for non_boolean in non_booleans:
            wrong_option[key] = non_boolean
        wrong_options.append(wrong_option)

    for key in ["minimum_count", "chain_min_len", "chain_max_len"]:
        wrong_option = {}
        for non_natural in non_naturals:
            wrong_option[key] = non_natural
        wrong_options.append(wrong_option)

    for key in ["chaining_character"]:
        wrong_option = {}
        for non_character in non_characters:
            wrong_option[key] = non_character
        wrong_options.append(wrong_option)

    wrong_options.append({
        "chain_min_len":10,
        "chain_max_len":1
    })

    right_options = []
    for key in ["remove_stop_words", "chain_after_filter", "chain_after_clean"]:
        right_option = {}
        for boolean in booleans:
            right_option[key] = boolean
        right_options.append(right_option)

    for key in ["minimum_count"]:
        right_option = {}
        for non_zero_natural in non_zero_naturals:
            right_option[key] = non_zero_natural
        right_options.append(right_option)

    for i in non_zero_naturals:
        right_option = {}
        right_option["chain_min_len"] = i
        for j in non_zero_naturals:
            right_option["chain_max_len"] = i+j
            right_options.append(right_option)

    right_options.append({
        "minimum_count":0
    })

    for key in ["chaining_character"]:
        right_option = {}
        for character in characters:
            right_option[key] = character
        right_options.append(right_option)

    errors = []
    for wrong_option in wrong_options:
        try:
            Factory(wrong_option)
            errors.append("Factory %s did not fail with options %s."%(Factory.__name__, wrong_option))
        except ValueError as e:
            pass

    for right_option in right_options:
        try:
            Factory(right_option)
        except ValueError as e:
            errors.append("Factory %s failed with options %s."%(Factory.__name__, right_option))
    return errors

def factory_fails(Factory, path, prepare=None):
    if prepare == None:
        prepare = Factory
    current_path = os.path.dirname(__file__)
    errors = factory_break_options(Factory)
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
        factory = prepare(_get_options_for(test))

        factory_run = factory.run(data)
        if result != factory_run:
            errors.append("%s has not expected result on run test '%s': %s != %s"%(Factory.__name__, test, result, factory_run))
        factory_enrich = factory.enrich(data, Zipf()).sort()
        if result != factory_enrich:
            errors.append("%s has not expected result on enrich test '%s': %s != %s"%(Factory.__name__, test, result, factory_enrich))
    return errors