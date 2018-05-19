import os
from collections import defaultdict
import json
from abc import ABC


class ZipfFactory(ABC):

    _default_opts = {
        "remove_stop_words": False,
        "minimum_count": 0,
        "chain_min_len": 1,
        "chain_max_len": 1,
        "chaining_character": " ",
        "chain_after_filter": False,
        "chain_after_clean": False
    }

    def __init__(self, options=None):
        if options is None:
            options = {}
        self._opts = {**self._default_opts, **options}

        self.validate_opts()
        self._word_filter = lambda el: True

        if self._opts["remove_stop_words"]:
            self._load_stop_words()
        else:
            self._stop_word_filter = lambda el: True

        if self._opts["minimum_count"] == 0:
            self._remove_low_count = lambda elements: elements

        if self._opts["chain_min_len"] == self._opts["chain_max_len"] == 1:
            self._chain = lambda elements: elements

    def __str__(self) -> str:
        """Prints a json dictionary representing the Zipf"""
        return json.dumps(self._opts, indent=2)

    __repr__ = __str__

    def validate_opts(self):
        # Validating options types
        for option in self._default_opts:
            if not isinstance(self._default_opts[option], type(self._opts[option])):
                raise ValueError("The given option %s has value %s, type %s expected." % (
                    option, self._opts[option], type(self._default_opts[option])))
            if isinstance(self._opts[option], int) and self._opts[option] < 0:
                raise ValueError("The given option %s has value %s, negative numbers are not allowed." % (
                    option, self._opts[option]))
        if self._opts["chain_min_len"] > self._opts["chain_max_len"]:
            raise ValueError("The option 'chain_min_len: %s' must be lower or equal to 'chain_max_len: %s'" % (
                self._opts["chain_min_len"], self._opts["chain_max_len"]))

    def set_word_filter(self, word_filter):
        """Sets the function that filters words"""
        self._word_filter = word_filter

    def _load_stop_words(self):
        with open(os.path.join(os.path.dirname(__file__), 'stop_words.json'), "r") as f:
            self._stop_words = {}
            for w in json.load(f):
                self._stop_words[w] = None

    def _stop_word_filter(self, element):
        return element not in self._stop_words

    def _remove_low_count(self, elements):
        frequency = defaultdict(int)
        for element in elements:
            frequency[element] += 1

        return [el for el in elements if frequency[el] > self._opts["minimum_count"]]

    def _elements_filter(self, element):
        return self._stop_word_filter(element) and self._word_filter(element)

    def _clean(self, elements):
        cleaned_elements = self._remove_low_count(elements)
        if self._opts["chain_after_clean"]:
            return self._chain(cleaned_elements)
        return cleaned_elements

    def _filter(self, elements):
        if not (self._opts["chain_after_filter"] or self._opts["chain_after_clean"]):
            elements = self._chain(elements)
        filtered_elements = list(filter(self._elements_filter, elements))
        if self._opts["chain_after_filter"]:
            return self._chain(filtered_elements)
        return filtered_elements

    def _chain(self, elements):
        chained_elements = []
        append = chained_elements.append
        join = self._opts["chaining_character"].join
        _min = self._opts["chain_min_len"]
        _max = self._opts["chain_max_len"]
        for i in range(len(elements)):
            for j in range(i+_min, i+_max+1):
                append(join(elements[i:j]))
        return chained_elements

    def run(self, _zipf):
        return _zipf.sort()
