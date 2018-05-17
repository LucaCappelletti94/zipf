from ...statistic import Statistic, Derivative
from time import time


class StatisticFromDir(Statistic):
    def __init__(self):
        super().__init__()
        self._zipfs = 0
        self._total_files = 0
        self._empty_files = 0
        self._empty_lists = 0
        self._estimate_update_timeout = 1
        self._last_estimate_update = 0
        self._elaboration_speed = Derivative(1, resolution=100)
        self._loader_done = False

    def set_loader_done(self):
        self._loader_done = True

    def set_total_files(self, total_files):
        self._total_files = total_files

    def add_zipf(self, value=1):
        self._lock_sum(self._zipfs, value)

    def add_empty_file(self, value=1):
        self._lock_sum(self._empty_files, value)

    def add_empty_list(self, value=1):
        self._lock_sum(self._empty_lists, value)

    def is_loader_done(self):
        return self._loader_done

    def get_zipfs(self):
        return self._zipfs

    def get_empty_files(self):
        return self._empty_files

    def get_empty_lists(self):
        return self._empty_lists

    def get_total_files(self):
        return self._total_files

    def _remaing_files(self):
        return self._total_files - self._empty_files - self._empty_lists - self._zipfs

    def get_elaboration_speed(self):
        if self._remaing_files() == 0:
            return 0
        return self._elaboration_speed.speed()

    def step_speeds(self):
        if time() - self._last_estimate_update > self._estimate_update_timeout:
            self._last_estimate_update = time()
            self._elaboration_speed.step(
                self._zipfs + self._empty_lists + self._empty_files)

    def get_remaining_elaboration_time(self):
        return self._get_remaining_time(
            self._remaing_files(),
            self._elaboration_speed.speed()
        )
