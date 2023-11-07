
'''
Receives the request for new streams
'''

import struct
import signal
import threading
import multiprocessing

from src.utils import Timer
from src.network import Network
from src.utils import Logger as L
from src.server import Globals as G
from src.network import Utils as NU
from src.server.stream import Stream as S
from src.server.handshake.register import Register as R

lider = ()
audio_ack = threading.Event()
G.TIMERS.append(audio_ack)

def open_new_stream(client):
    '''
    Starts a new process to deal with the client stream
    '''
    try:
        if G.STOP_EVENT.is_set():
            return

        if client in G.CHILDREN.values():
            L.LOGGER.info("Terminating process for client %s", client)
            G.CHILDREN[client].terminate()
            G.CHILDREN[client].join()

        L.LOGGER.info("Starting a new process for client %s", client)
        G.CHILDREN[client] = multiprocessing.Process(target=new_stream, args=(G.SERVER_NAME, client, NU.IPV4, S.AUDIO_TITLES, S.AUDIO_PACKETS))
        G.CHILDREN[client].start()

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))
        raise Exception("Error starting new stream")

def new_stream(server, lider_in, ipv4, audio_titles, audio_packets):
    '''
    Starts a new stream
    '''
    try:
        L.start_logger('stream_server')
        L.set_logger('stream_server')
        L.LOGGER.info("Creating new stream")

        signal.signal(signal.SIGINT, G.CLOSE_SERVER)

        global lider
        lider = lider_in

        G.NETWORK = Network.Network(ipv4, server)
        L.LOGGER.debug("Network interface created")
        L.LOGGER.info("Stream port is: %s", G.NETWORK.get_port())

        S.AUDIO_TITLES = audio_titles
        S.AUDIO_PACKETS = audio_packets

        send_stream_opened()
        wait_audio_ack()
        R.start_registration()

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))
        L.LOGGER.error("Couldn't start new stream")
        G.CLOSE_SERVER()

def send_stream_opened():
    '''
    Send port allocated to lider client. After receiving ack, send audio config to clients
    '''
    try:
        if audio_ack.is_set() or G.STOP_EVENT.is_set():
            return
        
        L.LOGGER.info("Sending stream oppened")
        packet = mount_stream_opened_packet()
        G.NETWORK.send(lider, packet)

        G.TIMER = Timer.Timer(G.RETRANSMIT_TIMEOUT, send_stream_opened)
        L.LOGGER.debug("Stream opened retransmit timer initiated")

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))
        send_stream_opened()

def wait_audio_ack():
    '''
    Waits for lider client to send the audio choice
    '''
    try:
        G.NETWORK.register_callback(NU.AUDIO_ACK, parse_audio_ack)
        G.TIMER = Timer.Timer(G.REGISTRATION_DURATION, R.registration_finished)
        L.LOGGER.debug("Registration timer started")
            
        audio_ack.wait()
        G.NETWORK.unregister_callback(NU.AUDIO_ACK)
        return

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))
        raise Exception("Error while waiting for audio ack")

def mount_stream_opened_packet():
    '''
    Mount the packet with the avaiable audios
    '''
    try:
        packet = bytes([NU.STREAM_OPENED])

        packet += struct.pack('Q', len(S.AUDIO_TITLES))
        for title in S.AUDIO_TITLES:
            packet += NU.serialize_str(title)
        
        return packet

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))
        raise Exception("Error mounting stream opened packet")

def parse_audio_ack(payload, source):
    '''
    Deals with audio ack packets
    '''
    try:
        if len(payload) != 8:
            return

        source_ip = source[0]
        lider_ip = lider[0]

        if source_ip != lider_ip:
            L.LOGGER.debug("Port ACK send by %s and not %s", source, lider)
            return

        L.LOGGER.info("Port ack received")
        S.AUDIO_ID = struct.unpack('Q', payload)[0]
        audio_ack.set()

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))
