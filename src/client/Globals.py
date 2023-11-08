'''
Global values for the client
'''

import threading

from src.utils import Logger
from src.client.stream import StreamHeap as SH

SERVER = ()                 # Server address
NETWORK = None              # Network interface

TIMERS = []                 # TImers used by client
STREAM_TIMER = None         # Timer dedicated to server 

SERVER_TIMEOUT = 10         # Time in seconds before timeouting when not receiving packets from server
STREAM_TIMEOUT =  20        # How many intervals without receiving stream packets before timeouting  
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
        Logger.LOGGER.info("Closing client")

        STOP_EVENT.set()
   
        if NETWORK != None:
            NETWORK.stop()

        if STREAM_TIMER != None:
            STREAM_TIMER.stop()
            
        for timer in TIMERS:
            timer.stop()

        for event in STOP_EVENTS:
            event.set()

    except Exception as e:
        Logger.LOGGER.error("Error while closing client: %s", str(e))

    finally:
        Logger.LOGGER.info("Exiting")