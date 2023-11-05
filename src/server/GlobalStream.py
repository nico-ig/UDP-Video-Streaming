from concurrent.futures import thread
import threading

IPV4 = False

INTERVAL = 500_000      # Interval in ns between stream packets

LIDER = None

TIMER = None
LOGGER = None
NETWORK = None

PORT_ALLOCATED_TIMEOUT = 5

CLIENTS = set()
START_EVENT = threading.Event()
STOP_EVENT = threading.Event()

AUDIO_ID = -1
AUDIO_FILE = ''
PORT_ACK_RECEIVED = threading.Event()

REGISTRATION_DURATION = 15
