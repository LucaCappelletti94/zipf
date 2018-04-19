from multiprocessing import Manager, Pool, Process, cpu_count
from ...mp.managers import MyManager
from ...utils import chunks
from .statistic_from_dir import statistic_from_dir as statistic
from .cli_from_dir import cli_from_dir as cli
from collections import OrderedDict

import glob
import math
import json
import re

MyManager.register('statistic', statistic)

class from_dir:
    def __init__(self, path, output=None, use_cli=False, extensions = ["json"]):
        self._path = path
        self._output = output
        self._use_cli = use_cli

        self._myManager = MyManager()
        self._myManager.start()

        self._statistic = self._myManager.statistic()
        self._extensions = extensions
        self._processes_number = cpu_count()

        self._file_interface = lambda file: file
        self._word_filter = lambda word: True
        self._words_regex = re.compile(r"\W+")

        self._zipfs = Manager().list()

        if self._use_cli:
            self._cli = cli(self._statistic)

    def _text_to_zipf(self, paths):
        trie = {}
        n = 0
        for path in paths:
            with open(path, "r") as f:
                if path.endswith(".json"):
                    obj = json.load(f)
                else:
                    obj = f.read()
            file = self._file_interface(obj)
            if file=="":
                self._statistic.add_empty_file()
                continue
            words = list(filter(self._word_filter, re.split(self._words_regex, file)))
            if len(words)==0:
                self._statistic.add_empty_wordlist()
                continue
            unit = 1/len(words)
            for word in words:
                if word in trie:
                    trie[word] = trie[word] + unit
                else:
                    trie[word] = unit
            n+=1
            self._statistic.add_zipf()

        self._zipfs.append((n, trie))

    def _merge(zipfs2):
        n1, z1 = zipfs2[0]
        n2, z2 = zipfs2[1]

        for k, v in z1.items():
            if k in z2:
                z2[k] = v + z2[k]
            else:
                z2[k] = v

        return (n1+n2, z2)

    def _load_paths(self):
        files_list = []
        for extension in self._extensions:
            files_list += glob.iglob(self._path+"/**/*.%s"%extension)
        self._statistic.set_total_files(len(files_list))
        return chunks(files_list, math.ceil(len(files_list)/self._processes_number))

    def set_interface(self, file_interface):
        if file_interface!=None:
            self._file_interface = file_interface

    def set_word_filter(self, word_filter):
        if word_filter!= None:
            self._word_filter = word_filter

    def run(self):
        if self._use_cli:
            self._cli.run()

        self._statistic.set_phase("Loading file paths")
        processes = []
        for i, ch in enumerate(self._load_paths()):
            process = Process(target=self._text_to_zipf, args=(ch,))
            process.start()
            processes.append(process)
        self._statistic.set_phase("Converting files to zipfs")
        for p in processes:
            p.join()

        self._statistic.set_phase("Merging zipfs")
        zipfs = self._zipfs
        with Pool(cpu_count()) as p:
            while len(zipfs)>=2:
                zipfs = list(p.imap(from_dir._merge, list(chunks(zipfs, 2))))

        self._statistic.set_phase("Normalizing zipfs")

        n, zipf = zipfs[0]

        for k, v in zipf.items():
            zipf[k] = v/n

        sorted_zipf = OrderedDict(sorted(zipf.items(), key=lambda t: t[1], reverse=True))

        if self._output!=None:
            self._statistic.set_phase("Saving file")
            with open(self._output, "w") as f:
                json.dump(sorted_zipf, f)

        self._statistic.done()

        if self._use_cli:
            self._cli.join()

        return sorted_zipf