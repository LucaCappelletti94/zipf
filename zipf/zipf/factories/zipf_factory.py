class zipf_factory:
    def __init__(self):
        self._word_filter = lambda word: True

    def set_word_filter(self, word_filter):
        """Sets the function that filters words"""
        self._word_filter = word_filter

    def run(self, _zipf):
        return _zipf.sort().normalize()