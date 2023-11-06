'''
Manages the handshake with the server
'''

from src.client import GlobalClient
from src.client import RegisterClient
from src.client import OpenStreamClient

from src.utils import Timer
from src.utils import Logger

def client_handshake(option):
    '''
    Perform the handshake with the server
    '''
    try:
        Timer.Timer(GlobalClient.HANDSHAKE_TIMEOUT, GlobalClient.CLOSE_CLIENT)
        
        if option == 'join':
            Logger.LOGGER.info("Joining stream")
            RegisterClient.register_to_stream()

        else:
            Logger.LOGGER.info("Opening a new stream")
            OpenStreamClient.open_stream_in_server()


    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))
        GlobalClient.CLOSE_CLIENT()