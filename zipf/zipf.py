"""Zipf represents a Zipf distribution and offers tools to edit it easily."""
import json
from collections import OrderedDict
from functools import cmp_to_key
from operator import add, mul, sub, truediv

from numpy import mean, median, var


class Zipf(OrderedDict):
    """Zipf represents a Zipf distribution offering tools to edit it easily."""

    def __init__(self, items=None):
        """Initialize a Zipf object."""
        if items:
            super().__init__(items)
        self._unrendered = False

    def _set_key_sources(self, first_source, second_source):
        """Assign the key sources."""
        self._keys_sources = first_source, second_source

    def _set_get_sources(self, first_source, second_source, operation, keygen):
        """Assign the get sources and operation."""
        self._unrendered = True
        if isinstance(second_source, (int, float)):
            self.keys = first_source.keys
            self.__getitem__ = self._get_non_rendered_item
        else:
            self.keys = keygen
            self._set_key_sources(first_source, second_source)
            self.__getitem__ = self._get_non_rendered_item_from_zipfs
        self._get_sources = first_source, second_source, operation

    def _get_non_rendered_item_from_zipfs(self, key):
        """Return the element key combining the original zipfs."""
        first_source, second_source, operation = self._get_sources
        v = self[key]
        if not v:
            self[key] = v = operation(
                first_source.__getitem__(key),
                second_source.__getitem__(key)
            )
        return v

    def _get_non_rendered_item(self, key):
        """Return the element key combining the original zipf and value."""
        first_source, value, operation = self._get_sources
        v = self[key]
        if not v:
            self[key] = v = operation(first_source.__getitem__(key), value)
        return v

    def is_unrendered(self):
        """Return True if the object is not rendered."""
        return self._unrendered

    def __str__(self):
        """Print a json dictionary representing the Zipf."""
        if self.is_unrendered():
            self = self.render()
        return json.dumps(self, indent=2)

    _repr_html_ = __repr__ = __str__

    def __missing__(self, key):
        """Return the default value of Zipf event, 0."""
        return 0

    def _and_keys(self):
        """Combine the keys of the two sources with an and operation."""
        first_source, second_source = self._keys_sources
        for key in first_source.keys():
            if second_source.__getitem__(key):
                yield key

    def _or_keys(self):
        """Combine the keys of the two sources with an or operation."""
        first_source, second_source = self._keys_sources
        for key in second_source.keys():
            yield key
        for key in first_source.keys():
            if not second_source.__getitem__(key):
                yield key

    def __mul__(self, value):
        """Multiply the Zipf by a number or the frequency in another Zipf."""
        z = Zipf()
        z._set_get_sources(self, value, mul, z._and_keys)
        return z

    __rmul__ = __mul__

    def __truediv__(self, value):
        """Divide the Zipf by a number or the frequency in another Zipf."""
        if value == 0:
            raise ValueError("Cannot divide by zero.")
        z = Zipf()
        z._set_get_sources(self, value, truediv, z._and_keys)
        return z

    def __neg__(self):
        """Return the negated zipf."""
        return -1 * self

    def __add__(self, other):
        """Sum two Zipf."""
        z = Zipf()
        z._set_get_sources(self, other, add, z._or_keys)
        return z

    def __radd__(self, other):
        """Sum two Zipf. It is used for sum()."""
        if other == 0:
            return self
        return self.__add__(other)

    def __sub__(self, other):
        """Sub two Zipf."""
        z = Zipf()
        z._set_get_sources(self, other, sub, z._or_keys)
        return z

    def __eq__(self, other):
        """Check is two zipfs are equal."""
        if not isinstance(other, Zipf):
            return False
        if self.is_unrendered():
            self = self.render()
        if other.is_unrendered():
            other = other.render()
        return OrderedDict.__eq__(self, other)

    def render(self):
        """Render the __getitem__, so that it does not call its alias chain."""
        rendered = Zipf()
        get = self.__getitem__
        for k in self.keys():
            v = get(k)
            if v:
                rendered[k] = v
        return rendered

    def remap(self, remapper):
        """Remap Zipf to the order of another, deleting unshared elements."""
        remapped = Zipf()
        remapped._set_key_sources(remapper, self)
        remapped.keys = remapped._and_keys
        remapped._unrendered = True
        remapped.__getitem__ = self.__getitem__
        return remapped

    def normalize(self):
        """Normalize the Zipf so that the sum is equal to one."""
        self.check_empty()
        total = sum(list(self.values()))
        if total != 1:
            return self / total
        return Zipf(self)

    def cut(self, _min=0, _max=1):
        """Return a Zipf without elements below _min or above _max."""
        result = Zipf()
        for k, v in self.items():
            if v > _min and v <= _max:
                result[k] = v
        return result

    def round(self, n=14):
        """Round every frequency on zipf to a given value."""
        return Zipf({k: round(v, n) for k, v in self.items()})

    def min(self):
        """Return the value with minimal frequency in the Zipf."""
        self.check_empty()
        return min(self, key=self.get)

    def max(self):
        """Return the value with maximal frequency in the Zipf."""
        self.check_empty()
        return max(self, key=self.get)

    def mean(self):
        """Determine the mean frequency."""
        self.check_empty()
        return round(mean(list(self.values())), 14)

    def median(self):
        """Determine the median frequency."""
        self.check_empty()
        return round(median(list(self.values())), 14)

    def var(self):
        """Determine the variance in frequencies."""
        self.check_empty()
        return round(var(list(self.values())), 14)

    def is_empty(self):
        """Determine if the zipf is empty."""
        return len(self) == 0

    def check_empty(self):
        """Throws an exception is the zipf is empty and not unrendered."""
        if self.is_empty() and not self.is_unrendered():
            raise ValueError("The Zipf is empty!")

    def _compare(x, y):
        if x[1] < y[1]:
            return -1
        elif x[1] > y[1]:
            return 1
        elif x[0] < y[0]:
            return -1
        else:
            return 1

    _keysort = cmp_to_key(_compare)

    def sort(self):
        """Return the sorted Zipf, based on the frequency value."""
        return Zipf(sorted(
            self.items(),
            key=Zipf._keysort,
            reverse=True
        ))

    def items(self):
        """Yield tuple key value."""
        get = self.__getitem__
        for key in self.keys():
            value = get(key)
            if value:
                yield (key, value)

    def load(path):
        """Load a Zipf from the given path."""
        with open(path, "r") as f:
            return Zipf(json.load(f))

    def save(self, path):
        """Save the Zipf as a dictionary to a given json file."""
        with open(path, "w") as f:
            json.dump(self, f)
