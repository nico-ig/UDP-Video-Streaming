'''
Creates and manages the client
'''

import sys
import signal

from src.utils import Timer
from src.network import Network
from src.utils import Logger as L
from src.client import Globals as G
from src.client.handshake.register import Register
from src.client.handshake.open_stream import OpenStream

def main():
    '''
    Starts and manages the client
    '''
    try:
        if len(sys.argv) < 3:
            print("Usage: python Client.py <Server Name> <Server Port> -j -4(optional)")
            exit()

        L.start_logger('client', 'alsa')
        L.set_logger('client')
        L.LOGGER.info("Starting client")

        signal.signal(signal.SIGINT, G.CLOSE_CLIENT)

        server_name = sys.argv[1]
        server_port = sys.argv[2]
        G.SERVER = (server_name, server_port)

        ipv4 = True if sys.argv[-1] == "-4" else False

        G.NETWORK = Network.Network(ipv4)
        L.LOGGER.debug("Network interface created")

        option = 'join' if len(
            sys.argv) == 4 and sys.argv[3] == "-j" else 'new'
        client_handshake(option)

    except Exception as e:
        L.LOGGER.error("Closing client, an error ocured: %s", str(e))
        G.CLOSE_CLIENT()

def client_handshake(option):
    '''
    Perform the handshake with the server
    '''
    try:
        #G.TIMERS.append(Timer.Timer(G.HANDSHAKE_TIMEOUT, G.CLOSE_CLIENT))
        
        if option == 'join':
            L.LOGGER.info("Joining stream")
            Register.register_to_stream()

        else:
            OpenStream.open_stream_in_server()

    except Exception as e:
        L.LOGGER.error("Error while performing handshake with server: %s", str(e))
        raise Exception("Couldn't perform handshake with server")

main()
