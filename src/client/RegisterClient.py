'''
Register a client to an already open stream
'''

from ast import Global
from src.packets import UtilsPackets
from src.packets import TypesPackets
from src.packets import ClientPackets
from src.client import GlobalClient
from src.utils import Timer

timer = None

def register_to_stream():
    '''
    Register to an already open stream in the server
    '''
    try:
        GlobalClient.LOGGER.info("Registration started")

        global timer
        GlobalClient.LOGGER.debug("Starting registration retransmit timer")
        timer = Timer.Timer(GlobalClient.REQUEST_ACK_TIMEOUT, send_registration_packet)

        send_registration_packet()
        prepare_to_listen_to_stream()

    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))

def send_registration_packet(self=''):
    '''
    Send to server a request to register at a stream
    ''' 
    try:
        GlobalClient.LOGGER.debug("Sending registration")
        packet = UtilsPackets.mount_byte_packet(TypesPackets.REGISTER)
        GlobalClient.NETWORK.send(GlobalClient.SERVER, packet)
        timer.kick()

    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))
    
def prepare_to_listen_to_stream():
    '''
    Prepare the client to start listening to the stream
    '''
    try:
        GlobalClient.NETWORK.register_callback(TypesPackets.REGISTER_ACK, ClientPackets.parse_register_ack)

        while not GlobalClient.REGISTER_ACK.is_set():
            pass
    
        GlobalClient.LOGGER.info("Register ack received")
        GlobalClient.NETWORK.unregister_callback(TypesPackets.REGISTER_ACK)

        timer.stop()
        GlobalClient.LOGGER.debug("Registration retransmit timer stopped")

        GlobalClient.LOGGER.debug("Starting timer for remaining registration duration with %ss", GlobalClient.REGISTER_DURATION)
        GlobalClient.TIMER = Timer.Timer(GlobalClient.REGISTER_DURATION * 2, GlobalClient.SIGINT_HANDLER)
        
    except Exception as e:
        GlobalClient.LOGGER.error("An error occurred: %s", str(e))