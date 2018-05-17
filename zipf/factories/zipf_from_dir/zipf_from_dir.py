from multiprocessing import Manager, Pool, Process, cpu_count
from ...mp.managers import MyManager
from ...utils import chunks
from ...zipf import Zipf
from ...factories import ZipfFromFile
from .statistic_from_dir import StatisticFromDir as statistic
from .cli_from_dir import CliFromDir as cli
from math import ceil

from glob import glob
import json
import re

MyManager.register('statistic', statistic)


class ZipfFromDir(ZipfFromFile):
    def __init__(self, options=None, use_cli=False):
        super().__init__(options)
        self._use_cli = use_cli
        self._myManager = MyManager()
        self._myManager.start()
        self._processes_number = cpu_count()

    def _text_to_zipf(self, paths):
        z = Zipf()
        n = 0
        self._statistic.set_live_process("text to zipf converter")
        for path in paths:
            z = super().enrich(path, z)
            n += 1
            self._statistic.add_zipf()
        self._zipfs.append(z/n)
        self._statistic.set_dead_process("text to zipf converter")

    def _merge(zipfs):
        if len(zipfs) == 2:
            return zipfs[0] + zipfs[1]
        return zipfs[0]

    def _validate_base_paths(self, base_paths):
        if isinstance(base_paths, str):
            return [base_paths]
        if isinstance(base_paths, list):
            return base_paths
        raise ValueError("No paths were given.")

    def _prepare_extensions(self, extensions):
        if extensions:
            self._extensions = extensions
        else:
            self._extensions = ["*"]

    def _load_paths(self, base_paths):
        files_list = []
        for path in self._validate_base_paths(base_paths):
            for extension in self._extensions:
                files_list += glob(path+"/*.%s" % extension)

        files_number = len(files_list)
        if files_number == 0:
            return None
        self._statistic.set_total_files(files_number)
        return chunks(files_list, ceil(files_number/self._processes_number))

    def _render_zipfs(self, paths_chunk_generator):
        self._statistic.set_phase("Loading file paths")
        self._zipfs = Manager().list()
        processes = []
        for i, ch in enumerate(paths_chunk_generator):
            process = Process(target=self._text_to_zipf, args=(ch,))
            process.start()
            processes.append(process)
        self._statistic.set_phase("Converting files to zipfs")
        for p in processes:
            p.join()
        return self._zipfs

    def _merge_zipfs(self, zipfs):
        with Pool(min(self._processes_number, len(zipfs))) as p:
            while len(zipfs) >= 2:
                self._statistic.set_phase("Merging %s zipfs" % len(zipfs))
                zipfs = list(
                    p.imap(ZipfFromDir._merge, list(chunks(zipfs, 2))))
        return zipfs[0]

    def run(self, paths, extensions=None):
        self._statistic = self._myManager.statistic()
        self._prepare_extensions(extensions)

        if self._use_cli:
            self._cli = cli(self._statistic)
            self._cli.run()

        paths_chunk_generator = self._load_paths(paths)
        if paths_chunk_generator is None:
            return Zipf()

        zipfs = self._render_zipfs(paths_chunk_generator)

        zipfs_number = len(zipfs)

        zipf = self._merge_zipfs(zipfs)

        self._statistic.set_phase("Normalizing zipfs")

        normalized_zipf = (zipf/zipfs_number).sort()

        self._statistic.done()

        if self._use_cli:
            self._cli.join()

        return normalized_zipf

    def enrich(self, paths, zipf, extensions=None):
        return zipf+self.run(paths, extensions)
