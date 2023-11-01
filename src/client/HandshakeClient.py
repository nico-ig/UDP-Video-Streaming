'''
Manages the handshake with the server
'''

from src.client import GlobalClient
from src.client import StreamClient
from src.client import OpenStreamClient
from src.client import RegisterClient

from src.utils import Utils
from src.utils import Timer

def client_handshake(option):
    '''
    Perform the handshake with the server
    '''
    try:
        if option == 'join':
            GlobalClient.LOGGER.info("Joining stream")
            new_stream_thread = None

        else:
            GlobalClient.LOGGER.info("Entering new stream")
            Utils.start_thread(OpenStreamClient.open_stream_in_server, '', True)

        Utils.start_thread(RegisterClient.register_to_stream, '', True)
        #StreamClient.start_listening_to_stream()

    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))