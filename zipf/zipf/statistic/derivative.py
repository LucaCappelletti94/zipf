import time

class derivative:

    def __init__(self, degree, resolution=1000):
        self._degree = degree
        self._first = True
        self._old_value = 0
        self._last_time = 0
        self._resolution = resolution
        self._derivatives = []
        if self._degree > 1:
            self._sub_derivative = derivative(self._degree-1)

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

    def acceleration(self):
        if self._degree > 1:
            return self._sub_derivative.speed()
        return 0

    def jerk(self):
        if self._degree > 2:
            return self._sub_derivative.acceleration()
        return 0

    def _mean(self):
        return sum(self._derivatives) / len(self._derivatives)

    def _update_derivative(self, value):
        new_derivative = (value - self._old_value)/(time.time() - self._last_time)
        self._derivatives.append(new_derivative)
        self._derivatives = self._derivatives[-self._resolution:]
        if self._degree > 1:
            self._sub_derivative.step(new_derivative)

    def _update(self, value):
        self._last_time = time.time()
        self._old_value = value