"""
Creates and manages the client
"""

import signal
import sys

from src.client import HandshakeClient
from src.utils import Timer
from src.utils import Logger
from src.network import Network

network = None
server_timer = None
server_timeout = 5
server = None

logger = Logger.start_logger()
logger = Logger.get_logger('client')

def sigint_handler(signum=0, frame=''):
    """
    Stops the client when sigint is received
    """
    try:
        if server_timer != None:
            server_timer.stop()

        if network != None:
            network.stop()

        logger.info("Sigint received")
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

        logger.info("Creating client")
        
        signal.signal(signal.SIGINT, sigint_handler)

        global host, port, network, server_timer, server

        server_name = sys.argv[1]
        server_port = sys.argv[2]
        server = (server_name, server_port)
        
        network = Network.Network()
        logger.info("Network interface created")
        
        server_timer = Timer.Timer(server_timeout, sigint_handler)
        logger.info("Server timer initiated")

        option = 'join' if len(sys.argv) == 4 and sys.argv[3] == "-j" else 'new'
        HandshakeClient.client_handshake(network, server, server_timer, logger, option)

    except Exception as e:
        error_message = 'Error creating client - ' + type(e)+ ': ' + str(e)
        logger.error(error_message)

main()
