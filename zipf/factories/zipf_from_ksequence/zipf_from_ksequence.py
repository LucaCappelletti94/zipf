from ...zipf import Zipf
from ...factories import ZipfFromList
import re


class ZipfFromKSequence(ZipfFromList):
    def __init__(self, k, options=None):
        super().__init__(options)
        if k <= 0:
            raise ValueError("The attribute k cannot be less than zero!")
        self.k = k

    def _split_sequences(self, sequence):
        """Extract a zipf distribution from the given text"""
        return (sequence[i:i+self.k] for i in range(0, len(sequence), self.k))

    def run(self, sequence):
        return super().run(self._split_sequences(sequence))
