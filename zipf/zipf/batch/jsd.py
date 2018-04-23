from multiprocessing import Process, cpu_count, Manager, Lock

from ..mp import MyManager
from ..utils import chunks
from ..factories import zipf_from_file
from ..zipf import zipf

from .batch_statistic import batch_statistic as statistic
from .batch_cli import batch_cli as cli

import glob
import math
import json

MyManager.register('statistic', statistic)

class jsd:
    def __init__(self, paths, zipfs, output=None, use_cli = False, extensions=["json"]):
        if isinstance(paths, str):
            paths = [paths]
        self._paths = paths
        self._extensions = extensions
        self._zipfs = zipfs
        self._output = output
        self._use_cli = use_cli
        self._file_label = lambda path: 1
        self._lock = Lock()
        self._divergences = Manager().list()
        self._myManager = MyManager()
        self._myManager.start()
        self._statistic = self._myManager.statistic()

        self._processes_number = cpu_count()

        if self._use_cli:
            self._cli = cli(self._statistic)

        self._factory = zipf_from_file()

    def set_interface(self, file_interface):
        self._factory.set_interface(file_interface)

    def set_word_filter(self, word_filter):
        self._factory.set_word_filter(word_filter)

    def set_file_label(self, file_label):
        if file_label != None:
            self._file_label = file_label

    def _load_paths(self):
        files_list = []
        for extension in self._extensions:
            for path in self._paths:
                files_list += glob.iglob(path+"/**/*.%s"%extension)
        self._statistic.set_total_files(len(files_list))
        return chunks(files_list, math.ceil(len(files_list)/self._processes_number))

    def job(self, paths):
        self._statistic.set_live_process("jsd calculator")
        divergences = []
        for path in paths:
            divergence = []
            divergence.append(self._file_label(path))

            try:
                file_zipf = self._factory.run(path)
            except ValueError as e:
                continue

            for _zipf in self._zipfs:
                divergence.append(_zipf.JSD(file_zipf))
            divergences.append(divergence)
            self._statistic.add_batch("jsd")

        self._lock.acquire()
        self._divergences += divergences
        self._lock.release()
        self._statistic.set_dead_process("jsd calculator")

    def run(self):
        if self._use_cli:
            self._cli.run()

        self._statistic.set_phase("Loading file paths")
        processes = []
        for i, ch in enumerate(self._load_paths()):
            process = Process(target=self.job, args=(ch,))
            process.start()
            processes.append(process)
        self._statistic.set_phase("Calculating file divergences from %s zipfs"%len(self._zipfs))
        for p in processes:
            p.join()

        if self._output!=None:
            self._statistic.set_phase("Saving file")
            with open(self._output, "w") as f:
                json.dump(self._divergences, f)

        self._statistic.done()

        if self._use_cli:
            self._cli.join()

        return list(self._divergences)
