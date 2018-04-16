from multiprocessing import Manager, Process
from ...mp.managers import MyManager
from ...file.loader import loader
from .statistic_from_dir import statistic_from_dir as statistic
from .cli_from_dir import cli_from_dir as cli

import queue

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
        self._loader = loader(path, extensions, self._statistic)

        self._file_interface = lambda file: file
        self._word_filter = lambda word: True
        self._words_regex = re.compile(r"\W+")

        if self._use_cli:
            self._cli = cli(self._statistic)

        self._files = self._loader.get_queue()
        self._zipfs = Manager().list()

    def _text_to_zipf(self, identifier):
        self._statistic.set_live_process("text_to_zipf")
        trie = {}
        n = 0
        while True:
            try:
                if self._statistic.is_loader_done():
                    timeout = 0.1
                else:
                    timeout = 10
                file = self._file_interface(self._files.get(timeout=timeout))
                if file=="":
                    continue
                words = list(filter(self._word_filter, re.split(self._words_regex, file)))
                if len(words)==0:
                    continue
                unit = 1/len(words)
                for word in words:
                    if word in trie:
                        trie[word] = trie[word] + unit
                    else:
                        trie[word] = unit
                n+=1

                self._statistic.add_zipf()
            except queue.Empty:
                break
            except Exception as e:
                with open("test/%s-%s.txt"%(identifier,n), "w") as f:
                    f.write(traceback.format_exc())

        self._zipfs.append((n, trie))
        self._statistic.set_dead_process("text_to_zipf")

    def _merge(self):
        self._statistic.set_live_process("trie_merger")
        n1, t1 = self._zipfs.pop()
        n2, t2 = self._zipfs.pop()

        for k, v in t1.items():
            if k in t2:
                t2[k] = v + t2[k]
            else:
                t2[k] = v

        self._zipfs.append((n1+n2, t2))
        self._statistic.set_dead_process("trie_merger")

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
        self._loader.run()
        self._statistic.set_phase("Converting files to zipfs")
        processes = []
        for i in range(8):
            p = Process(target=self._text_to_zipf, args=(i,), name="Zipf generator n. %s"%i)
            p.start()
            processes.append(p)
        for p in processes:
            p.join()

        self._loader.join()

        self._statistic.set_phase("Merging zipfs")
        processes = []
        while int(len(self._zipfs)/2)>2:
            processes = []
            for i in range(int(len(self._zipfs)/2)):
                p = Process(target=self._merge, name="Trie merger n. %s"%i)
                p.start()
                processes.append(p)
            for p in processes:
                p.join()

        self._statistic.set_phase("Merging last 2 trie")

        # final trie merger
        self._merge()

        self._statistic.set_phase("Converting trie to dict")

        n, t = self._zipfs.pop()
        result = {}

        for k, v in t.items():
            result[k] = v/n

        if self._output!=None:
            self._statistic.set_phase("Saving file")
            with open(self._output, "w") as f:
                json.dump(result, f)

        self._statistic.done()

        if self._use_cli:
            self._cli.join()

        return result