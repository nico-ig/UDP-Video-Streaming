'''
Global values for the client
'''

import threading

from src.utils import Logger
from src.utils import StreamHeap as sh

NETWORK = None          # Network interface
SERVER = None           # Server address
SERVER_TIMER = None     
TIMER = None

HANDSHAKE_TIMEOUT = 10
SERVER_TIMEOUT = 5              # Time in seconds before timeouting when not receiving packets from server
RETRANSMIT_TIMEOUT = 3    # Time in seconds before sending NEW_PORT_REQUEST again

REGISTER_DURATION = 10      # The durantion of the registration phase received by the server

STREAM_TIMEOUT =  10      # The start value in the amount of intervals between stream packets before timeouting

STOP_EVENT= threading.Event()
PORT_ALLOCATED = threading.Event()
REGISTER_ACK = threading.Event()
STREAM_STARTED = threading.Event()

STREAM = sh.stream_player

def CLOSE_CLIENT(close_stream_not_started=False):
    '''
    Handle the end of handhsake/registration timer
    '''
    try:
        if (close_stream_not_started and not STREAM_STARTED.is_set()) or not REGISTER_ACK.is_set():
            Logger.LOGGER.info("Couldn't start stream")
            SIGINT_HANDLER()

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def SIGINT_HANDLER(signum=0, frame=''):
    '''
    Stops the client when sigint is received
    '''
    try:
        Logger.LOGGER.info("Sigint received")

        STOP_EVENT.set()
        PORT_ALLOCATED.set()
        REGISTER_ACK.set()
        STREAM_STARTED.set()
   
        if NETWORK != None:
            NETWORK.stop()

        if SERVER_TIMER != None:
            SERVER_TIMER.stop()
            
        if TIMER != None:
            TIMER.stop()

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

    finally:
        Logger.LOGGER.info("Exitting")