'''
Opens a new stream in the server
'''

import sys
import select

from src.utils import Timer
from src.utils import Logger

from src.packets import UtilsPackets
from src.packets import TypesPackets
from src.packets import ClientPackets

from src.client import GlobalClient

def open_stream_in_server():
    '''
    Open a new stream in the server
    '''
    try:
        Logger.LOGGER.debug("Oppening a new stream")

        send_port_request()
        wait_port_allocated()

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def send_port_request():
    '''
    Send the request for a stream port at the server
    '''
    try:
        if GlobalClient.PORT_ALLOCATED.is_set() or GlobalClient.STOP_EVENT.is_set():
            return
        
        Logger.LOGGER.info("Sending new port request")
        packet = UtilsPackets.mount_byte_packet(TypesPackets.NEW_PORT_REQUEST)
        GlobalClient.NETWORK.send(GlobalClient.SERVER, packet, GlobalClient.IPV4)

        Timer.Timer(GlobalClient.RETRANSMIT_TIMEOUT, send_port_request)
        Logger.LOGGER.debug("Port request retransmit timer initiated")

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def wait_port_allocated():
    '''
    Deals with the port allocated packet from server. Answer with an port ack. 
    The callback for this type is unregistered only once the stream starts,
    since the packet may be lost and be requested more than once by the server
    '''
    try:
        GlobalClient.NETWORK.register_callback(
            TypesPackets.PORT_ALLOCATED, ClientPackets.parse_port_allocated)

        Logger.LOGGER.debug("Waiting port allocated")
        GlobalClient.PORT_ALLOCATED.wait()

        if GlobalClient.STOP_EVENT.is_set():
            return

        Logger.LOGGER.info("Port allocated received")
        Logger.LOGGER.info("Available audios are: %s", GlobalClient.AUDIOS)
        get_audio_choice()

        Logger.LOGGER.info("Sending port ack")
        packet = ClientPackets.mount_port_ack_packet()
        GlobalClient.NETWORK.send(GlobalClient.SERVER, packet, GlobalClient.IPV4)

    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))

def get_audio_choice():
    '''
    Get the audio id that should be requested
    '''
    if GlobalClient.AUDIO_ID >= 0:
        return

    print("Choose an audio ID to play it")
    print_available_audios()

    input_list = select.select([sys.stdin], [], [], GlobalClient.AUDIO_CHOICE_TIMEOUT)[0]
    if input_list:
        GlobalClient.AUDIO_ID = int(sys.stdin.readline().strip())
        print("You chose audio ID: " + str(GlobalClient.AUDIO_ID))

    else:
        GlobalClient.AUDIO_ID = 0
        print("Timeout, using default audio ID: " + str(GlobalClient.AUDIO_ID))


    if GlobalClient.AUDIO_ID >= len(GlobalClient.AUDIOS):
        GlobalClient.AUDIO_ID = 0
        print("Invalid value, using default ID: " + str(GlobalClient.AUDIO_ID))
        
    Logger.LOGGER.info(f'Requested audio id: {GlobalClient.AUDIO_ID}')

def print_available_audios():
    '''
    Print title list received from server
    '''
    print("Available audios:")
    print("ID / Audio Title")
    for i in range(0, len(GlobalClient.AUDIOS)):
        print(str(i) + " / " + GlobalClient.AUDIOS[i])