"""ZipfFromText create a Zipf from a given text."""
from re import compile, split

from ...factories import ZipfFromList


class ZipfFromText(ZipfFromList):
    """ZipfFromText create a Zipf from a given text."""

    def __init__(self, options=None):
        """Create a ZipfFromText with give options."""
        super().__init__(options)
        self._words_regex = compile(r"\W+")

    def _extract_words(self, text):
        """Extract a zipf distribution from the given text."""
        return (word for word in split(self._words_regex, text) if word)

    def run(self, text):
        """Return Zipf created from given text."""
        return super().run(self._extract_words(text))
