import time


class Derivative:

    def __init__(self, resolution=1000):
        self._first = True
        self._old_value = 0
        self._last_time = 0
        self._resolution = resolution
        self._derivatives = []

    def step(self, value):
        if self._first:
            self._first = False
        else:
            self._update_derivative(value)
        self._update(value)

    def position(self):
        if not self._first:
            return self._old_value
        return 0

    def speed(self):
        if len(self._derivatives) > 0:
            return self._mean()
        return 0

    def _mean(self):
        return sum(self._derivatives) / len(self._derivatives)

    def _update_derivative(self, value):
        new_derivative = (value - self._old_value) / \
            (time.time() - self._last_time)
        self._derivatives.append(new_derivative)
        self._derivatives = self._derivatives[-self._resolution:]

    def _update(self, value):
        self._last_time = time.time()
        self._old_value = value
