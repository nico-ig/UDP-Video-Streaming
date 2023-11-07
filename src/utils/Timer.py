'''
Deals with timeouts and time management callbacks
'''

import time
import threading

from src.utils import Utils
from src.utils import Logger as L

class Timer:
    '''
    Creates and manages a timer. The timeout is calculated in nanoseconds
    '''
    def __init__(self, timeout, callback, args = ''):
        try:
            self.timeout = int(timeout * 1e9)
            self.callback = callback
            self.args = args
            self.stop_event = threading.Event()
            self.last_kick = time.time_ns()

            self.timer_thread = Utils.start_thread(self.timer)

        except Exception as e:
            L.LOGGER.error("Error creating timer: %s", str(e))
            raise Exception("Couldn't create timer")

    def timer(self):
        '''
        Callback function to emulate a timer
        '''
        try:
            while not self.stop_event.is_set():
                if (time.time_ns() - self.last_kick >= self.timeout):
                    if self.args != '':
                        self.callback(*self.args)
                    else:
                        self.callback()
                    break

        except Exception as e:
            L.LOGGER.error(f"Error in timer callback: {str(e)}")
            raise Exception("Couldn't execute timer callback")
        
    def kick(self):
        '''
        Kick the timer, preventing it from expiring
        '''
        self.last_kick = int(time.time_ns())

    def remaining_time(self):
        '''
        Gets the remaining time before timer expires
        '''
        remaining_time =  int(self.timeout - (time.time_ns() - self.last_kick)) 
        return 0 if remaining_time < 0 else remaining_time

    def stop(self):
        '''
        Stops the timer
        '''
        try:
            self.stop_event.set()
            self.timer_thread.join()

        except Exception as e:
            L.LOGGER.error(f"Error stoping timer")