'''
Deals with the stream management 
Sends stream packets to clients
This should run in a separeted process from the main server
'''

from tarfile import BLOCKSIZE
import threading

from src.utils import Utils
from src.utils import Timer
from src.utils import Logger as L
from src.server import Globals as G
from src.network import Utils as NU
from src.server.stream import Packets as P

stream_packet_sent = threading.Event()

AUDIO_ID = -1
AUDIO_TITLES = []
AUDIO_PACKETS = []

def load_audio(blocksize, path):
    '''
    Load audio packets
    '''
    try:
        global AUDIO_TITLES, AUDIO_PACKETS

        AUDIO_PACKETS = P.mount_audio_packets(blocksize, path) 
        L.LOGGER.info("Audios packets loaded")

        AUDIO_TITLES = Utils.get_audio_titles(path)
        L.LOGGER.info("Available audios: %s", AUDIO_TITLES)

    except Exception as e:
        L.LOGGER.error("Error while loading audio packets: %s", str(e))
        raise Exception("Couldn't load audio packets")

def start_streaming():
    '''
    Sends stream packets to clients
    '''
    try:
        audio_title = AUDIO_TITLES[AUDIO_ID]
        L.LOGGER.info("Streaming %s, registered clients are: %s", audio_title, G.CLIENTS)

        packet = AUDIO_PACKETS[AUDIO_ID][1][0]
        NU.send_packet_to_clients(G.NETWORK, G.CLIENTS, packet, stream_packet_sent)
        L.LOGGER.info(f"First audio stream packet sent, interval: {G.INTERVAL / 1e9}s")

        G.NETWORK.set_send_buffer_size(G.BLOCKSIZE)
        L.LOGGER.debug(f"Send buffer size increased to: {G.BLOCKSIZE}")

        for packet in AUDIO_PACKETS[AUDIO_ID][1][1:]:
            G.TIMERS.append(Timer.Timer(G.INTERVAL / 1e9, NU.send_packet_to_clients, (G.NETWORK, G.CLIENTS, packet, stream_packet_sent)))
            stream_packet_sent.wait()
            stream_packet_sent.clear()

        L.LOGGER.info("Finished streaming")
        G.CLOSE_SERVER()

    except Exception as e:
        L.LOGGER.error("Closing server, error while start streaming: %s", str(e))
        G.CLOSE_SERVER()
