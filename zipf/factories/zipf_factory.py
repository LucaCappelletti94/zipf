import os
from collections import defaultdict
from ..zipf import Zipf
import json


class ZipfFactory():

    _default_opts = {
        "remove_stop_words": False,
        "minimum_count": 0,
        "chain_min_len": 1,
        "chain_max_len": 1,
        "chaining_character": " ",
        "sort": True
    }

    def __init__(self, options=None):
        if options is None:
            options = {}
        self._opts = {**self._default_opts, **options}

        self.validate_opts()
        self._word_filter = lambda el: True
        self._product = None

        if self._opts["remove_stop_words"]:
            self._load_stop_words()
        else:
            self._stop_word_filter = lambda el: True
            self._filter = lambda elements: elements

        if self._opts["minimum_count"] == 0:
            self._clean = lambda elements: elements

        if self._opts["chain_min_len"] == self._opts["chain_max_len"] == 1:
            self._chain = lambda elements: elements

    def __str__(self) -> str:
        """Prints a json dictionary representing the Zipf"""
        return json.dumps(self._opts, indent=2)

    __repr__ = __str__

    def validate_opts(self):
        # Validating options types
        for opt in self._default_opts:
            if not isinstance(self._default_opts[opt], type(self._opts[opt])):
                raise ValueError("The given option %s should have type %s." % (
                    opt, type(self._default_opts[opt])))
            if isinstance(self._opts[opt], int) and self._opts[opt] < 0:
                raise ValueError("The given option %s is negative." % (opt))
        _min = self._opts["chain_min_len"]
        _max = self._opts["chain_max_len"]
        if _min > _max:
            raise ValueError("min %s must be <= max %s" % (_min, _max))

    def set_product(self, product):
        self._product = product
        self._product_get = product.__getitem__
        self._product_set = product.__setitem__

    def get_product(self):
        return self._product

    def set_word_filter(self, word_filter):
        """Sets the function that filters words"""
        self._word_filter = word_filter
        self._filter = lambda elements: ZipfFactory._filter(self, elements)

    def _load_stop_words(self):
        path = os.path.join(os.path.dirname(__file__), 'stop_words.json')
        with open(path, "r") as f:
            self._stop_words = {}
            for w in json.load(f):
                self._stop_words[w] = None

    def _stop_word_filter(self, element):
        return element not in self._stop_words

    def _filter(self, elements):
        for element in elements:
            if self._stop_word_filter(element) and self._word_filter(element):
                yield element

    def _clean(self, elements):
        frequency = defaultdict(int)
        elements = list(elements)
        for element in elements:
            frequency[element] += 1

        _min = self._opts["minimum_count"]
        get = frequency.__getitem__

        return (el for el in elements if get(el) > _min)

    def _chain(self, elements):
        chained_elements = []
        append = chained_elements.append
        join = self._opts["chaining_character"].join
        _min = self._opts["chain_min_len"]
        _max = self._opts["chain_max_len"]
        elements = list(elements)
        n = len(elements)
        for i in range(n):
            for j in range(i+_min,  min(i+_max+1, n+1)):
                yield join(elements[i:j])

    def run(self, elements):
        zipf = Zipf()
        zget = zipf.__getitem__
        zset = zipf.__setitem__
        n = 0
        for el in self._clean(self._filter(self._chain(elements))):
            zset(el, zget(el)+1)
            n += 1
        if not n:
            return zipf
        if self._product is not None:
            product_get = self._product_get
            product_set = self._product_set
            for k, v in zipf.items():
                product_set(k, product_get(k)+v/n)
        z = zipf/n
        if self._opts["sort"]:
            return z.sort()
        return z
