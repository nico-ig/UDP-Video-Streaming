from concurrent.futures import thread
import threading

IPV4 = False

INTERVAL = 6_250_000      # Interval in ns between stream packets

LIDER = None

TIMER = None
LOGGER = None
NETWORK = None

RETRANSMIT_TIMEOUT = 3    

CLIENTS = set()
CONFIRMED_CLIENTS = set()

START_EVENT = threading.Event()
STOP_EVENT = threading.Event()

AUDIO_ID = -1
AUDIO_FILE = ''
AUDIO_TITLES = []
AUDIO_PACKETS = []

PORT_ACK_RECEIVED = threading.Event()

REGISTRATION_DURATION = 30
