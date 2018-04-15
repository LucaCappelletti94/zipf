import os
import json
import glob
from multiprocessing import Queue, Process
from tqdm import tqdm

class loader:

    PROCESSES_NUMBER = 4

    def __init__(self, path, extensions, statistic, timeout=60):
        if type(extensions)==str:
            extensions = [extensions]
        self._validate_input(path, extensions)
        self._statistic = statistic
        self._path, self._extensions, self._files, self._timeout= path, extensions, Queue(), timeout
        self._processes = []
        self._name = path.split("/")[-1]


    def _validate_input(self, path, extension):
        if not self._path_exists(path):
            raise ValueError("Given path %s does not exist"%path)
        if self._path_empty(path, extension):
            raise ValueError("Given path %s does not contain files of given extensions"%path)

    def _path_exists(self, path):
        return os.path.isdir(path)

    def _path_empty(self, path, extensions):
        for extension in extensions:
            for filename in glob.iglob(path+"/**/*.%s"%extension):
                return False
        return True

    def _loader(self, files_list):
        self._statistic.set_live_process("file loader")
        for filename in files_list:
            with open(filename, "r") as f:
                if filename.endswith(".json"):
                    obj = json.load(f)
                else:
                    obj = f.read()
                self._files.put(obj, timeout=self._timeout)
                self._statistic.add_file()
        self._statistic.set_dead_process("file loader")

    def get_queue(self):
        return self._files

    def chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def run(self):
        files_list = []
        for extension in self._extensions:
            files_list += glob.iglob(self._path+"/**/*.%s"%extension)

        self._statistic.set_total_files(len(files_list))
        files_chunks = list(self.chunks(files_list, int(len(files_list)/self.PROCESSES_NUMBER)))

        for i in range(self.PROCESSES_NUMBER):
            p = Process(target=self._loader, args=(files_chunks[i],), name="File loader %s n. %s"%(self._name, i))
            p.start()
            self._processes.append(p)

    def join(self):
        for p in self._processes:
            p.join()
