'''
Creates and manages the server
'''

import os
import sys
import signal

from src.utils import Utils
from src.utils import Logger

from src.network import Network

from src.server import GlobalServer
from src.server import GlobalStream
from src.server import HandshakeServer

def main():
    '''
    Starts and manages the server
    '''
    try:
        if len(sys.argv) < 3:
            print("Usage: python Server.py <hostname> <port> -i <interval ns(optional>) -4")
            exit()

        if sys.argv[3] == 'i':
            GlobalStream.INTERVAL = sys.argv[4]

        Logger.start_logger('server')
        Logger.set_logger('server')
        Logger.LOGGER.info("Creating server")

        signal.signal(signal.SIGINT, sigint_handler)

        GlobalServer.SERVER_NAME = sys.argv[1]
        GlobalServer.SERVER_PORT = sys.argv[2]

        GlobalServer.IPV4 = True if sys.argv[-1] == "-4" else False
        GlobalServer.NETWORK = Network.Network(GlobalServer.IPV4, GlobalServer.SERVER_NAME, GlobalServer.SERVER_PORT)
        Logger.LOGGER.debug("Network interface created")

        GlobalServer.AUDIOS = Utils.get_audio_titles(GlobalServer.AUDIO_FOLDER)
        Logger.LOGGER.info("Available audios: %s", GlobalServer.AUDIOS)

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