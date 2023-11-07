'''
Opens a new stream in the server
'''

from src.utils import Timer
from src.utils import Logger as L
from src.client import Globals as G
from src.network import Utils as NU
from src.client.handshake.register import Register
from src.client.handshake.open_stream import Packets as P

def open_stream_in_server():
    '''
    Open a new stream in the server
    '''
    try:
        L.LOGGER.debug("Oppening a new stream")

        send_stream_request()
        wait_stream_opened()

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))
        raise Exception("Error opening a new stream in server")

def send_stream_request():
    '''
    Send the request for a stream port at the server
    '''
    try:
        if P.STREAM_OPENED.is_set() or G.STOP_EVENT.is_set():
            return
        
        L.LOGGER.info("Sending new stream request")
        packet = bytes([NU.OPEN_STREAM_REQUEST])
        G.NETWORK.send(G.SERVER, packet)

        G.TIMERS.append(Timer.Timer(G.RETRANSMIT_TIMEOUT, send_stream_request))
        L.LOGGER.debug("Stream request retransmit timer initiated")

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))
        send_stream_request()

def wait_stream_opened():
    '''
    Deals with the port allocated packet from server. Answer with an port ack. 
    The callback for this type is unregistered only once the stream starts,
    since the packet may be lost and be requested more than once by the server
    '''
    try:
        G.NETWORK.register_callback(NU.STREAM_OPENED, P.parse_stream_opened)

        L.LOGGER.debug("Waiting for stream to be opened")
        P.STREAM_OPENED.wait()

        if G.STOP_EVENT.is_set():
            return

        Register.register_to_stream()

    except Exception as e:
        L.LOGGER.error("An error occurred: %s", str(e))
        G.NETWORK.unregister_callback(NU.STREAM_OPENED)
        wait_stream_opened()