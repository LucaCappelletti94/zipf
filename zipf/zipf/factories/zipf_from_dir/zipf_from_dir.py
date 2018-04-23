from multiprocessing import Manager, Pool, Process, cpu_count
from ...mp.managers import MyManager
from ...utils import chunks
from ...zipf import zipf
from ...factories import zipf_from_file
from .statistic_from_dir import statistic_from_dir as statistic
from .cli_from_dir import cli_from_dir as cli

import glob
import math
import re

MyManager.register('statistic', statistic)

class zipf_from_dir(zipf_from_file):
    def __init__(self, use_cli=False):
        super().__init__()
        self._use_cli = use_cli

    def _text_to_zipf(self, paths):
        z = zipf()
        n = 0
        self._statistic.set_live_process("text to zipf converter")
        for path in paths:
            try:
                z = self.enrich(path, z)
                n+=1
            except ValueError as e:
                pass

            self._statistic.add_zipf()
        self._zipfs.append(z/n)
        self._statistic.set_dead_process("text to zipf converter")

    def _merge(zipfs):
        return zipfs[0] + zipfs[1]

    def _load_paths(self):
        files_list = []
        paths = []
        for path in self._paths:
	        if len(self._extensions):
	        	for extension in self._extensions:
	        		paths.append(path+"/**/*.%s"%extension)
	        else:
	        	paths.append(path+"/**/*.*")

        for path in paths:
            files_list += glob.iglob(path)

        files_number = len(files_list)
        if not files_number:
        	raise ValueError("The given path does not contain files")
        self._statistic.set_total_files(files_number)
        return chunks(files_list, math.ceil(len(files_list)/self._processes_number))

    def run(self, path = None, extensions = [], paths=[]):
        self._myManager = MyManager()
        self._myManager.start()
        self._statistic = self._myManager.statistic()

        if self._use_cli:
            self._cli = cli(self._statistic)

        if path:
            paths.append(path)
        self._paths = []
        self._paths = paths
        self._extensions = extensions

        self._processes_number = cpu_count()
        self._zipfs = Manager().list()

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
        with Pool(self._processes_number) as p:
            while len(zipfs)>=2:
                zipfs = list(p.imap(zipf_from_dir._merge, list(chunks(zipfs, 2))))

        self._statistic.set_phase("Normalizing zipfs")

        final_zipf = (zipfs[0]/self._processes_number).sort()

        self._statistic.done()

        if self._use_cli:
            self._cli.join()

        return final_zipf