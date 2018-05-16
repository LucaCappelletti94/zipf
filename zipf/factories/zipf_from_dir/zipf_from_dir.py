from multiprocessing import Manager, Pool, Process, cpu_count
from ...mp.managers import MyManager
from ...utils import chunks
from ...zipf import Zipf
from ...factories import ZipfFromFile
from .statistic_from_dir import statistic_from_dir as statistic
from .cli_from_dir import cli_from_dir as cli

import glob
import math
import json
import re


MyManager.register('statistic', statistic)

class ZipfFromDir(ZipfFromFile):
    def __init__(self, options= None, use_cli=False):
        super().__init__(options)
        self._use_cli = use_cli

    def _text_to_zipf(self, paths):
        z = Zipf()
        n = 0
        self._statistic.set_live_process("text to zipf converter")
        for path in paths:
            z = super().enrich(path, z)
            n+=1
            self._statistic.add_zipf()
        self._zipfs.append(z/n)
        self._statistic.set_dead_process("text to zipf converter")

    def _merge(zipfs):
        if len(zipfs)==2:
            return zipfs[0] + zipfs[1]
        return zipfs[0]

    def _load_paths(self):
        files_list = []
        paths = []
        for path in self._paths:
            if len(self._extensions):
                for extension in self._extensions:
                    paths.append(path+"/*.%s"%extension)
            else:
                paths.append(path+"/*.*")

        for path in paths:
            files_list += glob.glob(path)

        files_number = len(files_list)
        if files_number == 0:
            return None
        self._statistic.set_total_files(files_number)
        return chunks(files_list, math.ceil(len(files_list)/self._processes_number))

    def run(self, paths, extensions = None):
        if isinstance(paths, str):
            self._paths = [paths]
        elif isinstance(paths, list):
            self._paths = paths
        else:
            raise ValueError("No paths were given.")

        self._myManager = MyManager()
        self._myManager.start()
        self._statistic = self._myManager.statistic()

        if self._use_cli:
            self._cli = cli(self._statistic)

        self._extensions = []
        if extensions:
            self._extensions = extensions

        self._processes_number = cpu_count()
        self._zipfs = Manager().list()

        if self._use_cli:
            self._cli.run()

        self._statistic.set_phase("Loading file paths")
        processes = []
        chk = self._load_paths()
        if chk == None:
            return Zipf()
        for i, ch in enumerate(chk):
            process = Process(target=self._text_to_zipf, args=(ch,))
            process.start()
            processes.append(process)
        self._statistic.set_phase("Converting files to zipfs")
        for p in processes:
            p.join()
        zipfs = self._zipfs
        n = len(zipfs)


        with Pool(min(self._processes_number, n)) as p:
            while len(zipfs)>=2:
                self._statistic.set_phase("Merging %s zipfs"%len(zipfs))
                zipfs = list(p.imap(ZipfFromDir._merge, list(chunks(zipfs, 2))))

        self._statistic.set_phase("Normalizing zipfs")

        final_zipf = (zipfs[0]/n).sort()

        self._statistic.done()

        if self._use_cli:
            self._cli.join()

        return final_zipf

    def enrich(self, paths, zipf, extensions = None):
        return zipf+self.run(paths, extensions)
