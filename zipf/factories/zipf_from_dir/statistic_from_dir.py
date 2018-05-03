from ...statistic import statistic, derivative
import time

class statistic_from_dir(statistic):
    def __init__(self):
        super().__init__()
        self._zipfs = 0
        self._total_files = 0
        self._empty_files = 0
        self._empty_wordlists = 0
        self._estimate_update_timeout = 1
        self._last_estimate_update = 0
        self._elaboration_speed = derivative(1, resolution=100)
        self._loader_done = False

    def set_loader_done(self):
        self._loader_done = True

    def set_total_files(self, total_files):
        self._total_files = total_files

    def add_zipf(self, value=1):
        self._lock.acquire()
        self._zipfs+=value
        self._lock.release()

    def add_empty_file(self, value=1):
        self._lock.acquire()
        self._empty_files+=value
        self._lock.release()

    def add_empty_wordlist(self, value=1):
        self._lock.acquire()
        self._empty_wordlists+=value
        self._lock.release()

    def is_loader_done(self):
        return self._loader_done

    def get_zipfs(self):
        return self._zipfs

    def get_empty_files(self):
        return self._empty_files

    def get_empty_wordlists(self):
        return self._empty_wordlists

    def get_total_files(self):
        return self._total_files

    def get_elaboration_speed(self):
        if self._total_files - self._empty_files - self._empty_wordlists - self._zipfs == 0:
            return 0
        return self._elaboration_speed.speed()

    def step_speeds(self):
        if time.time() - self._last_estimate_update > self._estimate_update_timeout:
            self._last_estimate_update = time.time()
            self._elaboration_speed.step(self._zipfs + self._empty_wordlists +  self._empty_files)

    def get_remaining_elaboration_time(self):
        return self._get_remaining_time(
            self._total_files - self._empty_files - self._empty_wordlists - self._zipfs,
            self._elaboration_speed.speed()
        )
