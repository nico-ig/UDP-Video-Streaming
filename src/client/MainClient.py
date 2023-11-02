'''
Creates and manages the client
'''

import signal
import sys

from src.client import HandshakeClient
from src.client import GlobalClient
from src.utils import Logger
from src.network import Network


def main():
    '''
    Starts and manages the client
    '''
    try:
        if len(sys.argv) < 3:
            print("Usage: python Client.py <Server Name> <Server Port> -j")
            exit()

        Logger.start_logger('client')
        Logger.LOGGER.info("Starting client")

        signal.signal(signal.SIGINT, GlobalClient.SIGINT_HANDLER)

        server_name = sys.argv[1]
        server_port = sys.argv[2]
        GlobalClient.SERVER = (server_name, server_port)

        GlobalClient.NETWORK = Network.Network()
        Logger.LOGGER.debug("Network interface created")

        option = 'join' if len(
            sys.argv) == 4 and sys.argv[3] == "-j" else 'new'
        HandshakeClient.client_handshake(option)

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))


main()
