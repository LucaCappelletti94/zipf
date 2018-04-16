from ...statistic.statistic import statistic
from ...statistic.derivative import derivative
import time

class statistic_from_dir(statistic):
    def __init__(self):
        super().__init__()
        self._files = 0
        self._zipfs = 0
        self._total_files = 0
        self._estimate_update_timeout = 1
        self._last_estimate_update = 0
        self._elaboration_speed = derivative(1)
        self._load_speed = derivative(1)
        self._loader_done = False

    def set_loader_done(self):
        self._loader_done = True

    def set_total_files(self, total_files):
        self._total_files = total_files

    def add_file(self):
        self._lock.acquire()
        self._files+=1
        self._lock.release()

    def add_zipf(self):
        self._lock.acquire()
        self._zipfs+=1
        self._lock.release()

    def is_loader_done(self):
        return self._loader_done

    def get_files(self):
        return self._files

    def get_zipfs(self):
        return self._zipfs

    def get_total_files(self):
        return self._total_files

    def get_elaboration_speed(self):
        return self._elaboration_speed.speed()

    def get_load_speed(self):
        if self._loader_done:
            return 0
        return self._load_speed.speed()

    def step_speeds(self):
        if time.time() - self._last_estimate_update > self._estimate_update_timeout:
            self._last_estimate_update = time.time()
            self._elaboration_speed.step(self._zipfs)
            self._load_speed.step(self._files)

    def get_remaining_elaboration_time(self):
        return self._get_remaining_time(
            self._total_files - self._elaboration_speed.position(),
            self._elaboration_speed.speed()
        )
