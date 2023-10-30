from http import server
import streamHeap
import Network
import TypesPackets
import threading
import GlobalServer

list_received = threading.Event()

def music_choices():
    print("Choose a music ID to play it")
    music_id = input()
    print("You chose music ID: " + music_id)
    return music_id

def add_stream_packet(data, source):
    if source != server:
        return
    
    key = data[1]
    data = data[2]

    GlobalServer.stream.add_to_stream(key, data)


# def start_listening_stream():
#     network.register_callback(STREAM_PACKET, add_stream_packet)
#     play_heap()
    
def print_available_musics(packet):
    music_list = parse_music_list(packet)
    print("Available musics:")
    print("ID / Music Name")
    for id, nome in music_list:
        print(id + " / " + nome)

def parse_music_list(packet):
    music_list = []

    while packet != []:
        id = packet[0]
        packet = packet[1:]
        tam = packet[0]
        packet = packet[1:]
        nome = packet[:tam]
        music_list.append(id[0], nome[0])
        
    list_received.set()
    return music_list


def music_list(packet):
    Network.register_callback(TypesPackets.MUSIC_LIST, parse_music_list)
    
    while not list_received.is_set():
        pass
    
    print_available_musics(packet)

def music_choices():
    print("Choose a music ID to play it")
    music_id = input()
    print("You chose music ID: " + music_id)
    return music_id

def music_request():
    Network.register_callback(TypesPackets.MUSIC_REQUEST, send_music_request)
    music_id = music_choices()
    Network.send(server, TypesPackets.MUSIC_REQUEST, music_id)


#### Dont forget to unregister from other packet types no longer relevants