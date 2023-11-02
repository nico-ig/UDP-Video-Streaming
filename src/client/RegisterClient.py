'''
Register a client to an already open stream
'''

from src.packets import UtilsPackets
from src.packets import TypesPackets
from src.packets import ClientPackets

from src.client import GlobalClient

from src.utils import Timer
from src.utils import Logger

def register_to_stream():
    '''
    Register to an already open stream in the server
    '''
    try:
        Logger.LOGGER.info("Registration started")

        send_registration_packet()
        prepare_to_listen_to_stream()

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def send_registration_packet():
    '''
    Send to server a request to register at a stream
    ''' 
    try:
        if GlobalClient.REGISTER_ACK.is_set() or GlobalClient.STOP_EVENT.is_set():
            return
            
        packet = UtilsPackets.mount_byte_packet(TypesPackets.REGISTER)
        GlobalClient.NETWORK.send(GlobalClient.SERVER, packet)
        Logger.LOGGER.debug("Registration send")

        Timer.Timer(GlobalClient.RETRANSMIT_TIMEOUT, send_registration_packet)
        Logger.LOGGER.debug("Registration retransmit timer initiated")

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))
    
def prepare_to_listen_to_stream():
    '''
    Prepare the client to start listening to the stream
    '''
    try:
        GlobalClient.NETWORK.register_callback(TypesPackets.REGISTER_ACK, ClientPackets.parse_register_ack)

        GlobalClient.REGISTER_ACK.wait()

        if GlobalClient.STOP_EVENT.is_set():
            return
    
        Logger.LOGGER.info("Register ack received")
        GlobalClient.NETWORK.unregister_callback(TypesPackets.REGISTER_ACK)

        Logger.LOGGER.debug("Starting timer for remaining registration duration with %ss", GlobalClient.REGISTER_DURATION)
        Timer.Timer(GlobalClient.REGISTER_DURATION * 2, GlobalClient.CLOSE_CLIENT, True)
        
    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))
