"""
Manages the handshake with the server
"""

from http import server
from src.packets import UtilsPackets
from src.packets import TypesPackets
from src.client import GlobalClient
from src.utils import Timer

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
            TypesPackets.PORT_ALLOCATED, port_allocated)

    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))

def port_allocated(data, source):
    '''
    Callback function for when receiving the port allocated from server. Answer with an port ack
    '''
    try:
        if len(data) != 0:
            return

        '''
        This part should be changed  to compare the ip address, not the name and the ip address
        source_ip, source_port = source
        server_ip, server_port = GlobalClient.SERVER
        
        if source_ip != server_ip:
            return
        '''
        GlobalClient.LOGGER.info("Received port allocated from %s", source)

        GlobalClient.SERVER_TIMER.kick()
        GlobalClient.TIMER.stop()

        packet = UtilsPackets.mount_byte_packet(TypesPackets.PORT_ACK)

        GlobalClient.SERVER = source
        GlobalClient.LOGGER.info("Sending port ack to %s", GlobalClient.SERVER)
        GlobalClient.NETWORK.send(source, packet)

        send_registration_packet(source)

    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))

def send_registration_packet(server):
    """
    Send to server a request to register at a stream
    """
    try:
        packet = UtilsPackets.mount_byte_packet(TypesPackets.REGISTER)

        GlobalClient.LOGGER.info("Sending registration to %s", server)
        GlobalClient.NETWORK.send(server, packet)
    
        GlobalClient.TIMER = Timer.Timer(GlobalClient.REQUEST_ACK_TIMEOUT, send_registration_packet, GlobalClient.SERVER)
        GlobalClient.TIMER.kick()

        ## Registrar a callback pra quando receber o ack do registration, pode ser o start_listening acho
    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))

