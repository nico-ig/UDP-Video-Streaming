"""
Manages the handshake with the server
"""

from src.packets import UtilsPackets
from src.packets import TypesPackets
from src.client import GlobalClient


def send_registration_packet(server):
    """
    Send to server a request to register at a stream
    """
    try:
        packet = UtilsPackets.mount_byte_packet(TypesPackets.REGISTER)

        GlobalClient.LOGGER.info("Sending register to %s", GlobalClient.SERVER)
        GlobalClient.NETWORK.send(server, packet)
    
    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))


def port_allocated(data, source):
    """
    Callback function when receiving the port allocated from server. Answer with an port ack
    """
    try:
        if len(data) != 0:
            return

        GlobalClient.LOGGER.info("Received port allocated from %s", source)

        GlobalClient.SERVER_TIMER.kick()
        GlobalClient.NETWORK.unregister_callback(TypesPackets.PORT_ALLOCATED)

        packet = UtilsPackets.mount_byte_packet(TypesPackets.PORT_ACK)

        GlobalClient.LOGGER.info("Sending port ack to %s", GlobalClient.SERVER)
        GlobalClient.NETWORK.send(source, packet)

        send_registration_packet(source)

    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))


def send_port_request():
    """
    Send the request for a stream port at the server
    """
    try:
        packet = UtilsPackets.mount_byte_packet(TypesPackets.NEW_PORT_REQUEST)

        GlobalClient.LOGGER.info("Sending new port request to %s", GlobalClient.SERVER)
        GlobalClient.NETWORK.send(GlobalClient.SERVER, packet)

        GlobalClient.NETWORK.register_callback(
            TypesPackets.PORT_ALLOCATED, port_allocated)

    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))


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
