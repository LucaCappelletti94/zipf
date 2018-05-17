from ...zipf import Zipf
from ...factories import ZipfFromList
import re


class ZipfFromKSequence(ZipfFromList):
    def __init__(self, k, options=None):
        super().__init__(options)
        if k <= 0:
            raise ValueError("The attribute k cannot be less than zero!")
        self._k = k

    def _split_sequences(self, text):
        """Extract a zipf distribution from the given text"""
        return [text[i:i+self._k] for i in range(0, len(text), self._k)]

    def run(self, text):
        return super().run(self._split_sequences(text))

    def enrich(self, text, zipf):
        return super().enrich(self._split_sequences(text), zipf)
