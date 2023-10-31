"""
Manages the handshake with the server
"""

from http import server
from src.packets import UtilsPackets
from src.packets import TypesPackets
from src.packets import ClientPackets
from src.client import GlobalClient
from src.client import StreamClient
from src.utils import Timer

register_send = False

def client_handshake(option):
    """
    Perform the handshake with the server
    """
    try:
        if option == 'join':
            GlobalClient.LOGGER.info("Joining stream at %s", GlobalClient.SERVER)
            send_registration_packet(GlobalClient.SERVER)

        else:
            GlobalClient.LOGGER.info("Entering new stream")
            send_port_request()

    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))

def send_port_request(self_timer=''):
    """
    Send the request for a stream port at the server
    """
    try:
        packet = UtilsPackets.mount_byte_packet(TypesPackets.NEW_PORT_REQUEST)

        GlobalClient.LOGGER.info("Sending new port request to %s", GlobalClient.SERVER)
        GlobalClient.NETWORK.send(GlobalClient.SERVER, packet)

        GlobalClient.TIMER = Timer.Timer(GlobalClient.NEW_PORT_REQUEST_TIMEOUT, send_port_request)
        GlobalClient.TIMER.kick()

        GlobalClient.NETWORK.register_callback(
            TypesPackets.PORT_ALLOCATED, ClientPacket.parse_port_allocated)

    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))

def port_allocated():
    '''
    Deals with the port allocated packet from server. Answer with an port ack
    '''
    try:
        GlobalClient.LOGGER.info("Received port allocated from %s", source)

        GlobalClient.SERVER = source

        GlobalClient.SERVER_TIMER.kick()
        GlobalClient.TIMER.stop()

        packet = UtilsPackets.mount_byte_packet(TypesPackets.PORT_ACK)

        GlobalClient.LOGGER.info("Sending port ack to %s", GlobalClient.SERVER)
        GlobalClient.NETWORK.send(GlobalClient.SERVER, packet)

        global register_send

        if not register_send:
            register_send = True
            send_registration_packet()

    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))

def send_registration_packet():
    '''
    Send to server a request to register at a stream
    ''' 
    try:
        packet = UtilsPackets.mount_byte_packet(TypesPackets.REGISTER)

        GlobalClient.LOGGER.info("Sending registration to %s", GlobalClient.SERVER)
        GlobalClient.NETWORK.send(GlobalClient.SERVER, packet)
    
        GlobalClient.TIMER = Timer.Timer(GlobalClient.REQUEST_ACK_TIMEOUT, send_registration_packet)
        GlobalClient.TIMER.kick()

        GlobalClient.NETWORK.register_callbask(TypesPackets.REGISTER_ACK, ClientPackets.parse_register_ack)

    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))

def register_ack_received():
    '''
    Prepare the client to start listening to the stream
    '''
    try:
        while not GlobalClient.REGISTER_ACK.is_set():
            pass
    
        
        GlobalClient.LOGGER.info("Register ack received")
        GlobalClient.unregister_callback(TypesPackets.REGISTER_ACK)

        GlobalClient.TIMER.stop()
        GlobalClient.TIMER = Timer.Timer(GlobalClient.STREAM_TIMEOUT, GlobalClient.SIGINT_HANDLER)
    
        StreamClient.start_listening_to_stream()

    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))