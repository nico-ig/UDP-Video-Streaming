"""
Creates and manages the client
"""

import signal
import sys

from src.client import HandshakeClient
from src.client import GlobalClient
from src.utils import Timer
from src.utils import Logger
from src.network import Network

GlobalClient.LOGGER = Logger.start_logger()
GlobalClient.LOGGER = Logger.get_logger('client')


def sigint_handler(signum=0, frame=''):
    """
    Stops the client when sigint is received
    """
    try:
        if GlobalClient.SERVER_TIMER != None:
            GlobalClient.SERVER_TIMER.stop()

        if GlobalClient.NETWORK != None:
            GlobalClient.NETWORK.stop()

        GlobalClient.LOGGER.info("Sigint received")
    except:
        pass


def main():
    """
    Starts and manages the client
    """
    try:
        if len(sys.argv) < 3:
            print("Usage: python Client.py <Server Name> <Server Port> -j")
            exit()

        GlobalClient.LOGGER.info("Creating client")

        signal.signal(signal.SIGINT, sigint_handler)

        server_name = sys.argv[1]
        server_port = sys.argv[2]
        GlobalClient.SERVER = (server_name, server_port)

        GlobalClient.NETWORK = Network.Network()
        GlobalClient.LOGGER.info("GlobalClient.NETWORK interface created")

        GlobalClient.SERVER_TIMER = Timer.Timer(
            GlobalClient.SERVER_TIMEOUT, sigint_handler)
        GlobalClient.LOGGER.info("Server timer initiated")

        option = 'join' if len(
            sys.argv) == 4 and sys.argv[3] == "-j" else 'new'
        HandshakeClient.client_handshake(option)

    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))


main()