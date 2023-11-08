import queue
import threading
import multiprocessing

from src.utils import Logger as L

TIMER = None
TIMERS = []

CHILDREN = {}               # Child processes
CLIENTS = set()             # Clients registered

NETWORK = None              # Netowrk interface
SERVER_PORT = 0 
SERVER_NAME = ""

BLOCKSIZE = 16384            # Size of audio stream block in stream packet
AUDIO_FOLDER = 'audios'

INTERVAL = 10_000_000        # Interval in ns between stream packets
RETRANSMIT_TIMEOUT = 3      # Time in s before retrasmiting a packet 
REGISTRATION_DURATION = 30  # Duration of registration

STOP_EVENTS = []
STOP_EVENT = threading.Event()
CLIENTS_QUEUE = queue.Queue()

def CLOSE_SERVER(signum = 0, fram = ''):
    '''
    Callback function to stop the stream when sigint is received
    '''
    try:
        if multiprocessing.current_process().name == 'MainProcess':
            L.LOGGER.info("Closing server")
        else:
            L.LOGGER.info("Closing stream")

        STOP_EVENT.set()

        if NETWORK != None:
            NETWORK.stop()

        if TIMER != None:
            TIMER.stop()

        for event in STOP_EVENTS:
            event.set()

        for timer in TIMERS:
            timer.stop()
 
    except Exception as e:
        if multiprocessing.current_process().name == 'MainProcess':
            L.LOGGER.error("Error while closing server: %s", str(e))
        else:
            L.LOGGER.error("Error while closing stream: %s", str(e))

    finally:
        if multiprocessing.current_process().name == 'MainProcess':
            L.LOGGER.info("Exiting server")
        else:
            L.LOGGER.info("Exiting stream")

        exit()
