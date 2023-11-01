"""
Creates and manages the server
"""

import signal
import sys

from src.server import GlobalServer
from src.server import HandshakeServer
from src.server import GlobalStream
from src.network import Network
from src.utils import Logger

def sigint_handler(signum=0, frame=''):
    """
    Stops the server when sigint is received
    """
    try:
        if GlobalServer.NETWORK != None:
            GlobalServer.NETWORK.stop()

        for child in GlobalServer.CHILDREN.values():
            child.terminate()

        for child in GlobalServer.CHILDREN.values():
            child.join()

    except Exception as e:
        GlobalServer.LOGGER.error("An error occurred: %s", str(e))

def main():
    """
    Starts and manages the server
    """
    try:
        if len(sys.argv) < 3:
            print("Usage: python Server.py <hostname> <port> <interval ns(optional>)")
            exit()

        if len(sys.argv) >= 4:
            GlobalStream.INTERVAL = sys.argv[3]

        GlobalServer.LOGGER = Logger.start_logger()
        GlobalServer.LOGGER = Logger.get_logger('server')
        GlobalServer.LOGGER.info("Creating server")

        signal.signal(signal.SIGINT, sigint_handler)

        GlobalServer.SERVER_NAME = sys.argv[1]
        GlobalServer.SERVER_PORT = sys.argv[2]

        GlobalServer.NETWORK = Network.Network(GlobalServer.SERVER_NAME, GlobalServer.SERVER_PORT)
        GlobalServer.LOGGER.info("GlobalServer.NETWORK interface created")

        HandshakeServer.server_handshake()

    except Exception as e:
        GlobalServer.LOGGER.error("An error occurred: %s", str(e))

main()