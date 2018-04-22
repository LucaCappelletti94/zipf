from ..statistic import statistic, derivative
import time

class batch_statistic(statistic):
    def __init__(self):
        super().__init__()
        self._batch = {}
        self._total_files = 0
        self._estimate_update_timeout = 0.2
        self._last_estimate_update = 0
        self._elaboration_speed = derivative(1, resolution=100)

    def set_total_files(self, total_files):
        self._total_files = total_files

    def add_batch(self, name):
        self._edit_dict(self._batch, name, 1)

    def get_batches(self):
        return self._batch

    def get_total_files(self):
        return self._total_files

    def get_elaboration_speed(self):
        if self._total_files - sum(self._batch.values()) == 0:
            return 0
        return self._elaboration_speed.speed()

    def step_speeds(self):
        if time.time() - self._last_estimate_update > self._estimate_update_timeout:
            self._last_estimate_update = time.time()
            self._elaboration_speed.step(sum(self._batch.values()))

    def get_remaining_elaboration_time(self):
        return self._get_remaining_time(
            self._total_files - sum(self._batch.values()),
            self._elaboration_speed.speed()
        )
