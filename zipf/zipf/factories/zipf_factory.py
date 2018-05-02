import os
from collections import defaultdict
class zipf_factory:

    _default_options = {
        "remove_stop_words":False,
        "minimum_count":0
    }

    def __init__(self, options = None):
        self._word_filter = None
        if custom_options == None:
            custom_options = {}
        self._options = {**self._default_options, **options}

        if self._options["remove_stop_words"]:
            self._load_stop_words()

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
                for token in element:
                    frequency[token] += 1


            return [[token for token in element if frequency[token] > self._options["minimum_count"]]
                     for element in elements]
        return elements

    def _elements_filter(self, element):
        return self._stop_word_filter(element) and self._custom_word_filter(element)

    def _clean(self, elements):
        return self._remove_low_count(elements)

    def _filter(self, elements):
        return list(filter(self._elements_filter, elements))

    def run(self, _zipf):
        return _zipf.sort()