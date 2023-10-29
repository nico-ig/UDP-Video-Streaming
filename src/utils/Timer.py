# Deals with timeouts and time management callbacks

from utils import Utils

import threading
import time

class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout * 1e9
        self.callback = callback
        self.stop_event = threading.Event()
        self.last_kick = time.time_ns()
        self.timer_thread = Utils.start_thread(self.timer)

    def timer(self):
        while not self.stop_event.is_set():
            if (time.time_ns() - self.last_kick >= self.timeout):
                self.callback()
                break
        
    def kick(self):
        self.last_kick = time.time_ns()

    def stop(self):
        self.stop_event.set()