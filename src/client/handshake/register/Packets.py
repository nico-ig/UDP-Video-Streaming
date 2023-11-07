'''
Packets for registration
'''

import struct
import threading

from src.utils import Logger as L
from src.client import Globals as G
from src.network import Utils as NU
from src.client.stream import Stream as S

REGISTER_DURATION = 0
AUDIO_CONFIG = threading.Event()
REGISTER_ACK = threading.Event()

G.STOP_EVENTS.append(AUDIO_CONFIG)
G.STOP_EVENTS.append(REGISTER_ACK)

def parse_register_ack(payload, source):
    '''
    Parse the register ack packet 
    '''
    try:
        if len(payload) != 2 or not NU.is_same_address(NU.SERVER, source):
            pass
            
        L.LOGGER.debug("Received register ack from %s", source)
       
        global REGISTER_DURATION
        REGISTER_DURATION = struct.unpack('Q', payload[:8])[0] / 1e9
        
        interval = struct.unpack('Q', payload[8:])[0] / 1e9
        G.STREAM_TIMEOUT *= interval

        REGISTER_ACK.set()
        
    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))

def parse_audio_config(payload, source):
    '''
    Parse the configs for selected audio
    '''
    try:
        if not NU.is_same_address(G.SERVER, source):
            return

        S.AUDIO_TITLE, payload = NU.deserialize_str(payload)

        if len(payload) != 24:
            S.AUDIO_TITLE = ''
            return

        S.AUDIO_SAMPLERATE = struct.unpack('Q', payload[:8])[0]
        S.AUDIO_CHANNELS = struct.unpack('Q', payload[8:16])[0]
        S.AUDIO_BLOCKSIZE = struct.unpack('Q', payload[16:])[0]

        # Changes the buffer size for incoming packets so audio stream packets can be received
        if G.NETWORK.get_buffer_size() <= S.AUDIO_BLOCKSIZE + 9:
            G.NETWORK.set_buffer_size(S.AUDIO_BLOCKSIZE + 10)

        AUDIO_CONFIG.set()

        L.LOGGER.info("Sending audio config ack")
        packet = bytes([NU.AUDIO_CONFIG_ACK])
        G.NETWORK.send(G.SERVER, packet)

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))