import threading
import time

class Watchdog:
    def __init__(self, timeout, callback):
        _ = self
        _._timeout = timeout * 1e9
        _._callback = callback
        _._stop_event = threading.Event()
        _._last_kick = time.time_ns()
        _._start_watchdog()

    def _start_watchdog(_):
        _._watchdog_thread = threading.Thread(target=_._watchdog_timer)
        _._watchdog_thread.start()

    def _watchdog_timer(_):
        while not _._stop_event.is_set():
            if (time.time_ns() - _._last_kick >= _._timeout):
                _._callback(_)
                break
        
    def kick(_):
        _._last_kick = time.time_ns()

    def stop(_):
        _._stop_event.set()
