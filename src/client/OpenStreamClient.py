'''
Opens a new stream in the server
'''

from src.packets import UtilsPackets
from src.packets import TypesPackets
from src.packets import ClientPackets
from src.client import GlobalClient
from src.utils import Timer

timer = None

def open_stream_in_server():
    '''
    Open a new stream in the server
    '''
    try:
        GlobalClient.LOGGER.debug("Oppening a new stream")

        global timer
        timer = Timer.Timer(GlobalClient.RETRANSMIT_TIMEOUT, send_port_request)
        GlobalClient.LOGGER.debug("Port request retransmit timer initiated")

        send_port_request()
        wait_port_allocated()

    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))

def send_port_request():
    '''
    Send the request for a stream port at the server
    '''
    try:
        GlobalClient.LOGGER.info("Sending new port request")
        packet = UtilsPackets.mount_byte_packet(TypesPackets.NEW_PORT_REQUEST)
        GlobalClient.NETWORK.send(GlobalClient.SERVER, packet)

        timer.kick()

    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))

def wait_port_allocated():
    '''
    Deals with the port allocated packet from server. Answer with an port ack. 
    The callback for this type is unregistered only once the stream starts,
    since the packet may be lost and be requested more than once by the server
    '''
    try:
        GlobalClient.NETWORK.register_callback(
            TypesPackets.PORT_ALLOCATED, ClientPackets.parse_port_allocated)

        while not GlobalClient.PORT_ALLOCATED.is_set():
            pass

        GlobalClient.LOGGER.debug("Port request retransmit timer stopped")
        timer.stop()

        GlobalClient.LOGGER.info("Port allocated received")
        GlobalClient.LOGGER.info("Sending port ack")
        packet = UtilsPackets.mount_byte_packet(TypesPackets.PORT_ACK)
        GlobalClient.NETWORK.send(GlobalClient.SERVER, packet)

    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))
