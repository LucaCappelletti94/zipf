from __future__ import division
from typing import Union
from collections import OrderedDict
from functools import cmp_to_key
import json
from numpy import mean, median, var
from .utils import is_number


class Zipf(OrderedDict):
    """Zipf represents a Zipf distribution offering tools to edit it easily"""

    def __init__(self, items=None):
        if items:
            super().__init__(items)
        self._unrendered = False

    def _set_unrendered(self):
        self._unrendered = True

    def is_unrendered(self):
        return self._unrendered

    def __str__(self):
        """Prints a json dictionary representing the Zipf"""
        if self.is_unrendered():
            self = self.render()
        return json.dumps(self, indent=2)

    __repr__ = __str__

    def __missing__(self, key):
        """The default value of an event in the Zipf is 0"""
        return 0

    def and_keygen(self, other):
        # big, small = self.smaller(other)

        def getkeys():
            for key in self.keys():
                if other.__getitem__(key):
                    yield key

        return getkeys

    def or_keygen(self, other):
        def getkeys():
            for key in other.keys():
                yield key
            for key in self.keys():
                if not other.__getitem__(key):
                    yield key

        return getkeys

    def __mul__(self, value):
        """Multiplies the Zipf by a number or the frequency in another Zipf.

            Args:
                value: a Zipf or a number to be multiplies with the Zipf.

            Returns:
                The multiplied Zipf

        """

        z = Zipf()
        z._set_unrendered()
        if is_number(value):
            def getitem(key):
                return self.__getitem__(key)*value
            z.keys = self.keys
        else:
            def getitem(key):
                return self.__getitem__(key)*value.__getitem__(key)
            z.keys = self.and_keygen(value)
        z.__getitem__ = getitem
        return z

    __rmul__ = __mul__

    def __truediv__(self, value):
        """Divides the Zipf by a number or the frequency in another Zipf.

            Args:
                value: either a Zipf or a number to divide the Zipf.

            Returns:
                The divided Zipf

        """

        z = Zipf()
        z._set_unrendered()
        if is_number(value):
            if value == 0:
                raise ValueError("Division by zero.")

            def getitem(key):
                return self.__getitem__(key)/value
            z.keys = self.keys
        else:
            def getitem(key):
                return self.__getitem__(key)/value.__getitem__(key)
            z.keys = self.and_keygen(value)
        z.__getitem__ = getitem
        return z

    def __neg__(self):
        z = Zipf()
        z._set_unrendered()

        def getitem(key):
            return -self.__getitem__(key)
        z.__getitem__ = getitem
        z.keys = self.keys
        return z

    def __add__(self, other):
        """Sums two Zipf
            Args:
                other: a given Zipf to be summed

            Returns:
                The summed Zipfs

        """
        z = Zipf()
        z._set_unrendered()

        def getitem(key):
            return self.__getitem__(key)+other.__getitem__(key)
        z.__getitem__ = getitem
        z.keys = self.or_keygen(other)
        return z

    def __radd__(self, other):
        if other == 0:
            return self
        return self + other

    def __sub__(self, other):
        """Subtracts two Zipf
            Args:
                other: a given Zipf to be subtracted

            Returns:
                The subtracted Zipfs

        """
        z = Zipf()
        z._set_unrendered()

        def getitem(key):
            return self.__getitem__(key)-other.__getitem__(key)
        z.__getitem__ = getitem
        z.keys = self.or_keygen(other)
        return z

    def __eq__(self, other):
        if self.is_unrendered():
            self = self.render()
        if other.is_unrendered():
            other = other.render()

        return OrderedDict.__eq__(self, other)

    def render(self):
        """Renders the __getitem__, so that it does not call its alias chain"""
        rendered = Zipf()
        get = self.__getitem__
        for k in self.keys():
            v = get(k)
            if v:
                rendered[k] = v
        return rendered

    def remap(self, remapper):
        """Remaps Zipf to the order of another, deleting unshared elements.

            Args:
                remapper: a Zipf that is used to remap the current Zipf

            Returns:
                the remapped Zipf

        """
        remapped = Zipf()
        for key, value in remapper.items():
            if key in self:
                remapped[key] = self[key]
        return remapped

    def normalize(self):
        """Normalizes the Zipf so that the sum is equal to one

            Returns:
                the normalized Zipf
        """
        self.check_empty()
        total = sum(list(self.values()))
        if total != 1:
            return self/total
        return Zipf(self)

    def cut(self, _min=0, _max=1):
        """Returns a Zipf without elements below _min or above _max"""
        result = Zipf()
        for k, v in self.items():
            if v > _min and v <= _max:
                result[k] = v
        return result

    def round(self):
        return Zipf({k: round(v, 14) for k, v in self.items()})

    def min(self):
        """Returns the value with minimal frequency in the Zipf"""
        self.check_empty()
        return min(self, key=self.get)

    def max(self):
        """Returns the value with maximal frequency in the Zipf"""
        self.check_empty()
        return max(self, key=self.get)

    def mean(self):
        """Determines the mean frequency"""
        self.check_empty()
        return round(mean(list(self.values())), 14)

    def median(self):
        """Determines the median frequency"""
        self.check_empty()
        return round(median(list(self.values())), 14)

    def var(self):
        """Calculates the variance in the frequencies"""
        self.check_empty()
        return round(var(list(self.values())), 14)

    def is_empty(self):
        return len(self) == 0

    def check_empty(self):
        if self.is_empty():
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
        """Returns the sorted Zipf, based on the frequency value"""
        return Zipf(sorted(
            self.items(),
            key=Zipf._keysort,
            reverse=True
        ))

    def items(self):
        if self.is_unrendered():
            return OrderedDict.items(self.render())
        return OrderedDict.items(self)

    def load(path):
        """Loads a Zipf from the given path.

        Args:
            path: The path where the Zipf is stored.

        Returns:
            The loaded Zipf
        """
        with open(path, "r") as f:
            return Zipf(json.load(f))

    def save(self, path):
        """Saves the Zipf as a dictionary to a given json file

        Args:
            path: the path to the json file to write

        """
        with open(path, "w") as f:
            json.dump(self, f)
