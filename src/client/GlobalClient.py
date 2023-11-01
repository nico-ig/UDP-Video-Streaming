'''
Global values for the client
'''

import threading

from src.packets import TypesPackets


NETWORK = None          # Network interface
SERVER = None           # Server address
SERVER_TIMER = None     
TIMER = None
LOGGER = None           

SERVER_TIMEOUT = 5              # Time in seconds before timeouting when not receiving packets from server
RETRANSMIT_TIMEOUT = 3    # Time in seconds before sending NEW_PORT_REQUEST again
REQUEST_ACK_TIMEOUT = 3         # Time in seconds before sending REGISTER again

REGISTER_DURATION = 0      # The durantion of the registration phase received by the server

STREAM_TIMEOUT =  10      # The start value in the amount of intervals between stream packets before timeouting

PORT_ALLOCATED = threading.Event()
REGISTER_ACK = threading.Event()

def SIGINT_HANDLER(signum=0, frame=''):
    '''
    Stops the client when sigint is received
    '''
    try:
        LOGGER.info("Sigint received")
   
        if SERVER_TIMER != None:
            SERVER_TIMER.stop()
            
        if TIMER != None:
            TIMER.stop()

        if NETWORK != None:
            NETWORK.stop()

    except Exception as e:
        LOGGER.error("An error occurred: %s", str(e))

