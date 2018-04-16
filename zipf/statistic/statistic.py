import time
from .derivative import derivative
from multiprocessing import Lock
from datetime import datetime, timedelta

class statistic:
    def __init__(self):
        self._running_processes = {}
        self._phase = ""
        self._done = False
        self._lock = Lock()
        self._estimate_update_timeout = 1
        self._last_estimate_update = 0

    def done(self):
        self._done = True

    def is_done(self):
        return self._done

    def set_start_time(self):
        self._start_time = time.time()

    def set_live_process(self, name):
        self._lock.acquire()
        delta = 1
        if name in self._running_processes.keys():
            delta += self._running_processes[name]
        self._running_processes.update({
            name: delta
        })
        self._lock.release()

    def set_dead_process(self, name):
        self._lock.acquire()
        delta = -1
        if name in self._running_processes.keys():
            delta += self._running_processes[name]
        self._running_processes.update({
            name: delta
        })
        self._lock.release()

    def set_phase(self, phase):
        self._phase = phase

    def get_phase(self):
        return self._phase

    def _format_value(self,response,value,pattern):
        if value > 0:
            if response != "":
                response+=", "
            response += pattern%value
        return response

    def _seconds_to_string(self, delta):

        if delta <= 1:
            return "now"

        d = datetime(1,1,1) + timedelta(seconds=delta)

        eta = ""
        if d.day-1>0:
            eta += "%sd"%(d.day-1)

        eta = self._format_value(eta,d.hour,  "%sh")
        eta = self._format_value(eta,d.minute, "%sm")
        eta = self._format_value(eta,d.second,"%ss")

        return eta

    def get_elapsed_time(self):
        return self._seconds_to_string(time.time()-self._start_time)

    def get_running_processes(self):
        return self._running_processes

    def _get_remaining_time(self, delta, speed):
        if delta == 0:
            return "now"
        if speed == 0:
            return "infinite"
        return self._seconds_to_string(delta/speed)