from ...zipf import zipf
from ..zipf_factory import zipf_factory

class zipf_from_list(zipf_factory):
    def __init__(self, custom_options = None):
        super().__init__(custom_options)

    def _create_zipf(self, elements, _zipf):

        filtered_elements = self._filter(elements)
        clean_elements = self._clean(filtered_elements)

        elements_number = len(clean_elements)

        if elements_number==0:
            return _zipf

        unit = 1/elements_number

        zd = _zipf._data

        get = zd.get

        for element in clean_elements:
            zd[element] = get(element, 0) + unit

        return _zipf

    def run(self, elements):
        """Extract a zipf distribution from the given text"""
        return super().run(self._create_zipf(elements, zipf()))

    def enrich(self, elements, _zipf):
        return self._create_zipf(elements, _zipf)