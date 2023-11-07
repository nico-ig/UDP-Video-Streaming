'''
Packets for open stream
'''

import sys
import select
import struct
import threading

from src.utils import Logger as L
from src.network import Utils as NU
from src.client import Globals as G

audio_id = -1
STREAM_OPENED = threading.Event()
G.STOP_EVENTS.append(STREAM_OPENED)

def parse_stream_opened(payload, source):
    '''
    Parse the payload in stream opened packet and sends the ack
    '''
    try:
        server_ip = G.SERVER[0]
        source_ip = source[0]

        if not NU.is_same_ip(server_ip, source_ip):
            return
        
        L.LOGGER.debug("Received port allocated from %s", source)
        G.SERVER = source

        audio_titles = parse_audios(payload)
        get_audio_choice(audio_titles)

        STREAM_OPENED.set()

        packet = bytes([NU.AUDIO_ACK]) + struct.pack('Q', audio_id)
        G.NETWORK.send(G.SERVER, packet)
        L.LOGGER.info("Stream ack sent")

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))
        raise Exception(f'Error parsing stream opened packet')
        
def parse_audios(payload):
    '''
    Parse the audio info in the payload
    '''
    try:
        audio_titles = []

        cnt = struct.unpack('Q', payload[:8])[0]
        payload = payload[8:]

        for i in range(0, cnt):
            title, payload = NU.deserialize_str(payload)
            audio_titles.append(title)
            
        if payload != b'':
            L.LOGGER(f'An error occurred: Audio title packet is not valid')
            raise Exception(f'Error parsing audios')

        return audio_titles

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))
        raise Exception(f'Error parsing audios')

def get_audio_choice(audio_titles):
    '''
    Get the audio id that should be requested
    '''
    try:
        global audio_id

        if audio_id >= 0:
            return

        L.LOGGER.info("Available audios are: %s", audio_titles)

        print("Choose an audio ID to play it")
        print_available_audios(audio_titles)

        input_list = select.select([sys.stdin], [], [], G.AUDIO_CHOICE_TIMEOUT)[0]
        if input_list:
            audio_id = int(sys.stdin.readline().strip())
            print("You chose audio ID: " + str(audio_id))

        else:
            audio_id = 0
            print("Timeout, using default audio ID: " + str(audio_id))

        if audio_id >= len(audio_titles):
            audio_id = 0
            print("Invalid value, using default ID: " + str(audio_id))
            
        L.LOGGER.info(f'Requested audio id: {audio_id}')

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))
        raise Exception(f'Error getting audio choice')

def print_available_audios(audio_titles):
    '''
    Print title list received from server
    '''
    try:
        print("Available audios:")
        print("ID / Audio Title")
        for i in range(0, len(audio_titles)):
            print(str(i) + " / " + audio_titles[i])

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))
        raise Exception(f'Error printing available audios')