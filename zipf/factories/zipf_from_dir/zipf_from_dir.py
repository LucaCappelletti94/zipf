from glob import glob
from multiprocessing import Manager, Process, cpu_count
from os import walk
from os.path import join

from ...factories import ZipfFromFile
from ...mp.managers import MyManager
from ...zipf import Zipf
from .cli_from_dir import CliFromDir as cli
from .statistic_from_dir import StatisticFromDir

MyManager.register('StatisticFromDir', StatisticFromDir)


class ZipfFromDir(ZipfFromFile):
    def __init__(self, options=None, use_cli=False):
        super().__init__(options)
        self._opts["sort"] = False
        self._use_cli = use_cli
        self._myManager = MyManager()
        self._myManager.start()
        self._processes_number = cpu_count()

    def _text_to_zipf(self, paths):
        self.set_product(Zipf())
        use_cli = self._use_cli
        self._statistic.set_live_process("text to zipf converter")
        n = 50
        i = 0
        for path in paths:
            super().run(path)
            i += 1
            if i % n == 0 and use_cli:
                self._statistic.add_zipf(n)

        if use_cli:
            self._statistic.add_zipf(i % n)
        self._zipfs.append((self.get_product() / len(paths)).render())
        self._statistic.set_dead_process("text to zipf converter")

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
        n = self._processes_number
        files_list = []
        for i in range(n):
            files_list.append([])
        i = 0
        files_number = 0
        for path in self._validate_base_paths(base_paths):
            for extension in self._extensions:
                for x in walk(path):
                    for y in glob(join(x[0], '*.%s' % extension)):
                        files_list[i].append(y)
                        files_number += 1
                        i = (i + 1) % n

        if files_number == 0:
            return None
        self._statistic.set_total_files(files_number)
        return files_list

    def _render_zipfs(self, chunked_paths):
        self._zipfs = Manager().list()
        processes = []
        self._statistic.set_phase("Starting processes")
        for ch in chunked_paths:
            process = Process(target=self._text_to_zipf, args=(ch,))
            process.start()
            processes.append(process)
        self._statistic.set_phase("Converting files to zipfs")
        for p in processes:
            p.join()
        return self._zipfs

    def run(self, paths, extensions=None):
        self._statistic = self._myManager.StatisticFromDir()
        self._prepare_extensions(extensions)

        if self._use_cli:
            self._cli = cli(self._statistic)
            self._cli.run()

        self._statistic.set_phase("Loading file paths")
        chunked_paths = self._load_paths(paths)
        if chunked_paths is None:
            self._statistic.done()
            if self._use_cli:
                self._cli.join()
            return Zipf()

        zipfs = self._render_zipfs(chunked_paths)

        self._statistic.set_phase("Normalizing zipfs")

        if len(zipfs) == 0:
            self._statistic.done()
            if self._use_cli:
                self._cli.join()
            return Zipf()

        normalized_zipf = (sum(zipfs) / len(zipfs)).sort()

        self._statistic.done()

        if self._use_cli:
            self._cli.join()

        return normalized_zipf
