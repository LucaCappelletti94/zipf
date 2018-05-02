from ...zipf import zipf
from ...factories import zipf_from_list
import re

class zipf_from_text(zipf_from_list):
    def __init__(self, custom_options = None):
        super().__init__(custom_options)
        self._words_regex = re.compile(r"\W+")

    def _extract_words(self, text):
        """Extract a zipf distribution from the given text"""
        return list(filter(None, re.split(self._words_regex, text)))

    def run(self, text):
        return super().run(self._extract_words(text))

    def enrich(self, text, _zipf):
        return super().enrich(self._extract_words(text), _zipf)
