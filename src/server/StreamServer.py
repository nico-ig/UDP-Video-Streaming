'''
Deals with the stream management 
Sends stream packets to clients
This should run in a separeted process from the main server
'''

from ast import Global
import signal

from src.server import GlobalStream
from src.network import Network
from src.packets import TypesPackets
from src.packets import UtilsPackets
from src.utils import Timer
from src.utils import Logger

def new_stream(server, lider):
    '''
    Starts a new stream
    '''
    try:

        GlobalStream.LOGGER = Logger.start_logger()
        GlobalStream.LOGGER = Logger.get_logger('stream-server')
        GlobalStream.LOGGER.info("Creating new stream")

        signal.signal(signal.SIGINT, sigint_handler)

        GlobalStream.LIDER = lider

        GlobalStream.NETWORK = Network.Network(server)
        GlobalStream.LOGGER.info("GlobalStream.NETWORK interface created")

        send_port_allocated()
        start_streaming()

    except Exception as e:
        GlobalStream.LOGGER.error("An error occurred: %s", str(e))

def send_port_allocated():
    '''
    Send port allocated to lider client
    '''
    try:
        if GlobalStream.PORT_ACK_ATTEMPTS > 0:
            GlobalStream.PORT_ACK_ATTEMPTS -= 1

            packet = UtilsPackets.mount_byte_packet(TypesPackets.PORT_ALLOCATED)

            GlobalStream.LOGGER.info("Sending port allocated to lider %s", GlobalStream.LIDER)
            GlobalStream.NETWORK.send(GlobalStream.LIDER, packet)

            if GlobalStream.TIMER == None:
                GlobalStream.NETWORK.register_callback(TypesPackets.PORT_ACK, port_ack_received)
                GlobalStream.NETWORK.register_callback(TypesPackets.REGISTER, new_client)
            else:
                GlobalStream.TIMER.stop()
                
            GlobalStream.TIMER = Timer.Timer(GlobalStream.PORT_ACK_TIMEOUT, send_port_allocated)
            GlobalStream.LOGGER.info("Port ACK timer registerd for lider %s", GlobalStream.LIDER)

        else:
            GlobalStream.LOGGER.info("No more attempts to receive port ack from %s", GlobalStream.LIDER)
            sigint_handler()
            
    except Exception as e:
        GlobalStream.LOGGER.error("An error occurred: %s", str(e))

def port_ack_received(data, source):
    '''
    Deals with port ack incoming packets
    '''
    try:
        if len(data) != 0:
            return

        source_ip, source_port = source
        lider_ip, lider_port = GlobalStream.LIDER

        if source_ip != lider_ip:
            GlobalStream.LOGGER.info("Port ACK send by %s and not %s", source, GlobalStream.LIDER)
            return

        GlobalStream.TIMER.stop()
        GlobalStream.NETWORK.unregister_callback(TypesPackets.PORT_ACK)

        GlobalStream.TIMER = Timer.Timer(GlobalStream.REGISTRATION_DURATION, registration_finished)
        GlobalStream.LOGGER.info("Registration timer registered for lider %s", GlobalStream.LIDER)

    except Exception as e:
        GlobalStream.LOGGER.error("An error occurred: %s", str(e))

def new_client(data, source):
    '''
    Deals with new clients wishing to join the stream
    '''
    try:
        if len(data) != 0:
            return

        GlobalStream.CLIENTS.add(source)
        GlobalStream.LOGGER.info("New client %s registerd", source)

        packet = UtilsPackets.mount_byte_packet(TypesPackets.REGISTER_ACK)

        GlobalStream.LOGGER.info("Sending register ack to client %s", source)
        GlobalStream.NETWORK.send(source, packet) 

    except Exception as e:
        GlobalStream.LOGGER.error("An error occurred: %s", str(e))

def registration_finished(self_timer=''):
    '''
    Callback funtion to finish the registration
    '''
    try:
        GlobalStream.LOGGER.info("Registration finished")

        GlobalStream.NETWORK.stop()
        GlobalStream.START_EVENT.set()

    except Exception as e:
        GlobalStream.LOGGER.error("An error occurred: %s", str(e))

def start_streaming():
    '''
    Starts the stream
    '''
    try:
        while not GlobalStream.START_EVENT.is_set():
            pass

        if len(GlobalStream.CLIENTS) < 1:
            GlobalStream.LOGGER.info("No client registered for stream")
            sigint_handler()
            
        GlobalStream.LOGGER.info("Should start streaming, registered clients are: %s", GlobalStream.CLIENTS)
        GlobalStream.TIMER.stop()

    except Exception as e:
        GlobalStream.LOGGER.error("An error occurred: %s", str(e))

def sigint_handler(self_watchdog=''):
    """
    Callback function to stop the stream when sigint is received
    """
    try:
        if GlobalStream.NETWORK != None:
            GlobalStream.NETWORK.stop()

        if GlobalStream.TIMER != None:
            GlobalStream.TIMER.stop()
 
    except Exception as e:
        GlobalStream.LOGGER.error("An error occurred: %s", str(e))

def send_packet_to_client(clients, packet):
    '''
    Sends a packet to every client
    '''
    for client in clients:
        try:
            GlobalStream.NETWORK.send(client, packet)

        except Exception as e:
            GlobalStream.LOGGER.error("An error occurred: %s", str(e))

def send_packets_to_clients(clients, packets):
    '''
    Sends all packets to clients (DEBUG ONLY - DELETE LATER)
    '''
    for client in clients:
        for packet in packets:
            try:
                GlobalStream.NETWORK.send(client, packet)
            except Exception as e:
                GlobalStream.LOGGER.error("An error occurred: %s", str(e))
        