from __future__ import division
from typing import Union
from multiprocessing import Pool, cpu_count
from collections import OrderedDict
import math, numbers
import matplotlib.pyplot as plt
import json
import numpy as np

class zipf:
    """The zipf class represents a zipf distribution and offers various tools to edit it easily"""

    def __init__(self, data={}):
        """Creates a zipf from the given dictionary

        Args:
            data: The dictionary with the zipf information.

        """
        self._data = OrderedDict(data)

    def load(path: str) -> 'zipf':
        """Loads a zipf from the given path.

        Args:
            path: The path where the zipf is stored.

        Returns:
            The loaded zipf
        """
        with open(path, "r") as f:
            return zipf(json.load(f))

    def save(self, path):
        """Saves the zipf as a dictionary to a given json file

        Args:
            path: the path to the json file to write

        """
        with open(path, "w") as f:
            json.load(self._data, f)

    def __str__(self) -> str:
        """Prints a json dictionary representing the zipf"""
        return json.dumps(self._data, indent=2)

    def __len__(self) -> int:
        """Returns the zipf lenght"""
        return len(self._data)

    def __contains__(self, key: Union[str, numbers.Number]) -> bool:
        """Returns whetever if the zipf contains a given word (or element)

        Args:
            key: the element that has to be found

        """
        return key in self._data

    def __iter__(self):
        """Iterates over the zipf"""
        return iter(self._data)

    def __getitem__(self, key: Union[str, numbers.Number]) -> float:
        """Retrieve an element from the zipf

        Args:
            key: a slice or an hash representing an element in the zipf

        """
        if isinstance(key, slice):
            return zipf(list(self.items())[key])
        return self._data.get(key, 0)

    def __setitem__(self, key: Union[str, numbers.Number], frequency:float):
        """Sets an element of the zipf to the given frequency

        Args:
            key: an hash representing an element in the zipf
            frequency: a float number representing the frequency

        """
        if isinstance(frequency, numbers.Number):
            self._data[key] = frequency
        else:
            raise ValueError("A frequency must be a number.")

    def __mul__(self, value: Union['zipf', numbers.Number]) -> 'zipf':
        """Multiplies each value of the zipf by either a numeric value or the corrisponding word frequency in the other zipf.

            Args:
                value: either a zipf or a number to be multiplies with the zipf.

            Returns:
                The multiplied zipf

        """
        if isinstance(value, numbers.Number):
            return zipf({k: self[k]*value for k in self})
        elif isinstance(value, zipf):
            return zipf({ k: self.get(k)*value.get(k) for k in set(self) | set(value) })
        else:
            raise ValueError("Moltiplication is allowed only with numbers or zipf objects.")

    def __truediv__(self, value: numbers.Number) -> 'zipf':
        """Divides each value of the zipf by either a numeric value or the corrisponding word frequency in the other zipf.

            Args:
                value: either a zipf or a number to divide the zipf.

            Returns:
                The divided zipf

        """
        if isinstance(value, numbers.Number):
            if value==0:
                raise ValueError("Division by zero.")
            return zipf({k: self[k]/value for k in self})
        elif isinstance(value, zipf):
            return zipf({ k: self[k]/value[k] for k in set(self) & set(value) })
        else:
            raise ValueError("Division is allowed only with numbers or zipf objects.")

    __rmul__ = __mul__
    __repr__ = __str__

    def __add__(self, other: 'zipf') -> 'zipf':
        """Sums two zipf
            Args:
                other: a given zipf to be summed

            Returns:
                The summed zipfs

        """
        if isinstance(other, zipf):
            return zipf({ k: self[k] + other[k] for k in set(self) | set(other) })
        raise ValueError("Given argument is not a zipf object")

    def __sub__(self, other: 'zipf') -> 'zipf':
        """Subtracts two zipf
            Args:
                other: a given zipf to be subtracted

            Returns:
                The subtracted zipfs

        """
        if isinstance(other, zipf):
            return zipf({ k: self[k] - other[k] for k in set(self) | set(other) })
        raise ValueError("Given argument is not a zipf object")

    def KL(self, other: 'zipf') -> float:
        """Determines the Kullback–Leibler divergence on the subset of both zipfs events, in log2.

            Args:
                other: the zipf to which determine the KL divergence.

            Returns:
                A float number representing the KL divergence
        """
        total = 0
        for key in set(self.keys()) & set(other.keys()):
            v = self[key]
            total += v*math.log(v/other[key],2)
        return total

    def _emiJSD(self, other: 'zipf') -> float:
        total = 0
        other_data = other._data
        for key, value in self._data.items():
            ov = other.get(key)
            if ov:
                total += value*math.log(2*value/(ov + value), 2)
            else:
                total += value
        return total

    def JSD(self, other: 'zipf') -> float:
        """Determines the Jensen–Shannon divergence on both zipfs events, in log2.

            Args:
                other: the zipf to which determine the JS divergence.

            Returns:
                A float number representing the JS divergence
        """
        return (self._emiJSD(other) + other._emiJSD(self))/2

    def items(self):
        """Retrieves the zipf items"""
        return self._data.items()

    def values(self):
        """Retrieves the zipf frequencies values"""
        return self._data.values()

    def keys(self):
        """Retrieves the zipf keys"""
        return self._data.keys()

    def update(self, value:dict):
        """Updates multiple values of the zipfs at once

           Args:
                value: a dictionary containing a map {key:frequency}
        """
        self._data.update(value)

    def min(self) -> float:
        """Returns the value with minimal frequency in the zipf"""
        return min(self, key=self.get)

    def max(self) -> float:
        """Returns the value with maximal frequency in the zipf"""
        return max(self, key=self.get)

    def plot(self):
        """Plots the zipf"""
        y = [t[1] for t in self.items()]

        plt.figure(figsize=(20,10))
        plt.plot(range(len(self)), y, 'o', markersize=1)
        plt.show()

    def remap(self, remapper:'zipf')->'zipf':
        """Returns a remapped zipf to the order of the other zipf, deleting elements when not present in both.

            Args:
                remapper: a zipf that is used to remap the current zipf

            Returns:
                the remapped zipf

        """
        remapped = zipf()
        for key, value in remapper.items():
            if key in self:
                remapped[key] = self[key]
        return remapped

    def normalize(self)->'zipf':
        """Normalizes the zipf so that the sum is equal to one

            Returns:
                the normalized zipf
        """
        if sum(list(self.values()))!=1:
            return self/sum(list(self.values()))
        return zipf(self._data)

    def mean(self)->float:
        """Determines the mean frequency"""
        return np.mean(list(self.values()))

    def median(self)->float:
        """Determines the median frequency"""
        return np.median(list(self.values()))

    def var(self)->float:
        """Calculates the variance in the frequencies"""
        return np.var(list(self.values()))

    def sort(self)->'zipf':
        """Returns the sorted zipf, based on the frequency value"""
        return zipf(sorted(self.items(), key=lambda t: t[1], reverse=True))

    def cut(self, _min=0, _max=1)->'zipf':
        """Returns a zipf without elements below _min or above _max"""
        cut_zipf = zipf()
        for k,v in self.items():
            if v > _min and v <= _max:
                cut_zipf[k] = v
        return cut_zipf

    def plot_remapped(self, remapper):
        """Plots a zipf remapped over another zipf"""
        x1 = []
        y1 = []
        y2 = []
        for i, key in enumerate(remapper):
            if key in self:
                x1.append(i)
                y1.append(self[key])
            y2.append(remapper[key])

        plt.figure(figsize=(20,10))
        plt.plot(range(len(remapper)), y2, '-', markersize=1)
        plt.plot(x1, y1, 'o', markersize=3)
        plt.show()