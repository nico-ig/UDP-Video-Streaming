"""
Deals with timeouts and time management callbacks
"""

from utils import Utils

import threading
import time

class Timer:
    """
    Creates and manages a timer. The timeout is calculated in nanoseconds
    """
    def __init__(self, timeout, callback):
        try:
            self.logger = Logger.get_logger('timer')

            self._timeout = timeout * 1e9
            self.callback = callback
            self.stop_event = threading.Event()
            self.last_kick = time.time_ns()

            self.timer_thread = Utils.start_thread(self.timer)

        except Exception as e:
            error_message = 'Error creating timer - ' + type(e)+ ': ' + str(e)
            self.logger.error(error_message)

    def timer(self):
        """
        Callback function to emulate a timer
        """
        try:
            while not self.stop_event.is_set():
                if (time.time_ns() - self.last_kick >= self.timeout):
                    self.callback()
                    break
        except:
            pass
        
    def kick(self):
        """
        Kick the timer, preventing it from expiring
        """
        try:
            self.last_kick = time.time_ns()
        except:
            pass

    def stop(self):
        """
        Stops the timer
        """
        try:
            self.stop_event.set()
        except:
            pass