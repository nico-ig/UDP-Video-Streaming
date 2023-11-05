'''
Deals with the parsing of the packets in the client (incoming and outgoing)
'''

import threading
import struct

from src.utils import Utils
from src.utils import Logger

from src.client import GlobalClient

from src.packets import TypesPackets

list_received = threading.Event()

def parse_stream_packet(data, source):
    if source != GlobalClient.SERVER:
        return
    
    key = data[1]
    data = data[2]

    return key, data

def parse_port_allocated(payload, source):
    '''
    Parse the payload in a port allocated packet    
    '''
    try:
        server_ip, server_port = GlobalClient.SERVER
        source_ip, source_port = source

        if not Utils.is_same_ip(server_ip, source_ip, GlobalClient.IPV4):
            return
        
        parse_audios(payload)

        Logger.LOGGER.debug("Received port allocated from %s", source)

        GlobalClient.SERVER = source
        GlobalClient.PORT_ALLOCATED.set()

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))
        
def parse_audios(payload):
    GlobalClient.AUDIOS = []

    cnt = struct.unpack('Q', payload[:8])[0]
    payload = payload[8:]

    for i in range(0, cnt):
        title, payload = Utils.deserialize_str(payload)
        GlobalClient.AUDIOS.append(title)
        
    if payload != b'':
        raise Exception(f'Audio title packet is not valid')

def mount_port_ack_packet():
    return bytes([TypesPackets.PORT_ACK]) + struct.pack('Q', GlobalClient.AUDIO_ID)

def parse_register_ack(payload, source):
    '''
    Parse the register ack packet 
    '''
    try:
        if len(payload) != 2 or not Utils.is_same_address(GlobalClient.SERVER, source):
            pass
            
        Logger.LOGGER.debug("Received register ack from %s", source)
       
        GlobalClient.REGISTER_DURATION = struct.unpack('Q', payload[:8])[0] / 1e9
        
        interval = struct.unpack('Q', payload[8:])[0] / 1e9
        GlobalClient.STREAM_TIMEOUT *= interval

        GlobalClient.REGISTER_ACK.set()
        
    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))