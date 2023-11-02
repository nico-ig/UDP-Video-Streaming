'''
Creates and manages the server
'''

import os
import sys
import signal

from src.server import GlobalServer
from src.server import HandshakeServer
from src.server import GlobalStream

from src.network import Network

from src.utils import Logger

def main():
    '''
    Starts and manages the server
    '''
    try:
        if len(sys.argv) < 3:
            print("Usage: python Server.py <hostname> <port> <interval ns(optional>)")
            exit()

        if len(sys.argv) >= 4:
            GlobalStream.INTERVAL = sys.argv[3]

        Logger.start_logger('server')
        Logger.LOGGER.info("Creating server")

        signal.signal(signal.SIGINT, sigint_handler)

        GlobalServer.SERVER_NAME = sys.argv[1]
        GlobalServer.SERVER_PORT = sys.argv[2]

        GlobalServer.NETWORK = Network.Network(GlobalServer.SERVER_NAME, GlobalServer.SERVER_PORT)
        Logger.LOGGER.debug("Network interface created")

        HandshakeServer.server_handshake()

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def sigint_handler(signum=0, frame=''):
    '''
    Stops the server when sigint is received
    '''
    try:
        Logger.LOGGER.info("Sigint received")

        GlobalServer.STOP_EVENT.set()
        GlobalServer.CLIENTS_QUEUE.put(0, 0)                    

        if GlobalServer.NETWORK != None:
            GlobalServer.NETWORK.stop()

            for child in GlobalServer.CHILDREN.values():
                try:
                    os.kill(child.pid, signal.SIGINT)
                    child.terminate()
                except:
                    continue

        for child in GlobalServer.CHILDREN.values():
            child.join()

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

    finally:
        Logger.LOGGER.info("Exitting")

main()