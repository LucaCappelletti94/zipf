from ...zipf import zipf
from ..zipf_factory import zipf_factory

class zipf_from_list(zipf_factory):
    def __init__(self):
        super().__init__()

    def _create_zipf(self, elements, _zipf):
        elements_number = len(elements)

        if elements_number==0:
            raise ValueError("Empty word list")

        unit = 1/elements_number

        for element in elements:
            _zipf[element] = _zipf[element] + unit

        return _zipf

    def run(self, elements):
        """Extract a zipf distribution from the given text"""
        return super().run(self._create_zipf(elements, zipf()))

    def enrich(self, elements, _zipf):
        return self._create_zipf(elements, _zipf)