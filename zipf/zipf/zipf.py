from __future__ import division
from typing import Union
from multiprocessing import Pool, cpu_count
from collections import OrderedDict
import math, numbers
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import json
import numpy as np

class zipf:
    """The zipf class represents a zipf distribution and offers various tools to edit it easily"""

    def __init__(self, data=None):
        """Creates a zipf from the given dictionary

        Args:
            data: The dictionary with the zipf information.

        """
        if data:
            self._data = OrderedDict(data)
        else:
            self._data = OrderedDict({})

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
            json.dump(self._data, f)

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

    def __getitem__(self, key: Union[str, numbers.Number, slice]) -> float:
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

        if self.is_number(frequency):
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
        sd = self._data
        if self.is_number(value):
            return zipf({k: sd[k]*value for k in sd})
        elif isinstance(value, zipf):
            od = value._data
            sget = sd.get
            oget = od.get
            return zipf({ k: sget(k)*oget(k) for k in set(sd) | set(od) })
        else:
            raise ValueError("Moltiplication is allowed only with numbers or zipf objects.")

    def __truediv__(self, value: numbers.Number) -> 'zipf':
        """Divides each value of the zipf by either a numeric value or the corrisponding word frequency in the other zipf.

            Args:
                value: either a zipf or a number to divide the zipf.

            Returns:
                The divided zipf

        """
        sd = self._data
        if self.is_number(value):
            if value==0:
                raise ValueError("Division by zero.")
            return zipf({k: sd[k]/value for k in sd})
        elif isinstance(value, zipf):
            od = value._data
            return zipf({ k: sd[k]/od[k] for k in set(sd) & set(od) })
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
            sd = self._data
            od = other._data
            return zipf({ k: sd[k] + od[k] for k in set(self) | set(other) })
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

    def is_number(self, value):
        return isinstance(value, (int, float))

    def jensen_shannon(self, other):
        """
            Determines the Jensen–Shannon divergence on both zipfs events.

            Both zipfs HAVE TO be normalized.

            Args:
                other: the zipf to which determine the JS divergence.

            Returns:
                A float number representing the JS divergence
        """
        total = 0
        delta = 0
        if len(self) > len(other):
            big_data = self._data
            small_data = other._data
        else:
            big_data = other._data
            small_data = self._data

        big_get = big_data.get
        log = math.log

        for key, value in small_data.items():
            ov = big_get(key)
            if ov:
                denominator = (ov + value)/2
                total += value*log(value/denominator) + ov*log(ov/denominator)
                delta -= ov
            else:
                delta += value

        total += (1+delta)*log(2)
        return total/2

    def kullback_leibler(self, other: 'zipf') -> float:
        """Determines the Kullback–Leibler divergence on the subset of both zipfs events.

            Args:
                other: the zipf to which determine the KL divergence.

            Returns:
                A float number representing the KL divergence
        """
        total = 0
        sd = self._data
        od = other._data
        for key in set(self.keys()) & set(other.keys()):
            v = sd[key]
            total += v*math.log(v/od[key])
        return total

    def hellinger(self, other: 'zipf') -> float:
        """Determines the hellinger distance on the subset of both zipfs events.

            Args:
                other: the zipf to which determine the hellinger distance.

            Returns:
                A float number representing the hellinger distance
        """
        total = 0
        sd = self._data
        od = other._data
        for key in set(self.keys()) & set(other.keys()):
            total += (math.sqrt(sd[key])-math.sqrt(od[key]))**2
        return math.sqrt(total)/math.sqrt(2)

    def total_variation(self, other: 'zipf') -> float:
        """Determines the Total Variation distance on the zipfs.

            Args:
                other: the zipf to which determine the TV distance.

            Returns:
                A float number representing the TV distance
        """
        total = 0
        sd = self._data
        od = other._data
        for key in set(self.keys()) | set(other.keys()):
            total += abs(sd.get(key,0) - od.get(key,0))
        return total

    def _bhattacharyya_coefficient(self, other: 'zipf') -> float:
        """Determines the bhattacharyya coefficient of the zipfs.

            Args:
                other: the zipf to which determine the bhattacharyya coefficient .

            Returns:
                A float number representing the bhattacharyya coefficient
        """
        total = 0
        sd = self._data
        od = other._data
        for key in set(self.keys()) & set(other.keys()):
            total += math.sqrt(sd[key]*od[key])
        return total

    def bhattacharyya(self, other: 'zipf') -> float:
        """Determines the bhattacharyya distance of the zipfs.

            Args:
                other: the zipf to which determine the bhattacharyya distance .

            Returns:
                A float number representing the bhattacharyya distance
        """
        return -math.log(self._bhattacharyya_coefficient(other))

    def mahalanobis(self, other: 'zipf') -> float:
        """Determines the mahalanobis distance of the zipfs.

            Args:
                other: the zipf to which determine the mahalanobis distance .

            Returns:
                A float number representing the mahalanobis distance
        """
        total = 0
        sd = self._data
        od = other._data
        for key in set(self.keys()) | set(other.keys()):
            total += (sd.get(key,0) - od.get(key,0))**2
        return math.sqrt(total)

    def items(self):
        """Retrieves the zipf items"""
        return self._data.items()

    def get(self, k):
        """Retrieves the zipf items"""
        return self._data.get(k, 0)

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
        cd = cut_zipf._data
        for k,v in self.items():
            if v > _min and v <= _max:
                cd[k] = v
        return cut_zipf

    def plot(self,  plot_style = 'o'):
        """Plots the zipf"""
        y = [t[1] for t in self.items()]

        plt.figure(figsize=(20,10))
        plt.plot(range(len(self)), y, plot_style, markersize=1)
        plt.show()

    def plot_remapped(self, remapper, plot_style = 'o'):
        """Plots a zipf remapped over another zipf"""
        x1 = []
        y1 = []
        y2 = []
        for i, key in enumerate(remapper):
            if key in self:
                x1.append(i)
                y1.append(self._data[key])
            y2.append(remapper._data[key])

        plt.figure(figsize=(20,10))
        plt.plot(range(len(remapper)), y2, '-', markersize=1)
        plt.plot(x1, y1, plot_style, markersize=3)
        plt.show()