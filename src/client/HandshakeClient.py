'''
Manages the handshake with the server
'''

from src.client import GlobalClient
from src.client import StreamClient
from src.client import OpenStreamClient
from src.client import RegisterClient

from src.utils import Utils
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

        else:
            Logger.LOGGER.info("Entering new stream")
            Utils.start_thread(OpenStreamClient.open_stream_in_server, True)

        Utils.start_thread(RegisterClient.register_to_stream, True)
        StreamClient.listen_to_stream()

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))