'''
Deals with the parsing of the packets in the client (incoming and outgoing)
'''

from ast import Global
import threading
import struct

from src.utils import Utils
from src.utils import Logger

from src.client import GlobalClient

from src.packets import TypesPackets

list_received = threading.Event()

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

        if GlobalClient.AUDIO_ID < 0:
            Logger.LOGGER.debug("Waiting for audio to be chosen")
            GlobalClient.AUDIO_CHOSEN.wait()

        Logger.LOGGER.info("Sending port ack")
        packet = mount_port_ack_packet()
        GlobalClient.NETWORK.send(GlobalClient.SERVER, packet, GlobalClient.IPV4)

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))
        
def parse_audios(payload):
    GlobalClient.AUDIO_TITLES = []

    cnt = struct.unpack('Q', payload[:8])[0]
    payload = payload[8:]

    for i in range(0, cnt):
        title, payload = Utils.deserialize_str(payload)
        GlobalClient.AUDIO_TITLES.append(title)
        
    if payload != b'':
        raise Exception(f'Audio title packet is not valid')

def mount_port_ack_packet():
    return bytes([TypesPackets.PORT_ACK]) + struct.pack('Q', GlobalClient.AUDIO_ID)

def parse_register_ack(payload, source):
    '''
    Parse the register ack packet 
    '''
    try:
        if len(payload) != 2 or not Utils.is_same_address(GlobalClient.SERVER, source, GlobalClient.IPV4):
            pass
            
        Logger.LOGGER.debug("Received register ack from %s", source)
       
        GlobalClient.REGISTER_DURATION = struct.unpack('Q', payload[:8])[0] / 1e9
        
        interval = struct.unpack('Q', payload[8:])[0] / 1e9
        GlobalClient.STREAM_TIMEOUT *= interval

        GlobalClient.REGISTER_ACK.set()
        
    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def parse_audio_config(payload, source):
    '''
    Parse the configs for selected audio
    '''
    try:
        if not Utils.is_same_address(GlobalClient.SERVER, source, GlobalClient.IPV4):
            return

        GlobalClient.AUDIO_TITLE, payload = Utils.deserialize_str(payload)

        if len(payload) != 24:
            GlobalClient.AUDIO_TITLE = ''
            return

        GlobalClient.AUDIO_SAMPLERATE = struct.unpack('Q', payload[:8])[0]
        GlobalClient.AUDIO_CHANNELS = struct.unpack('Q', payload[8:16])[0]
        GlobalClient.AUDIO_BLOCKSIZE = struct.unpack('Q', payload[16:])[0]

        # Changes the buffer size for incoming packets so audio stream packets can be received
        if GlobalClient.NETWORK.get_buffer_size() <= GlobalClient.AUDIO_BLOCKSIZE + 9:
            GlobalClient.NETWORK.set_buffer_size(GlobalClient.AUDIO_BLOCKSIZE + 10)

        GlobalClient.AUDIO_CONFIG.set()

        Logger.LOGGER.info("Sending audio config ack")
        packet = bytes([TypesPackets.AUDIO_CONFIG_ACK])
        GlobalClient.NETWORK.send(GlobalClient.SERVER, packet, GlobalClient.IPV4)

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def parse_stream_packets(payload, source):
    '''
    Add a packet to the stream buffer
    '''
    try:
        if not Utils.is_same_address(GlobalClient.SERVER, source, GlobalClient.IPV4):
            return

        if len(payload) < 9:
            return

        seq = struct.unpack('Q', payload[:8])[0]
        GlobalClient.AUDIO_BUFFER.add_to_buffer(seq, payload[8:])

        GlobalClient.STREAM_STARTED.set()

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))