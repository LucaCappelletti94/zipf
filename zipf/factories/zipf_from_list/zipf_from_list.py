from ...zipf import Zipf
from ..zipf_factory import ZipfFactory


class ZipfFromList(ZipfFactory):
    def __init__(self, options=None):
        super().__init__(options)

    def _create_zipf(self, elements, zipf):
        filtered_elements = self._filter(elements)
        clean_elements = self._clean(filtered_elements)

        elements_number = len(clean_elements)

        if elements_number == 0:
            return zipf

        unit = 1/elements_number

        zget = zipf.get
        zset = zipf.__setitem__

        [zset(element, zget(element, 0) + unit) for element in clean_elements]

        return zipf

    def run(self, elements):
        """Extract a zipf distribution from the given text"""
        return super().run(self._create_zipf(elements, Zipf()))

    def enrich(self, elements, zipf):
        return self._create_zipf(elements, zipf)
