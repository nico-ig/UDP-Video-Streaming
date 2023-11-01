import threading
import queue

from src.utils import StreamHeap as sh

DICT_CLIENT = {}
DICT_WATCHDOG = {}
CHILDREN = {}

SERVER_NAME = ""
SERVER_PORT = 0
NETWORK = None

BLOCKSIZE = 1024 # Power of two that fits in MTU = 1500

STOP_EVENT = threading.Event()
CLIENTS_QUEUE = queue.Queue()

stream = sh.stream_player

