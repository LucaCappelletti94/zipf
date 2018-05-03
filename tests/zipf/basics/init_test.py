import json
from zipf import zipf

def test_answer():
    d = {"a":1}
    z = zipf(d)
    assert str(z) == json.dumps(d, indent=2)