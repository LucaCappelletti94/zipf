from __future__ import division
from typing import Union
from collections import OrderedDict
import json
from numpy import mean, median, var
from .utils import is_number


class Zipf(OrderedDict):
    """Zipf represents a Zipf distribution offering tools to edit it easily"""

    def __str__(self) -> str:
        """Prints a json dictionary representing the Zipf"""
        return json.dumps(self, indent=2)

    __repr__ = __str__

    def __missing__(self, key):
        """The default value of an event in the Zipf is 0"""
        return 0

    def __getitem__(self, key):
        return OrderedDict.__getitem__(self, key)

    def __setitem__(self, key: Union[str, float, int], frequency: float):
        """Sets an element of the Zipf to the given frequency

        Args:
            key: an hash representing an element in the Zipf
            frequency: a float number representing the frequency

        """

        if is_number(frequency):
            return OrderedDict.__setitem__(self, key, frequency)

        raise ValueError("A frequency must be a number.")

    def __mul__(self, value: Union['Zipf', float, int]) -> 'Zipf':
        """Multiplies the Zipf by a number or the frequency in another Zipf.

            Args:
                value: a Zipf or a number to be multiplies with the Zipf.

            Returns:
                The multiplied Zipf

        """
        if is_number(value):
            return Zipf({k: v*value for k, v in self.items()})

        if not isinstance(value, Zipf):
            raise ValueError(
                "Moltiplication is allowed only with numbers or Zipf objects.")

        oget = value.get
        result = Zipf()
        for k, v in self.items():
            other_value = oget(k)
            if other_value:
                result[k] = other_value*v
        return result

    __rmul__ = __mul__

    def __truediv__(self, value: Union['Zipf', float, int]) -> 'Zipf':
        """Divides the Zipf by a number or the frequency in another Zipf.

            Args:
                value: either a Zipf or a number to divide the Zipf.

            Returns:
                The divided Zipf

        """
        if value == 0:
            raise ValueError("Division by zero.")

        if is_number(value):
            return Zipf({k: v/value for k, v in self.items()})

        if not isinstance(value, Zipf):
            raise ValueError(
                "Division is allowed only with numbers or Zipf objects.")

        oget = value.get
        result = Zipf()
        for k, v in self.items():
            other_value = oget(k)
            if other_value:
                result[k] = v/other_value
        return result

    def __neg__(self):
        return Zipf({k: -v for k, v in self.items()})

    def __add__(self, other: 'Zipf') -> 'Zipf':
        """Sums two Zipf
            Args:
                other: a given Zipf to be summed

            Returns:
                The summed Zipfs

        """
        if isinstance(other, Zipf):
            result = Zipf()
            for k, v in self.items():
                result[k] = v
            for k, v in other.items():
                if result[k] == -v:
                    result.pop(k, None)
                else:
                    result[k] += v
            return result
        raise ValueError("Given argument is not a Zipf object")

    def __sub__(self, other: 'Zipf') -> 'Zipf':
        """Subtracts two Zipf
            Args:
                other: a given Zipf to be subtracted

            Returns:
                The subtracted Zipfs

        """
        if isinstance(other, Zipf):
            result = Zipf()
            for k, v in self.items():
                result[k] = v
            for k, v in other.items():
                if result[k] == v:
                    result.pop(k, None)
                else:
                    result[k] -= v
            return result
        raise ValueError("Given argument is not a Zipf object")

    def remap(self, remapper: 'Zipf')->'Zipf':
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

    def normalize(self)->'Zipf':
        """Normalizes the Zipf so that the sum is equal to one

            Returns:
                the normalized Zipf
        """
        self.check_empty()
        total = sum(list(self.values()))
        if total != 1:
            return self/total
        return Zipf(self)

    def cut(self, _min=0, _max=1)->'Zipf':
        """Returns a Zipf without elements below _min or above _max"""
        result = Zipf()
        for k, v in self.items():
            if v > _min and v <= _max:
                result[k] = v
        return result

    def round(self):
        return Zipf({k: round(v, 14) for k, v in self.items()})

    def min(self) -> float:
        """Returns the value with minimal frequency in the Zipf"""
        self.check_empty()
        return min(self, key=self.get)

    def max(self) -> float:
        """Returns the value with maximal frequency in the Zipf"""
        self.check_empty()
        return max(self, key=self.get)

    def mean(self)->float:
        """Determines the mean frequency"""
        self.check_empty()
        return round(mean(list(self.values())), 14)

    def median(self)->float:
        """Determines the median frequency"""
        self.check_empty()
        return round(median(list(self.values())), 14)

    def var(self)->float:
        """Calculates the variance in the frequencies"""
        self.check_empty()
        return round(var(list(self.values())), 14)

    def is_empty(self):
        return len(self) == 0

    def check_empty(self):
        if self.is_empty():
            raise ValueError("The Zipf is empty!")

    def sort(self)->'Zipf':
        """Returns the sorted Zipf, based on the frequency value"""
        return Zipf(sorted(self.items(), key=lambda t: t[1], reverse=True))

    def load(path: str) -> 'Zipf':
        """Loads a Zipf from the given path.

        Args:
            path: The path where the Zipf is stored.

        Returns:
            The loaded Zipf
        """
        with open(path, "r") as f:
            return Zipf(json.load(f))

    def save(self, path: str):
        """Saves the Zipf as a dictionary to a given json file

        Args:
            path: the path to the json file to write

        """
        with open(path, "w") as f:
            json.dump(self, f)
