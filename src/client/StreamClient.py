import threading

from src.packets import TypesPackets
from src.packets import ClientPackets

from src.client import GlobalClient

from src.utils import Timer
from src.utils import Logger

#### Dont forget to unregister from other packet types no longer relevants

def listen_to_stream():
    Logger.LOGGER.info("Waiting for audio config to start listening to stream")
    GlobalClient.AUDIO_CONFIG.wait()
    
    GlobalClient.NETWORK.register_callback(TypesPackets.STREAM, ClientPackets.parse_stream_packets)
    