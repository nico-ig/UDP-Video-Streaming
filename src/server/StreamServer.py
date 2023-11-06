'''
Deals with the stream management 
Sends stream packets to clients
This should run in a separeted process from the main server
'''

import signal
import threading

from src.utils import Timer
from src.utils import Logger

from src.network import Network

from src.server import GlobalStream

from src.packets import TypesPackets
from src.packets import ServerPackets

stream_packet_sent = threading.Event()

def new_stream(server, lider, ipv4, audio_titles, audio_packets):
    '''
    Starts a new stream
    '''
    try:
        Logger.start_logger('stream_server')
        Logger.set_logger('stream_server')
        Logger.LOGGER.info("Creating new stream")

        signal.signal(signal.SIGINT, sigint_handler)

        GlobalStream.LIDER = lider
        GlobalStream.IPV4 = ipv4

        GlobalStream.NETWORK = Network.Network(GlobalStream.IPV4, server)
        Logger.LOGGER.debug("Network interface created")
        Logger.LOGGER.info("Stream port is: %s", GlobalStream.NETWORK.get_port())

        GlobalStream.NETWORK.register_callback(TypesPackets.PORT_ACK, ServerPackets.parse_port_ack)
        GlobalStream.LIDER_TIMER = Timer.Timer(GlobalStream.REGISTRATION_DURATION, sigint_handler)
        Logger.LOGGER.debug("Port ack received timer started")
        
        GlobalStream.AUDIO_TITLES = audio_titles
        GlobalStream.AUDIO_PACKETS = audio_packets

        GlobalStream.NETWORK.register_callback(TypesPackets.AUDIO_CONFIG_ACK, ServerPackets.parse_audio_config_ack)

        send_port_allocated()
        start_registration()

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def send_port_allocated():
    '''
    Send port allocated to lider client. After receiving ack, send audio config to clients
    '''
    try:
        if GlobalStream.START_EVENT.is_set() or GlobalStream.STOP_EVENT.is_set():
            return

        if GlobalStream.PORT_ACK_RECEIVED.is_set():
            send_audio_config()            
            return
        
        Logger.LOGGER.info("Sending port allocated")
        packet = ServerPackets.mount_port_allocated_packet()
        GlobalStream.NETWORK.send(GlobalStream.LIDER, packet, GlobalStream.IPV4)

        Timer.Timer(GlobalStream.RETRANSMIT_TIMEOUT, send_port_allocated)
        Logger.LOGGER.debug("Port allocated retransmit timer initiated")

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def start_registration():
    '''
    Starts the registration
    '''
    try:
        GlobalStream.TIMER = Timer.Timer(GlobalStream.REGISTRATION_DURATION, registration_finished)
        Logger.LOGGER.debug("Registration timer started")

        GlobalStream.NETWORK.register_callback(TypesPackets.REGISTER, ServerPackets.parse_new_registration)
        Logger.LOGGER.info("Waiting for clients to register")

        GlobalStream.START_EVENT.wait()
        if GlobalStream.STOP_EVENT.is_set():
            return

        GlobalStream.NETWORK.unregister_callback(TypesPackets.REGISTER)

        start_streaming()

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def start_streaming():
    '''
    Sends stream packets to clients
    '''

    if not GlobalStream.CLIENTS:
        Logger.LOGGER.info("No clients registered")
        sigint_handler()
        return
            
    audio_title = GlobalStream.AUDIO_TITLES[GlobalStream.AUDIO_ID]
    Logger.LOGGER.info("Streaming %s, registered clients are: %s", audio_title, GlobalStream.CLIENTS)

    packet = GlobalStream.AUDIO_PACKETS[GlobalStream.AUDIO_ID][1][0]
    send_packet_to_clients(GlobalStream.CLIENTS, packet, stream_packet_sent)
    Timer.Timer(GlobalStream.INTERVAL / 1e9, send_packet_to_clients, (GlobalStream.CLIENTS, packet, stream_packet_sent))
    Logger.LOGGER.debug(f"First audio stream packet sent, interval: {GlobalStream.INTERVAL / 1e9}s")

    for packet in GlobalStream.AUDIO_PACKETS[GlobalStream.AUDIO_ID][1][1:]:
        stream_packet_sent.wait()
        stream_packet_sent.clear()

        Timer.Timer(GlobalStream.INTERVAL / 1e9, send_packet_to_clients, (GlobalStream.CLIENTS, packet, stream_packet_sent))

    Logger.LOGGER.info("Finished streaming")

def send_audio_config():
    '''
    Sends the audio config to clients, packet needs to be confirmed by client
    '''
    if GlobalStream.STOP_EVENT.is_set():
        return

    if GlobalStream.START_EVENT.is_set():
        GlobalStream.CLIENTS = []
        GlobalStream.CLIENTS = GlobalStream.CONFIRMED_CLIENTS
        return
        
    config_packet = GlobalStream.AUDIO_PACKETS[GlobalStream.AUDIO_ID][0]

    clients_not_confirmed = list(GlobalStream.CLIENTS - GlobalStream.CONFIRMED_CLIENTS)

    if len(clients_not_confirmed) > 0:
        Logger.LOGGER.info("Sending audio config to clients: %s", clients_not_confirmed)
        send_packet_to_clients(clients_not_confirmed, config_packet)
        Logger.LOGGER.debug("Audio config retransmit timer will be initiated")

    Timer.Timer(GlobalStream.RETRANSMIT_TIMEOUT, send_audio_config)

def registration_finished():
    '''
    Callback funtion to finish the registration
    '''
    try:
        Logger.LOGGER.info("Registration finished")
        GlobalStream.START_EVENT.set()

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def send_packet_to_clients(clients, packet, event=None):
    '''
    Sends a packet to every client
    '''
    try:
        for client in clients:
            GlobalStream.NETWORK.send(client, packet, GlobalStream.IPV4)

        if event != None:
            event.set()

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def sigint_handler(signum = 0, fram = ''):
    '''
    Callback function to stop the stream when sigint is received
    '''
    try:
        Logger.LOGGER.info("Sigint received")

        GlobalStream.STOP_EVENT.set()
        GlobalStream.START_EVENT.set()

        if GlobalStream.NETWORK != None:
            GlobalStream.NETWORK.stop()

        if GlobalStream.TIMER != None:
            GlobalStream.TIMER.stop()
 
    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

    finally:
        Logger.LOGGER.info("Exitting")
