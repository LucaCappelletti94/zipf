from .factories.from_dir.from_dir import from_dir
from .factories.from_file.from_file import from_file
from multiprocessing import Pool, cpu_count
from collections import OrderedDict
import math, numbers
import matplotlib.pyplot as plt
import json
import numpy as np

class zipf:
    def __init__(self, data={}):
        self._data = OrderedDict(data)

    def from_dir(path, file_interface=None, word_filter=None, output_file=None, use_cli=False):
        factory = from_dir(path, output_file, use_cli)
        factory.set_interface(file_interface)
        factory.set_word_filter(word_filter)
        data = factory.run()
        return zipf(data)

    def from_file(path, file_interface=None, word_filter=None, output_file=None):
        factory = from_file(path, output_file)
        factory.set_interface(file_interface)
        factory.set_word_filter(word_filter)
        data = factory.run()
        return zipf(data)

    def load(path):
        """Loads the zipf from a file where it was first stored"""
        with open(path, "r") as f:
            return zipf(json.load(f))

    def save(self, path):
        """Saves the zipf as a dictionary to a given json file"""
        with open(path, "w") as f:
            json.load(self._data, f)

    def __str__(self):
        return json.dumps(self._data, indent=2)

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return zipf(self._data[key])
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __mul__(self, value):
        if isinstance(value, numbers.Number):
            tmp_zipf = zipf()
            tmp_zipf.update((x, y*value) for x, y in self.items())
            return tmp_zipf
        else:
            raise ValueError("Moltiplication is allowed only with int and floats.")

    def __truediv__(self, value):
        if value==0:
            raise ValueError("Division by zero.")
        return self.__mul__(1/value)

    __rmul__ = __mul__
    __repr__ = __str__

    def __add__(self, other):
        return zipf({ k: self.get(k) + other.get(k) for k in set(self) | set(other) })

    def KL(self, other):
        """Kullback–Leibler divergence defined for subset"""
        """https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence"""
        total = 0
        for key in set(self.keys()) & set(other.keys()):
            v = self[key]
            total += v*math.log(v/other[key],2)
        return total

    def _emiJSD(self, other):
        total = 0
        for key, value in self._data.items():
            ov = other.get(key)
            if ov:
                total += value*math.log(2*value/(ov + value), 2)
            else:
                total += value
        return total

    def JSD(self, other):
        """Jensen–Shannon divergence"""
        """https://en.wikipedia.org/wiki/Jensen%E2%80%93Shannon_divergence"""
        return (self._emiJSD(other._data) + other._emiJSD(self._data))/2

    def get(self, key, default=0):
        return self._data.get(key, default)

    def items(self):
        return self._data.items()

    def values(self):
        return self._data.values()

    def keys(self):
        return self._data.keys()

    def update(self, value):
        return self._data.update(value)

    def min(self, value):
        return min(self, key=self.get)

    def max(self, value):
        return max(self, key=self.get)

    def plot(self):
        y = [t[1] for t in self.items()]

        plt.figure(figsize=(20,10))
        plt.plot(range(len(self)), y, 'o', markersize=1)
        plt.show()

    def remap(self, remapper):
        remapped = zipf()
        for key, value in remapper.items():
            if key in self:
                remapped[key] = self[key]
        return remapped

    def renormalize(self):
        return self/sum(list(self.values()))

    def mean(self):
        return np.mean(list(self.values()))

    def var(self):
        return np.var(list(self.values()))

    def cut(self, _min=0, _max=1):
    	cut_zipf = zipf()
    	for k,v in self.items():
    		if v > _min and v <= _max:
    			cut_zipf[k] = v
    	return cut_zipf.renormalize()


    def plot_remapped(self, remapper):
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


