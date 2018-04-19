from collections import OrderedDict

import os
import json
import re

class from_file:
    def __init__(self):
        self._file_interface = lambda file: file
        self._word_filter = lambda word: True
        self._words_regex = re.compile(r"\W+")

    def set_interface(self, file_interface):
        if file_interface!=None:
            self._file_interface = file_interface

    def set_word_filter(self, word_filter):
        if word_filter!= None:
            self._word_filter = word_filter

    def run(self, path, output=None):
        if not os.path.isfile(path):
            raise ValueError("Given file %s does not exists"%path)

        with open(path, "r") as f:
            if path.endswith(".json"):
                obj = json.load(f)
            else:
                obj = f.read()

        file = self._file_interface(obj)

        if file=="":
            raise ValueError("Empty file")

        words = list(filter(self._word_filter, re.split(self._words_regex, file)))

        if len(words)==0:
            raise ValueError("Empty word list")

        unit = 1/len(words)

        zipf = {}

        for word in words:
            if word in zipf:
                zipf[word] = zipf[word] + unit
            else:
                zipf[word] = unit

        sorted_zipf = OrderedDict(sorted(zipf.items(), key=lambda t: t[1], reverse=True))

        if output!=None:
            self._statistic.set_phase("Saving file")
            with open(output, "w") as f:
                json.dump(sorted_zipf, f)

        return sorted_zipf