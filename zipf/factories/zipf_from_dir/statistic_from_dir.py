from time import time

from ...statistic import Derivative, Statistic


class StatisticFromDir(Statistic):
    def __init__(self):
        super().__init__()
        self._zipfs = 0
        self._total = 0
        self._elaboration_speed = Derivative(resolution=100)

    def set_total_files(self, total_files):
        self._total = total_files

    def add_zipf(self, value=1):
        self._lock.acquire()
        self._zipfs += value
        self._lock.release()

    def get_zipfs(self):
        return self._zipfs

    def get_total_files(self):
        return self._total

    def _remaing_files(self):
        return self._total - self._zipfs

    def get_elaboration_speed(self):
        if self._remaing_files() == 0:
            return 0
        return self._elaboration_speed.speed()

    def step_speeds(self):
        self._elaboration_speed.step(self._zipfs)

    def get_remaining_elaboration_time(self):
        return self._get_remaining_time(
            self._remaing_files(),
            self._elaboration_speed.speed()
        )
