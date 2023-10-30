'''
Receives the request for new streams
'''

import multiprocessing

from src.packets import TypesPackets
from src.server import GlobalServer
from src.server import StreamServer

def start_new_streaming(data, source):
    '''
    Starts a new process to deal with the client stream
    '''
    try:
        if len(data) != 0:
            return

        if source in GlobalServer.CHILDREN:
            GlobalServer.LOGGER.info("Terminating process for client %s", source)
            GlobalServer.CHILDREN[source].terminate()
            GlobalServer.CHILDREN[source].join()

        GlobalServer.LOGGER.info("Starting a new process for client %s", source)
        GlobalServer.CHILDREN[source] = multiprocessing.Process(target=StreamServer.new_stream, args=(GlobalServer.SERVER_NAME, source))
        GlobalServer.CHILDREN[source].start()

    except Exception as e:
        GlobalServer.LOGGER.error("An error occurred: %s", str(e))

def server_handshake():
    '''
    Perform the handshake with the server
    '''
    try:
        GlobalServer.LOGGER.info("Waiting for clients")
        GlobalServer.NETWORK.register_callback(TypesPackets.NEW_PORT_REQUEST, start_new_streaming)

    except Exception as e:
        GlobalServer.LOGGER.error("An error occurred: %s", str(e))