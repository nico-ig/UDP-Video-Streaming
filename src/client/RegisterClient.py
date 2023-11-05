'''
Register a client to an already open stream
'''

from src.packets import UtilsPackets
from src.packets import TypesPackets
from src.packets import ClientPackets

from src.client import AudioClient
from src.client import GlobalClient
from src.client import StreamClient

from src.utils import Utils
from src.utils import Timer
from src.utils import Logger

audio_config_recv = False

def register_to_stream():
    '''
    Register to an already open stream in the server
    '''
    try:
        Logger.LOGGER.info("Registration started")

        send_registration_packet()

        Utils.start_thread(wait_audio_config)
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
        GlobalClient.NETWORK.send(GlobalClient.SERVER, packet, GlobalClient.IPV4)
        Logger.LOGGER.debug("Registration send")

        Timer.Timer(GlobalClient.RETRANSMIT_TIMEOUT, send_registration_packet)
        Logger.LOGGER.debug("Registration retransmit timer initiated")

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))
    
def wait_audio_config():
    try:
        GlobalClient.NETWORK.register_callback(
            TypesPackets.AUDIO_CONFIG, ClientPackets.parse_audio_config)

        Logger.LOGGER.debug("Waiting audio config")
        GlobalClient.AUDIO_CONFIG.wait()
        
        if GlobalClient.STOP_EVENT.is_set():
            return

        global audio_config_recv

        if audio_config_recv == False:
            Logger.LOGGER.info("Audio config received")
            Logger.LOGGER.info("Title: %s", GlobalClient.AUDIO_TITLE)
            Logger.LOGGER.info("Channels: %s", GlobalClient.AUDIO_CHANNELS)
            Logger.LOGGER.info("Samplerate: %s", GlobalClient.AUDIO_SAMPLERATE)
            Logger.LOGGER.info("Blocksize: %s", GlobalClient.AUDIO_BLOCKSIZE)
            AudioClient.start_player()
            audio_config_recv = True


        Logger.LOGGER.info("Sending audio config ack")
        packet = bytes([TypesPackets.AUDIO_CONFIG_ACK])
        GlobalClient.NETWORK.send(GlobalClient.SERVER, packet, GlobalClient.IPV4)

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def prepare_to_listen_to_stream():
    '''
    Prepare the client to start listening to the stream
    '''
    try:
        GlobalClient.NETWORK.register_callback(TypesPackets.REGISTER_ACK, ClientPackets.parse_register_ack)

        GlobalClient.REGISTER_ACK.wait()

        if GlobalClient.STOP_EVENT.is_set() or not GlobalClient.AUDIO_CONFIG.is_set():
            return
    
        Logger.LOGGER.info("Register ack received")
        GlobalClient.NETWORK.unregister_callback(TypesPackets.REGISTER_ACK)

        Logger.LOGGER.debug("Starting timer for remaining registration duration with %ss", GlobalClient.REGISTER_DURATION)
        Timer.Timer(GlobalClient.REGISTER_DURATION * 2, GlobalClient.CLOSE_CLIENT, True)

        StreamClient.listen_to_stream()
        
    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))
