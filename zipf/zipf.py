from __future__ import division
from typing import Union
from collections import OrderedDict
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot
import json
from numpy import mean, median, var
from .utils import is_number

class zipf(OrderedDict):
    """The zipf class represents a zipf distribution and offers various tools to edit it easily"""

    def __str__(self) -> str:
        """Prints a json dictionary representing the zipf"""
        return json.dumps(self, indent=2)

    __repr__ = __str__

    def __missing__(self, key):
        """The default value of an event in the zipf is 0"""
        OrderedDict.__setitem__(self, key, 0)
        return 0

    def __getitem__(self, key):
        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __setitem__(self, key: Union[str, float, int], frequency:float):
        """Sets an element of the zipf to the given frequency

        Args:
            key: an hash representing an element in the zipf
            frequency: a float number representing the frequency

        """

        if is_number(frequency):
            return OrderedDict.__setitem__(self, key, frequency)
        else:
            raise ValueError("A frequency must be a number.")

    def __mul__(self, value: Union['zipf', float, int]) -> 'zipf':
        """Multiplies each value of the zipf by either a numeric value or the corrisponding word frequency in the other zipf.

            Args:
                value: either a zipf or a number to be multiplies with the zipf.

            Returns:
                The multiplied zipf

        """
        if is_number(value):
            return zipf({k: v*value for k, v in self.items()})
        elif isinstance(value, zipf):
            oget = value.get
            result = zipf()
            for k,v in self.items():
                other_value = oget(k)
                if other_value:
                    result[k] = other_value*v
            return result
        else:
            raise ValueError("Moltiplication is allowed only with numbers or zipf objects.")

    __rmul__ = __mul__

    def __truediv__(self, value: Union['zipf', float, int]) -> 'zipf':
        """Divides each value of the zipf by either a numeric value or the corrisponding word frequency in the other zipf.

            Args:
                value: either a zipf or a number to divide the zipf.

            Returns:
                The divided zipf

        """
        if is_number(value):
            if value==0:
                raise ValueError("Division by zero.")
            return zipf({k: v/value for k, v in self.items()})
        elif isinstance(value, zipf):
            oget = value.get
            result = zipf()
            for k,v in self.items():
                other_value = oget(k)
                if other_value:
                    result[k] = v/other_value
            return result
        else:
            raise ValueError("Division is allowed only with numbers or zipf objects.")

    def __neg__(self):
        return zipf({k:-v for k,v in self.items()})

    def __add__(self, other: 'zipf') -> 'zipf':
        """Sums two zipf
            Args:
                other: a given zipf to be summed

            Returns:
                The summed zipfs

        """
        if isinstance(other, zipf):
            result = zipf()
            for k,v in self.items():
                result[k] = v
            for k,v in other.items():
                if result[k] == -v:
                    result.pop(k, None)
                else:
                    result[k] += v
            return result
        raise ValueError("Given argument is not a zipf object")

    def __sub__(self, other: 'zipf') -> 'zipf':
        """Subtracts two zipf
            Args:
                other: a given zipf to be subtracted

            Returns:
                The subtracted zipfs

        """
        if isinstance(other, zipf):
            result = zipf()
            for k,v in self.items():
                result[k] = v
            for k,v in other.items():
                if result[k] == v:
                    result.pop(k, None)
                else:
                    result[k] -= v
            return result
        raise ValueError("Given argument is not a zipf object")

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
        self.check_empty()
        total = sum(list(self.values()))
        if total!=1:
            return self/total
        return zipf(self)

    def cut(self, _min=0, _max=1)->'zipf':
        """Returns a zipf without elements below _min or above _max"""
        result = zipf()
        for k,v in self.items():
            if v > _min and v <= _max:
                result[k] = v
        return result

    def min(self) -> float:
        """Returns the value with minimal frequency in the zipf"""
        self.check_empty()
        return min(self, key=self.get)

    def max(self) -> float:
        """Returns the value with maximal frequency in the zipf"""
        self.check_empty()
        return max(self, key=self.get)

    def mean(self)->float:
        """Determines the mean frequency"""
        self.check_empty()
        return round(mean(list(self.values())),14)

    def median(self)->float:
        """Determines the median frequency"""
        self.check_empty()
        return round(median(list(self.values())),14)

    def var(self)->float:
        """Calculates the variance in the frequencies"""
        self.check_empty()
        return round(var(list(self.values())),14)

    def check_empty(self):
        if len(self) == 0:
            raise ValueError("The zipf is empty!")

    def sort(self)->'zipf':
        """Returns the sorted zipf, based on the frequency value"""
        return zipf(sorted(self.items(), key=lambda t: t[1], reverse=True))

    def load(path: str) -> 'zipf':
        """Loads a zipf from the given path.

        Args:
            path: The path where the zipf is stored.

        Returns:
            The loaded zipf
        """
        with open(path, "r") as f:
            return zipf(json.load(f))

    def save(self, path: str):
        """Saves the zipf as a dictionary to a given json file

        Args:
            path: the path to the json file to write

        """
        with open(path, "w") as f:
            json.dump(self, f)

    def plot(self,  plot_style = 'o', show = True):
        """Plots the zipf"""
        y = [t[1] for t in self.items()]

        matplotlib.pyplot.figure(figsize=(20,10))
        matplotlib.pyplot.plot(range(len(self)), y, plot_style, markersize=1)
        if show:
            matplotlib.pyplot.show()

    def plot_remap(self, remapper, plot_style = 'o', show = True):
        """Plots a zipf remapped over another zipf"""
        x1 = []
        y1 = []
        y2 = []
        sget = self.get
        rget = remapper.get
        x1append = x1.append
        y1append = y1.append
        y2append = y2.append
        i = 0
        for key, value in remapper.items():
            v = sget(key)
            if v:
                x1append(i)
                y1append(v)
            y2append(value)
            i+=1

        matplotlib.pyplot.figure(figsize=(20,10))
        matplotlib.pyplot.plot(range(len(remapper)), y2, '-', markersize=1)
        matplotlib.pyplot.plot(x1, y1, plot_style, markersize=3)
        if show:
            matplotlib.pyplot.show()

