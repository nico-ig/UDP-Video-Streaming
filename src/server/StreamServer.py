'''
Deals with the stream management 
Sends stream packets to clients
This should run in a separeted process from the main server
'''

import signal
import struct

from src.server import GlobalStream

from src.network import Network

from src.packets import TypesPackets
from src.packets import UtilsPackets
from src.packets import ServerPackets

from src.utils import Timer
from src.utils import Logger

def new_stream(server, lider):
    '''
    Starts a new stream
    '''
    try:

        Logger.start_logger('stream_server')
        Logger.LOGGER.info("Creating new stream")

        signal.signal(signal.SIGINT, sigint_handler)

        GlobalStream.LIDER = lider

        GlobalStream.NETWORK = Network.Network(server)
        Logger.LOGGER.debug("Network interface created")
        Logger.LOGGER.info("Stream port is: %s", GlobalStream.NETWORK.get_port())

        Logger.LOGGER.debug("Starting port ack received timer")
        GlobalStream.LIDER_TIMER = Timer.Timer(GlobalStream.REGISTRATION_DURATION, sigint_handler)

        send_port_allocated()
        start_registration()

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def send_port_allocated():
    '''
    Send port allocated to lider client
    '''
    try:
        Logger.LOGGER.info("Sending port allocated")
        packet = UtilsPackets.mount_byte_packet(TypesPackets.PORT_ALLOCATED)
        GlobalStream.NETWORK.send(GlobalStream.LIDER, packet)


        if GlobalStream.TIMER is not None:
            GlobalStream.TIMER.stop()

        GlobalStream.TIMER = Timer.Timer(GlobalStream.PORT_ALLOCATED_TIMEOUT, send_port_allocated)
        Logger.LOGGER.debug("Port allocated retransmit timer initiated")

        GlobalStream.NETWORK.register_callback(TypesPackets.PORT_ACK, ServerPackets.parse_port_ack)
        
    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def start_registration():
    '''
    Starts the registration
    '''
    try:
        GlobalStream.TIMER.stop()
        GlobalStream.TIMER = Timer.Timer(GlobalStream.REGISTRATION_DURATION, registration_finished)
        Logger.LOGGER.debug("Registration timer started")

        GlobalStream.NETWORK.register_callback(TypesPackets.REGISTER, new_client)
        Logger.LOGGER.info("Waiting for clients to register")

        while not GlobalStream.START_EVENT.is_set():
            pass

        if len(GlobalStream.CLIENTS) < 1:
            Logger.LOGGER.debug("No clients registered")
            sigint_handler()
            
        Logger.LOGGER.info("Should start streaming, registered clients are: %s", GlobalStream.CLIENTS)

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def new_client(data, source):
    '''
    Deals with new clients wishing to join the stream
    '''
    try:
        if len(data) != 0:
            return

        GlobalStream.CLIENTS.add(source)
        Logger.LOGGER.info("New client %s registered", source)

        packet = UtilsPackets.mount_byte_packet(TypesPackets.REGISTER_ACK)
        packet += struct.pack('Q', GlobalStream.TIMER.remaining_time())
        packet += struct.pack('Q', GlobalStream.INTERVAL)

        Logger.LOGGER.info("Sending register ack to client %s", source)
        GlobalStream.NETWORK.send(source, packet) 

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def registration_finished():
    '''
    Callback funtion to finish the registration
    '''
    try:
        Logger.LOGGER.info("Registration finished")

        GlobalStream.NETWORK.stop()
        GlobalStream.START_EVENT.set()

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def sigint_handler(signum = 0, fram = ''):
    '''
    Callback function to stop the stream when sigint is received
    '''
    try:
        Logger.LOGGER.info("Sigint received")

        if GlobalStream.NETWORK != None:
            GlobalStream.NETWORK.stop()

        if GlobalStream.TIMER != None:
            GlobalStream.TIMER.stop()
 
    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

    finally:
        Logger.LOGGER.info("Exited")
        exit()

def send_packet_to_client(clients, packet):
    '''
    Sends a packet to every client
    '''
    for client in clients:
        try:
            GlobalStream.NETWORK.send(client, packet)

        except Exception as e:
            Logger.LOGGER.error("An error occurred: %s", str(e))

def send_packets_to_clients(clients, packets):
    '''
    Sends all packets to clients (DEBUG ONLY - DELETE LATER)
    '''
    for client in clients:
        for packet in packets:
            try:
                GlobalStream.NETWORK.send(client, packet)
            except Exception as e:
                Logger.LOGGER.error("An error occurred: %s", str(e))
        