'''
Deals with the parsing of the packets in the client (incoming and outgoing)
'''

import threading
import struct

from src.utils import Utils
from src.client import GlobalClient

list_received = threading.Event()

def parse_stream_packet(data, source):
    if source != GlobalClient.SERVER:
        return
    
    key = data[1]
    data = data[2]

    return key, data

def parse_music_list(packet, source):
    music_list = []

    while packet != []:
        id = packet[0]
        packet = packet[1:]
        tam = packet[0]
        packet = packet[1:]
        nome = packet[:tam]
        GlobalClient.music_list.append(id[0], nome[0])
   # Eu colocaria o kick na funcao que ta esperando o list_received ser setado 
    GlobalClient.SERVER_TIMER.kick()
    list_received.set()

def parse_port_allocated(payload, source):
    '''
    Parse the payload in a port allocated packet    
    '''
    try:
        if len(payload) != 0:
            return
        
        server_ip, server_port = GlobalClient.SERVER
        source_ip, source_port = source

        if not Utils.is_same_ip(server_ip, source_ip):
            return
        
        GlobalClient.LOGGER.debug("Received port allocated from %s", source)

        GlobalClient.SERVER = source
        GlobalClient.PORT_ALLOCATED.set()

    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))
        
def parse_register_ack(payload, source):
    '''
    Parse the register ack packet 
    '''
    try:
        if len(payload) != 2 or not Utils.is_same_address(GlobalClient.SERVER, source):
            pass
            
        GlobalClient.LOGGER.debug("Received register ack from %s", source)
       
        GlobalClient.REGISTER_DURATION = struct.unpack('Q', payload[:8])[0] / 1e9
        
        interval = struct.unpack('Q', payload[8:])[0] / 1e9
        GlobalClient.STREAM_TIMEOUT *= interval

        GlobalClient.REGISTER_ACK.set()
        
    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))