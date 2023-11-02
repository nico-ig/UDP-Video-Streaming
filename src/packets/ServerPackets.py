'''
Deals with the parsing of the packets (incoming and outgoing) for the server
'''

import struct

from src.server import GlobalServer
from src.server import GlobalStream

from src.packets import TypesPackets
from src.packets import UtilsPackets

from src.utils import Logger

def parse_new_client(data, source):
    '''
    Parse the requests to start a new stream
    '''
    try:
        if len(data) != 0:
            return

        Logger.LOGGER.info("Parse new client from %s received", source)
        GlobalServer.CLIENTS_QUEUE.put(source)
    
    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def parse_port_ack(data, source):
    '''
    Deals with port ack incoming packets
    '''
    try:
        if len(data) != 0:
            return

        source_ip, source_port = source
        lider_ip, lider_port = GlobalStream.LIDER

        if source_ip != lider_ip:
            Logger.LOGGER.debug("Port ACK send by %s and not %s", source, GlobalStream.LIDER)
            return

        Logger.LOGGER.info("Port ack received")

        GlobalStream.LIDER_TIMER.stop()
        Logger.LOGGER.debug("Port allocated retransmit timer stopped")

        GlobalStream.NETWORK.unregister_callback(TypesPackets.PORT_ACK)

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))


def parse_new_registration(data, source):
    '''
    Parse the packet for a new register from clients
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