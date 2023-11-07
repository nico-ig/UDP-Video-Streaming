'''
Global values for the client
'''

import sys
import threading
from src.utils import Logger

SERVER = ()                 # Server address
NETWORK = None              # Network interface

TIMERS = []                 # TImers used by client
SERVER_TIMER = None         # Timer dedicated to server 

SERVER_TIMEOUT = 10         # Time in seconds before timeouting when not receiving packets from server
STREAM_TIMEOUT =  10        # How many intervals without receiving stream packets before timeouting  
RETRANSMIT_TIMEOUT = 3      # Time in seconds before retransmiting a packet
HANDSHAKE_TIMEOUT = 30      # Time in seconds to timeout if streaming is not started
AUDIO_CHOICE_TIMEOUT = 5    # Time in seconds before chosing default audio id

STOP_EVENT = threading.Event()
STOP_EVENTS = []            # Auxiliar stop events

def CLOSE_CLIENT(signum=0, frame=''):
    '''
    Stops the client
    '''
    try:
        Logger.LOGGER.info("Couldn't start stream, closing client")

        STOP_EVENT.set()
   
        if NETWORK != None:
            NETWORK.stop()

        if SERVER_TIMER != None:
            SERVER_TIMER.stop()
            
        for timer in TIMERS:
            timer.stop()

        for event in STOP_EVENTS:
            event.set()

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

    finally:
        Logger.LOGGER.info("Exitting")
        exit()