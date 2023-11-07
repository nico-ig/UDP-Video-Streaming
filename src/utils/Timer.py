'''
Deals with timeouts and time management callbacks
'''

import time
import threading

from src.utils import Utils
from src.utils import Logger

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
            Logger.LOGGER.error("An error occurred: %s", str(e))
            raise Exception("Couldn's create timer")

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
            print(f"An error occurred: {str(e)}")
        
    def kick(self):
        '''
        Kick the timer, preventing it from expiring
        '''
        self.last_kick = int(time.time_ns())

    def remaining_time(self):
        '''
        Gets the remaining time before timer expires
        '''
        return int(self.timeout - (time.time_ns() - self.last_kick)) 

    def stop(self):
        '''
        Stops the timer
        '''
        self.stop_event.set()
        self.timer_thread.join()