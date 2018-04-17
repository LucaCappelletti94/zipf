from .factories.from_dir.from_dir import from_dir
from collections import OrderedDict
import json

class zipf:
    def __init__(self, data):
        self._data = OrderedDict(data)

    def from_dir(path, file_interface=None, word_filter=None, output_file=None, use_cli=False):
        fd = from_dir(path, output_file, use_cli)
        fd.set_interface(file_interface)
        fd.set_word_filter(word_filter)
        data = fd.run()
        return zipf(data)

    def load(path):
        with open(path, "r") as f:
            return zipf(json.load(f))

    def save(self, path):
        with open(path, "w") as f:
            json.load(self._data, f)

    def __str__(self):
        return str(self._data)