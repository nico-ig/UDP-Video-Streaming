import streamHeap

def print_available_musics(music_list):
    print("Available musics:")
    print("ID / Music Name")

def music_choices():
    print("Choose a music ID to play it")
    music_id = input()
    print("You chose music ID: " + music_id)
    return music_id

def add_stream_packet(stream_player, packet):
    key = packet[1]
    data = packet[2]

    stream_player.add_to_stream(key, data)







#### Dont forget to unregister from other packet types no longer relevants