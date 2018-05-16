import os
import json
from zipf import Zipf
from zipf.factories import Zipf_from_list

def test_list_factory():
    current_path = os.path.dirname(__file__)
    path = os.path.join(current_path, "zipf_from_list.json")
    path_default = os.path.join(current_path, "zipf_default.json")
    z = Zipf.load(path_default)
    factory = Zipf_from_list()
    with open(path, "r") as f:
        data = json.load(f)
    assert z == factory.run(data) == factory.enrich(data, Zipf()).sort()