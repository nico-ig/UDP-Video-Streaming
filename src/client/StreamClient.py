import threading

from src.packets import TypesPackets
from src.packets import ClientPackets

from src.client import GlobalClient

from src.utils import Timer
from src.utils import Logger

#### Dont forget to unregister from other packet types no longer relevants

def listen_to_stream():
    GlobalClient.SERVER_TIMER = Timer.Timer(GlobalClient.STREAM_TIMEOUT, GlobalClient.CLOSE_CLIENT)
    Logger.LOGGER.debug("Stream packets timer initiated")

    GlobalClient.NETWORK.register_callback(TypesPackets.STREAM, ClientPackets.parse_stream_packet)
    