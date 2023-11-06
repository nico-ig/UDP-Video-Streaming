import threading
import queue

IPV4 = False

DICT_CLIENT = {}
DICT_WATCHDOG = {}
CHILDREN = {}

SERVER_NAME = ""
SERVER_PORT = 0
NETWORK = None

BLOCKSIZE = 8192

STOP_EVENT = threading.Event()
CLIENTS_QUEUE = queue.Queue()

AUDIO_TITLES = []
AUDIO_PACKETS = []
AUDIO_FOLDER = 'audios'
