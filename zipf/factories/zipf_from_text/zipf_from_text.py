from ...zipf import Zipf
from ...factories import ZipfFromList
from re import compile, split


class ZipfFromText(ZipfFromList):
    def __init__(self, options=None):
        super().__init__(options)
        self._words_regex = compile(r"\W+")

    def _extract_words(self, text):
        """Extract a zipf distribution from the given text"""
        for word in split(self._words_regex, text):
            if word:
                yield word

    def run(self, text):
        return super().run(self._extract_words(text))
