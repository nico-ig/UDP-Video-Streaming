from http import server
import streamHeap

def print_available_musics(music_list):
    print("Available musics:")
    print("ID / Music Name")

def music_choices():
    print("Choose a music ID to play it")
    music_id = input()
    print("You chose music ID: " + music_id)
    return music_id

def add_stream_packet(data, source):
    if source != server:
        return
    
    key = packet[1]
    data = packet[2]

    stream_player.add_to_stream(key, data)


def start_listening_stream():
    network.register_callback(STREAM_PACKET, add_stream_packet)
    play_heap()
    

0x5 0x00 0x00 0x00 0x00 0x00 0x2 0x1 0x0

id[0] = packet[0]
packet = packet[1:]
tam = packet[0]
packet = packet[1:]
nome[0] = packet[:tam]
music[0] = (id[0], name[0])

list_received = threading.Event()

def parse:
    //parse pra music_list
    list_received.set()

def musicListFuntion:
    register_callback(parse)
    
    while not list_received.is_set():
        pass
    
    print_music_list()


#### Dont forget to unregister from other packet types no longer relevants