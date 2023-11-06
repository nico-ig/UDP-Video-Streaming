'''
Global values for the client
'''

import threading

from src.utils import Logger

IPV4 = False
NETWORK = None          # Network interface
SERVER = None           # Server address
SERVER_TIMER = None     
TIMER = None
PLAYER = None

AUDIO_CHOSEN = threading.Event()
AUDIO_TITLE = ''
AUDIO_SAMPLERATE = 0
AUDIO_CHANNELS = 0
AUDIO_BLOCKSIZE = 0
AUDIO_BUFFER = None
AUDIO_TITLES = []
AUDIO_ID = -1
AUDIO_CHOICE_TIMEOUT = 5
AUDIO_CONFIG = threading.Event()

HANDSHAKE_TIMEOUT = 30
SERVER_TIMEOUT = 10              # Time in seconds before timeouting when not receiving packets from server
RETRANSMIT_TIMEOUT = 3    # Time in seconds before sending NEW_PORT_REQUEST again

REGISTER_DURATION = 0      # The durantion of the registration phase received by the server

STREAM_TIMEOUT =  10      # The start value in the amount of intervals between stream packets before timeouting

STOP_EVENT= threading.Event()
PORT_ALLOCATED = threading.Event()
REGISTER_ACK = threading.Event()
STREAM_STARTED = threading.Event()

def CLOSE_CLIENT():
    '''
    Handle the end of handhsake/registration timer
    '''
    try:
        if not REGISTER_ACK.is_set():
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

        if PLAYER != None:
            PLAYER.stop()

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

    finally:
        Logger.LOGGER.info("Exitting")