import threading

from src.network import Network
from src.packets import TypesPackets
from src.packets import ClientPackets

from src.server import GlobalServer
from src.client import GlobalClient

from src.utils import Timer
from src.utils import Logger

def add_stream(data, source):
# Parar esse timer quando receber o primeiro pacote de stream, e não quando entrar nessa função, ou algo assim
# Quando a stream começar também desrregistrar o port_allocated
    GlobalClient.TIMER.stop()
    Logger.LOGGER.info("Registration timer stopped")
    GlobalClient.SERVER_TIMER = Timer.Timer(GlobalClient.STREAM_TIMEOUT, GlobalClient.SIGINT_HANDLER)
    Logger.LOGGER.debug("Stream packets timer initiated")
# Iniciar e depois śó chutar

    key, stream = ClientPackets.parse_stream_packet(data, source)
    GlobalServer.stream.add_to_stream(key, stream)


def listen_to_stream():
    GlobalClient.NETWORK.register_callback(TypesPackets.STREAM_PACKET, add_stream)

    # play_heap()
    
# def music_request():
#     Network.register_callback(TypesPackets.MUSIC_REQUEST, start_streaming)
#     music_id = music_choices()
#     Network.send(server, TypesPackets.MUSIC_REQUEST, music_id, GlobalClient.IPV4)


#### Dont forget to unregister from other packet types no longer relevants