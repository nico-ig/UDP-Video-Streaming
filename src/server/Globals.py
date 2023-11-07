import queue
import threading

from src.utils import Logger as L

TIMER = None
TIMERS = []

CHILDREN = {}               # Child processes
CLIENTS = set()             # Clients registered

NETWORK = None              # Netowrk interface
SERVER_PORT = 0 
SERVER_NAME = ""

BLOCKSIZE = 8192            # Size of audio stream block in stream packet
AUDIO_FOLDER = 'audios'

INTERVAL = 6_250_000        # Interval in ns between stream packets
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
        L.LOGGER.info("Closing server")

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
        L.LOGGER.error("An error occurred: %s", str(e))

    finally:
        L.LOGGER.info("Exitting")
        exit()
