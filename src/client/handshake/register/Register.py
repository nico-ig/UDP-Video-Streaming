'''
Register a client to an already open stream
'''

from src.utils import Timer
from src.utils import Utils
from src.utils import Logger as L
from src.client import Globals as G
from src.network import Utils as NU
from src.client.stream import Stream as S
from src.client.stream import Packets as SP
from src.client.handshake.register import Packets as P

def register_to_stream():
    '''
    Register to a stream in the server
    '''
    try:
        L.LOGGER.info("Registration started")

        send_registration_packet()
        Utils.start_thread(wait_audio_config, True)
        prepare_to_listen_to_stream()

    except Exception as e:
        L.LOGGER.error(f"Error registering to stream: {str(e)}")
        raise Exception(f"Couldn't register to stream")

def send_registration_packet():
    '''
    Send to server a request to register at a stream
    ''' 
    try:
        if P.REGISTER_ACK.is_set() or G.STOP_EVENT.is_set():
            return
            
        packet = bytes([NU.REGISTER])
        G.NETWORK.send(G.SERVER, packet)
        L.LOGGER.debug("Registration send")

        G.TIMERS.append(Timer.Timer(G.RETRANSMIT_TIMEOUT, send_registration_packet))
        L.LOGGER.debug("Registration retransmit timer initiated")

    except Exception as e:
        L.LOGGER.error("Error sending registration packet: %s", str(e))
        raise Exception("Couldn't send registration packet")
    
def wait_audio_config():
    '''
    Wait for the audio config from server
    '''
    try:
        G.NETWORK.register_callback(NU.AUDIO_CONFIG, P.parse_audio_config)

        L.LOGGER.debug("Waiting audio config")
        P.AUDIO_CONFIG.wait()
        if G.STOP_EVENT.is_set():
            return

        L.LOGGER.info("Audio config received")
        L.LOGGER.info("Title: %s", S.AUDIO_TITLE)
        L.LOGGER.info("Channels: %s", S.AUDIO_CHANNELS)
        L.LOGGER.info("Samplerate: %s", S.AUDIO_SAMPLERATE)
        L.LOGGER.info("Blocksize: %s", S.AUDIO_BLOCKSIZE)

    except Exception as e:
        L.LOGGER.error("Error while waiting for audio config: %s", str(e))

def prepare_to_listen_to_stream():
    '''
    Prepare the client to start listening to the stream
    '''
    try:
        G.NETWORK.register_callback(NU.REGISTER_ACK, P.parse_register_ack)

        P.REGISTER_ACK.wait()
        if G.STOP_EVENT.is_set():
            return
    
        L.LOGGER.info("Register ack received")
        G.NETWORK.unregister_callback(NU.STREAM_OPENED)

        L.LOGGER.debug("Starting timer for remaining registration duration with %ss", P.REGISTER_DURATION)
        G.TIMERS.append(Timer.Timer(P.REGISTER_DURATION * 2, registration_finished))

        P.AUDIO_CONFIG.wait()
        if G.STOP_EVENT.is_set():
            return

        S.listen_to_stream()
        
    except Exception as e:
        L.LOGGER.error("Error while preparing for listening to stream: %s", str(e))
        raise Exception("Couldn't start to listen to stream")

def registration_finished():
    try:
        if G.STOP_EVENT.is_set() or not SP.STREAM_STARTED.is_set():
            L.LOGGER.info("Couldn't register to server")
            G.CLOSE_CLIENT()
        
        #G.NETWORK.unregister_callback(NU.REGISTER_ACK)

    except Exception as e:
        L.LOGGER.error("Error while finishing registration: %s", str(e))
