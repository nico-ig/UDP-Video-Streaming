# Deals with the parsing of the packets (incoming and outgoing) for the server

from src.server import GlobalServer
from src.server import GlobalStream

from src.utils import Logger

from src.packets import TypesPackets

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
