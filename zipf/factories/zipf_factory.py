import os
from collections import defaultdict
import json
from abc import ABC


class ZipfFactory(ABC):

    _default_options = {
        "remove_stop_words": False,
        "minimum_count": 0,
        "chain_min_len": 1,
        "chain_max_len": 1,
        "chaining_character": " ",
        "chain_after_filter": False,
        "chain_after_clean": False
    }

    def __init__(self, options=None):
        self._word_filter = None
        if options is None:
            options = {}
        self._options = {**self._default_options, **options}

        self.validate_options()

        if self._options["remove_stop_words"]:
            self._load_stop_words()

    def __str__(self) -> str:
        """Prints a json dictionary representing the Zipf"""
        return json.dumps(self._options, indent=2)

    __repr__ = __str__

    def validate_options(self):
        # Validating options types
        for option in self._default_options:
            if not isinstance(self._default_options[option], type(self._options[option])):
                raise ValueError("The given option %s has value %s, type %s expected." % (
                    option, self._options[option], type(self._default_options[option])))
            if isinstance(self._options[option], int) and self._options[option] < 0:
                raise ValueError("The given option %s has value %s, negative numbers are not allowed." % (
                    option, self._options[option]))
        if self._options["chain_min_len"] > self._options["chain_max_len"]:
            raise ValueError("The option 'chain_min_len: %s' must be lower or equal to 'chain_max_len: %s'" % (
                self._options["chain_min_len"], self._options["chain_max_len"]))

    def set_word_filter(self, word_filter):
        """Sets the function that filters words"""
        self._word_filter = word_filter

    def _load_stop_words(self):
        with open(os.path.join(os.path.dirname(__file__), 'stop_words.json'), "r") as f:
            self._stop_words = json.load(f)

    def _custom_word_filter(self, element):
        if self._word_filter:
            return self._word_filter(element)
        return True

    def _stop_word_filter(self, element):
        if self._options["remove_stop_words"]:
            return element not in self._stop_words
        return True

    def _remove_low_count(self, elements):
        # remove words that appear only once

        if self._options["minimum_count"]:
            frequency = defaultdict(int)
            for element in elements:
                frequency[element] += 1

            return [el for el in elements if frequency[el] > self._options["minimum_count"]]
        return elements

    def _elements_filter(self, element):
        return self._stop_word_filter(element) and self._custom_word_filter(element)

    def _clean(self, elements):
        cleaned_elements = self._remove_low_count(elements)
        if self._options["chain_after_clean"]:
            return self._chain(cleaned_elements)
        return cleaned_elements

    def _filter(self, elements):
        if not (self._options["chain_after_filter"] or self._options["chain_after_clean"]):
            elements = self._chain(elements)
        filtered_elements = list(filter(self._elements_filter, elements))
        if self._options["chain_after_filter"]:
            return self._chain(filtered_elements)
        return filtered_elements

    def _chain(self, elements):
        if self._options["chain_min_len"] == self._options["chain_max_len"] == 1:
            return elements
        chained_elements = []
        append = chained_elements.append
        join = self._options["chaining_character"].join
        _min = self._options["chain_min_len"]
        _max = self._options["chain_max_len"]
        for i in range(len(elements)):
            for j in range(i+_min, i+_max+1):
                append(join(elements[i:j]))
        return chained_elements

    def run(self, _zipf):
        return _zipf.sort()
