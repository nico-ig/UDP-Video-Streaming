import threading
import time

class Watchdog:
    def __init__(self, timeout):
        _ = self
        _._timeout = timeout * 1e9
        _._last_kick = time.time_ns()
        _._stop_event = threading.Event()
        _._start_watchdog()

    def _start_watchdog(_):
        _._watchdog_thread = threading.Thread(target=_._watchdog_timer)
        _._watchdog_thread.start()

    def _watchdog_timer(_):
        while time.time_ns() - _._last_kick < _._timeout:
            pass

        _._stop_event.set()
        
    def kick_watchdog(_):
        _._last_kick = time.time_ns()


