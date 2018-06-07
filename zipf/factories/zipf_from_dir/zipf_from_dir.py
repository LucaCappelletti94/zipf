"""ZipfFromDir create a Zipf from a directory with text files."""
from glob import glob
from multiprocessing import Manager, Process, cpu_count, Queue, Value
from multiprocessing.managers import BaseManager
from os import walk
from os.path import join
import queue
import time

from ...factories import ZipfFromFile
from ...zipf import Zipf
from .cli_from_dir import CliFromDir as cli
from .statistic_from_dir import StatisticFromDir


class MyManager(BaseManager):
    """Extend BaseManager to be customizable."""

    pass


MyManager.register('StatisticFromDir', StatisticFromDir)


class ZipfFromDir(ZipfFromFile):
    """ZipfFromDir create a Zipf from a directory with text files."""

    def __init__(self, options=None, use_cli=False):
        """Create a ZipfFromDir with give options."""
        super().__init__(options)
        self._opts["sort"] = False
        self._use_cli = use_cli
        self._myManager = MyManager()
        self._myManager.start()
        self._processes = None
        self._statistic = self._myManager.StatisticFromDir()
        self._processes_number = cpu_count()

    def _paths_to_zipf(self):
        """Create a Zipf from given paths."""
        while not self._kill.value:
            try:
                paths = self._queue.get(False)
            except queue.Empty:
                time.sleep(0.1)
                continue
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
            self._result_queue.put(self.get_product() / len(paths))
            self._statistic.set_dead_process("text to zipf converter")

    def _validate_base_paths(self, base_paths):
        """Validate paths argument."""
        if isinstance(base_paths, str):
            return [base_paths]
        if isinstance(base_paths, list):
            return base_paths
        raise ValueError("No paths were given.")

    def _setup_extensions(self, extensions):
        """Handle setup of given extensions list."""
        if extensions:
            self._extensions = extensions
        else:
            self._extensions = ["*"]

    def _load_paths(self, base_paths):
        """Recursively load paths from given base paths."""
        n = self._processes_number
        files_lists = []
        for i in range(n):
            files_lists.append([])
        i = 0
        files_number = 0
        for path in self._validate_base_paths(base_paths):
            for extension in self._extensions:
                for x in walk(path):
                    for y in glob(join(x[0], '*.%s' % extension)):
                        files_lists[i].append(y)
                        files_number += 1
                        i = (i + 1) % n

        if files_number == 0:
            return None
        self._statistic.set_total_files(files_number)
        return [files_list for files_list in files_lists if len(files_list)]

    def _render_zipfs(self, chunked_paths):
        """Execute Zipf rendering from paths in multiprocessing."""
        single_run = False
        if not self.are_processes_active():
            single_run = True
            self.start_processes()

        self._statistic.set_phase("Converting files to zipfs")
        n = len(chunked_paths)
        [self._queue.put(chk) for chk in chunked_paths]

        results = [self._result_queue.get() for i in range(n)]

        if single_run:
            self.close_processes()
        
        return results

    def start_processes(self):
        """Start a group of processes."""
        self._statistic.set_phase("Starting processes")
        self._kill = Value('i', 0)
        self._queue = Queue()
        self._result_queue = Queue()
        self._processes = [
            Process(target=self._paths_to_zipf) for i in range(self._processes_number)
        ]
        [p.start() for p in self._processes]

    def close_processes(self):
        """Closes the group of processes."""
        self._kill.value=1
        [p.join() for p in self._processes]
        self._processes = None

    def are_processes_active(self):
        return self._processes is not None

    def run(self, paths, extensions=None):
        """Create and return zipf created from given paths."""
        self._setup_extensions(extensions)
        self._statistic.reset()

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
