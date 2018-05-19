from ...zipf import Zipf
from ...factories import ZipfFromList
from re import compile, split


class ZipfFromText(ZipfFromList):
    def __init__(self, options=None):
        super().__init__(options)
        self._words_regex = compile(r"\W+")

    def _extract_words(self, text):
        """Extract a zipf distribution from the given text"""
        return list(filter(None, split(self._words_regex, text)))

    def run(self, text):
        return super().run(self._extract_words(text))

    def enrich(self, text, zipf):
        return super().enrich(self._extract_words(text), zipf)
