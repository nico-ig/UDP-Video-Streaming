from http import server
import threading
from src.packets import ClientPackets
from src.utils import StreamHeap
from src.network import Network
from src.packets import TypesPackets
from src.server import GlobalServer
from src.client import GlobalClient

list_received = threading.Event()

def music_choices():
    print("Choose a music ID to play it")
    music_id = input()
    print("You chose music ID: " + music_id)
    return music_id

def add_stream(data, source):
    key, stream = ClientPackets.parse_stream_packet(data, source)
    GlobalServer.stream.add_to_stream(key, stream)


def start_listening_stream():
    Network.register_callback(TypesPackets.STREAM_PACKET, ClientPackets.add_stream_packet)
    # play_heap()
    
def print_available_musics(packet):
    music_list = ClientPackets.parse_music_list(packet)
    print("Available musics:")
    print("ID / Music Name")
    for id, nome in GlobalClient.music_list:
        print(id + " / " + nome)

def music_list(packet):
    Network.register_callback(TypesPackets.MUSIC_LIST, ClientPackets.parse_music_list)
    
    while not list_received.is_set():
        pass
    
    music_choices()

def music_choices():
    print("Choose a music ID to play it")
    print_available_musics()
    music_id = input()
    ## Verificar se o id é válido
    print("You chose music ID: " + music_id)
    return music_id

# def music_request():
#     Network.register_callback(TypesPackets.MUSIC_REQUEST, start_streaming)
#     music_id = music_choices()
#     Network.send(server, TypesPackets.MUSIC_REQUEST, music_id)


#### Dont forget to unregister from other packet types no longer relevants