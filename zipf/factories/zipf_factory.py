"""ZipfFactory creates Zipf objects."""
import json
import os

from ..zipf import Zipf


class ZipfFactory():
    """ZipfFactory creates Zipf objects."""

    _default_opts = {
        "remove_stop_words": False,
        "minimum_count": 0,
        "chain_min_len": 1,
        "chain_max_len": 1,
        "chaining_character": " ",
        "sort": True
    }

    def __init__(self, options=None):
        """Initialize a ZipfFactory with given options."""
        self._opts = {}
        self._opts.update(self._default_opts)
        if options is not None:
            self._opts.update(options)

        self._validate_opts()
        self._product = None

        if self._opts["remove_stop_words"]:
            self._load_stop_words()
        else:
            self._stop_word_filter = lambda w: True

        self._word_filter = self._stop_word_filter

        if self._opts["chain_min_len"] == self._opts["chain_max_len"] == 1:
            self._chain = lambda elements: elements

    def __str__(self):
        """Print a json dictionary representing the factory."""
        return json.dumps(self._opts, indent=2)

    _repr_html_ = __repr__ = __str__

    def _validate_opts(self):
        """Validate user options."""
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
        """Set the final product object."""
        self._product = product
        self._product_get = product.__getitem__
        self._product_set = product.__setitem__

    def get_product(self):
        """Return the elaborated product."""
        return self._product

    def set_word_filter(self, _filter):
        """Set the function that filters words."""
        self._word_filter = lambda w: _filter(w) and self._stop_word_filter(w)

    def _load_stop_words(self):
        """Load from path the stopwords."""
        path = os.path.join(os.path.dirname(__file__), 'stop_words.json')
        with open(path, "r") as f:
            self._stop_words = {}
            for w in json.load(f):
                self._stop_words[w] = None

    def _stop_word_filter(self, element):
        """Check if word is not a stopword."""
        return element not in self._stop_words

    def _filter(self, words):
        """Return generator of filtered words."""
        w = self._word_filter
        return (word for word in words if w(word))

    def _chain(self, elements):
        """Return a generator with chained words."""
        join = self._opts["chaining_character"].join
        _min = self._opts["chain_min_len"]
        _max = self._opts["chain_max_len"] + 1
        elements = list(elements)
        n = len(elements)
        n1 = n + 1
        for i in range(n):
            for j in range(i + _min,  min(i + _max, n1)):
                yield join(elements[i:j])

    def run(self, elements):
        """Return a zipf created from the given elements."""
        zipf = Zipf()
        zset = zipf.__setitem__
        zget = zipf.__getitem__
        n = 0
        gen = self._filter(self._chain(elements))
        for k in gen:
            zset(k, zget(k) + 1)
            n += 1
        _min = self._opts["minimum_count"]
        if _min > 1:
            remove = []
            append = remove.append
            for k, v in zipf.items():
                if v <= _min:
                    append(k)
                    n -= v
            for k in remove:
                del zipf[k]
        if not n:
            return zipf
        if self._product is not None:
            product_get = self._product_get
            product_set = self._product_set
            for k, v in zipf.items():
                product_set(k, product_get(k) + v / n)
        z = zipf / n
        if self._opts["sort"]:
            return z.sort()
        return z
