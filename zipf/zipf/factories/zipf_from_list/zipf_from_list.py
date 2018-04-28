from ...zipf import zipf
from ..zipf_factory import zipf_factory

class zipf_from_list(zipf_factory):
    def __init__(self):
        super().__init__()
        self._word_filter = None

    def set_word_filter(self, word_filter):
        """Sets the function that filters words"""
        self._word_filter = word_filter

    def _create_zipf(self, elements, _zipf):

        if self._word_filter:
            elements = list(filter(self._word_filter, elements))

        elements_number = len(elements)

        if elements_number==0:
            return _zipf

        unit = 1/elements_number

        zd = _zipf._data

        get = zd.get

        for element in elements:
            zd[element] = get(element, 0) + unit

        return _zipf

    def run(self, elements):
        """Extract a zipf distribution from the given text"""
        return super().run(self._create_zipf(elements, zipf()))

    def enrich(self, elements, _zipf):
        return self._create_zipf(elements, _zipf)