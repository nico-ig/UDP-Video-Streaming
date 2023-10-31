# Deals with the parsing of the packets (incoming and outgoing)

from src.client import ClientGlobals

def parse_stream_packet(data, source):
    if source != server:
        return
    
    key = data[1]
    data = data[2]

    return key, data

def parse_music_list(packet):
    music_list = []

    while packet != []:
        id = packet[0]
        packet = packet[1:]
        tam = packet[0]
        packet = packet[1:]
        nome = packet[:tam]
        CLientGlobals.music_list.append(id[0], nome[0])
        
    list_received.set()
