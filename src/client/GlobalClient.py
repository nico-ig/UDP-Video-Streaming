"""
Global values for the client
"""

NETWORK = None          # Network interface
SERVER = None           # Server address
SERVER_TIMER = None     
TIMER = None
LOGGER = None           

SERVER_TIMEOUT = 5              # Time in seconds before timeouting when not receiving packets from server
NEW_PORT_REQUEST_TIMEOUT = 3    # Time in seconds before sending NEW_PORT_REQUEST again
REQUEST_ACK_TIMEOUT = 3         # Time in seconds before sending REGISTER again

STREAM_TIMEOUT =  100      # The start value in the amount of intervals between stream packets before timeouting

def SIGINT_HANDLER(signum=0, frame=''):
    """
    Stops the client when sigint is received
    """
    try:
        if SERVER_TIMER != None:
            SERVER_TIMER.stop()
            
        if TIMER != None:
            TIMER.stop()

        if NETWORK != None:
            NETWORK.stop()

        LOGGER.info("Sigint received")
   
    except Exception as e:
        LOGGER.error("An error occurred: %s", str(e))

