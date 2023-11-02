'''
Receives the request for new streams
'''

import multiprocessing

from src.packets import TypesPackets
from src.packets import ServerPackets

from src.server import GlobalServer
from src.server import StreamServer

from src.utils import Logger

def server_handshake():
    '''
    Perform the handshake with the clients
    '''
    try:
        GlobalServer.NETWORK.register_callback(TypesPackets.NEW_PORT_REQUEST, ServerPackets.parse_new_client)

        while not GlobalServer.STOP_EVENT.is_set():
            Logger.LOGGER.info("Waiting for clients")
            client = GlobalServer.CLIENTS_QUEUE.get()

            start_new_streaming(client)

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def start_new_streaming(client):
    '''
    Starts a new process to deal with the client stream
    '''
    try:
        if GlobalServer.STOP_EVENT.is_set():
            return

        if client in GlobalServer.CHILDREN.values():
            Logger.LOGGER.info("Terminating process for client %s", client)
            GlobalServer.CHILDREN[client].terminate()
            GlobalServer.CHILDREN[client].join()

        Logger.LOGGER.info("Starting a new process for client %s", client)
        GlobalServer.CHILDREN[client] = multiprocessing.Process(target=StreamServer.new_stream, args=(GlobalServer.SERVER_NAME, client))
        GlobalServer.CHILDREN[client].start()

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))
