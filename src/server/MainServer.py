'''
Creates and manages the server
'''

import os
import sys
import signal

from src.network import Network
from src.utils import Logger as L
from src.server import Globals as G
from src.network import Utils as NU
from src.server.stream import Stream as S
from src.server.handshake.open_stream import OpenStream as OS

def main():
    '''
    Starts and manages the server
    '''
    try:
        if len(sys.argv) < 3:
            print("Usage: python Server.py <hostname> <port> -i <interval ns(optional>) -4")
            exit()

        if len(sys.argv) > 3 and sys.argv[3] == 'i':
            S.INTERVAL = sys.argv[4]

        L.start_logger('server')
        L.set_logger('server')
        L.LOGGER.info("Creating server")

        signal.signal(signal.SIGINT, sigint_handler)

        G.SERVER_NAME = sys.argv[1]
        G.SERVER_PORT = sys.argv[2]

        ipv4 = True if sys.argv[-1] == "-4" else False
        G.NETWORK = Network.Network(ipv4, G.SERVER_NAME, G.SERVER_PORT)
        L.LOGGER.debug("Network interface created")

        S.load_audio(G.BLOCKSIZE, G.AUDIO_FOLDER)
        handshake()

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))
        sigint_handler()

def handshake():
    '''
    Perform the handshake with the clients
    '''
    try:
        G.NETWORK.register_callback(NU.OPEN_STREAM_REQUEST, parse_new_client)

        while not G.STOP_EVENT.is_set():
            L.LOGGER.info("Waiting for clients")
            client = G.CLIENTS_QUEUE.get()

            OS.open_new_stream(client)

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))
        handshake()

def parse_new_client(data, source):
    '''
    Parse the requests to start a new stream
    '''
    try:
        if len(data) != 0:
            return

        L.LOGGER.info("Parse new client from %s received", source)
        G.CLIENTS_QUEUE.put(source)
    
    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))
        raise Exception("Couldn't parse new client")

def sigint_handler(signum=0, frame=''):
    '''
    Stops the server when sigint is received
    '''
    try:
        if L.LOGGER != None:
            L.LOGGER.info("Sigint received")

        if G.NETWORK != None:
            G.NETWORK.stop()

            for child in G.CHILDREN.values():
                try:
                    os.kill(child.pid, signal.SIGINT)
                    child.terminate()
                except:
                    continue

        for child in G.CHILDREN.values():
            child.join()

    except Exception as e:
        if L.LOGGER != None:
            L.LOGGER.error("An error occurred: %s", str(e))

    finally:
        if L.LOGGER != None:
            L.LOGGER.info("Exitting")

main()