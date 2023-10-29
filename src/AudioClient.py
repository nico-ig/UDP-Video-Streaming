import streamHeap as sh

stream = sh.stream_player

def add_packet_to_heap(packet):
    stream.add_to_stream(packet[0], packet[1])