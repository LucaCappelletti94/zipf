from .factories.from_dir.from_dir import from_dir
from multiprocessing import Pool, cpu_count
from collections import OrderedDict
import math, numbers
import matplotlib.pyplot as plt
import json

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
        factory = from_dir(path, output_file, use_cli)
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
        return str(dict(self._data))

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return zipf(list(self.items())[key])
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

    __rmul__ = __mul__

    def __add__(self, other):
        return zipf({ k: self.get(k) + other.get(k) for k in set(self) | set(other) })

    def KL(self, other):
        """Kullback–Leibler divergence defined for subset"""
        """https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence"""
        total = 0
        for key in set(self.keys()) & set(other.keys()):
            v = self[key]
            total += v*math.log(v/other[key])
        return total

    def _emiJSD(one, two):
        total = 0
        for key, value in one.items():
            total += value*math.log(2*value/(two.get(key) + value))
        return total/2

    def JSD(self, other):
        """Jensen–Shannon divergence"""
        """https://en.wikipedia.org/wiki/Jensen%E2%80%93Shannon_divergence"""
        # with Pool(2) as p:
        #     return sum(list(p.starmap(zipf._emiJSD, [(self, other), (other, self)])))
        return zipf._emiJSD(self, other) + zipf._emiJSD(other, self)

    def merge(self, other):
        return { k: (self.get(k) + other.get(k))*0.5 for k in set(self) | set(other) }

    def get(self, key, default=0):
        return self._data.get(key, default)

    def items(self):
        return self._data.items()

    def keys(self):
        return self._data.keys()

    def update(self, value):
        return self._data.update(value)

    def plot(self):
        y = [t[1] for t in self.items()]

        plt.figure(figsize=(20,10))
        plt.plot(range(len(self)), y, 'o', markersize=1)
        plt.show()