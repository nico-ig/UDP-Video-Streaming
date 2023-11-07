'''
Deals with clients registration to stream
'''
import struct

from src.utils import Timer
from src.utils import Logger as L
from src.network import Utils as NU
from src.server import Globals as G
from src.server.stream import Stream as S

confirmed_clients = set()

def start_registration():
    '''
    Starts the registration
    '''
    try:
        L.LOGGER.info("Registration started")
        G.NETWORK.register_callback(NU.REGISTER, parse_new_registration)

        send_audio_config()
        G.NETWORK.register_callback(NU.AUDIO_CONFIG_ACK, parse_audio_config_ack)

        if G.STOP_EVENT.is_set():
            return

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))
        raise Exception("Couldn't register clients")

def parse_new_registration(data, source):
    '''
    Parse the packet for a new register from clients
    '''
    try:
        if len(data) != 0:
            return

        G.CLIENTS.add(source)
        L.LOGGER.info("New client %s registered", source)

        packet = bytes([NU.REGISTER_ACK])
        packet += struct.pack('Q', G.TIMER.remaining_time())
        packet += struct.pack('Q', G.INTERVAL)

        G.NETWORK.send(source, packet) 
        L.LOGGER.info("Register ack sent to client %s", source)

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))

def send_audio_config():
    '''
    Sends the audio config to clients, packet needs to be confirmed by client
    '''
    try:
        if G.STOP_EVENT.is_set():
            return

        config_packet = S.AUDIO_PACKETS[S.AUDIO_ID][0]

        clients_not_confirmed = list(G.CLIENTS - confirmed_clients)

        if len(clients_not_confirmed) > 0:
            L.LOGGER.info("Sending audio config to clients: %s", clients_not_confirmed)
            NU.send_packet_to_clients(G.NETWORK, clients_not_confirmed, config_packet)
            L.LOGGER.debug("Audio config retransmit timer will be initiated")

        Timer.Timer(G.RETRANSMIT_TIMEOUT, send_audio_config)

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))
        send_audio_config()

def parse_audio_config_ack(payload, source):
    '''
    Parse audio config ack from registered clients
    '''
    try:
        if len(payload) != 0 or not source in G.CLIENTS:
            return

        confirmed_clients.add(source)

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))

def registration_finished():
    '''
    Deals with the end of registration timer
    '''
    try:
        G.CLIENTS = []
        G.CLIENTS = confirmed_clients

        if not G.CLIENTS:
            L.LOGGER.info("No clients registered")
            G.CLOSE_SERVER()
                    
        G.NETWORK.unregister_callback(NU.REGISTER)
        G.NETWORK.unregister_callback(NU.AUDIO_CONFIG_ACK)

        S.start_streaming()

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))