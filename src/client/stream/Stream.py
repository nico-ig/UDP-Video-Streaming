'''
Deals with audio input 
Recieves stream of audio and plays it 
'''

import sounddevice as sd

from src.utils import Timer
from src.utils import Logger as L
from src.client import Globals as G
from src.network import Utils as NU
from src.client.stream import AlsaUtils
from src.client.stream import Packets as P
from src.client.stream import StreamHeap as SH

player = None
AUDIO_TITLE = ''
AUDIO_SAMPLERATE = 0
AUDIO_CHANNELS = 0
AUDIO_BLOCKSIZE = 0

def listen_to_stream():
    '''
    Start the stream player
    '''
    try:
        #G.SERVER_TIMER = Timer.Timer(G.STREAM_TIMEOUT / 1e9, G.CLOSE_CLIENT)
        L.LOGGER.debug("Stream packets timer initiated")

        G.NETWORK.register_callback(NU.STREAM, P.parse_stream_packets)

        try_to_change_alsa_error_handler()

        samplerate = AUDIO_SAMPLERATE
        channels = AUDIO_CHANNELS
        blocksize = AUDIO_BLOCKSIZE

        global player
        player = sd.RawOutputStream(
            samplerate=samplerate, blocksize=blocksize // 8,
            device=None, channels=channels, dtype='float32',
            callback=callback, finished_callback=None)

        player.start()
        L.LOGGER.info("Player started")
        
    except Exception as e:
        L.LOGGER.error("CLosing client, error while listening to stream: %s", str(e))
        G.CLOSE_CLIENT()

def try_to_change_alsa_error_handler():
    '''
    Try to change alsa error handler, if not success alsa errors will
    show on terminal
    '''
    try:
        alsa_logger = L.get_logger('alsa')
        AlsaUtils.set_error_handler(alsa_logger)

    except Exception as e:
        L.LOGGER.error("Couldn't change alsa error handler: %s", str(e))


def callback(outdata, frames, time, status):
    '''
    Callback function to fill the buffer used by sounddevice
    '''
    try:
        seq, stream = SH.remove()

        if len(stream) < len(outdata):
            outdata[:len(stream)] = stream
            outdata[len(stream):] = b'\x00' * (len(outdata) - len(stream))

        else:
            outdata[:] = stream

    except Exception as e:
        L.LOGGER.error("Error in stream callback: %s", str(e))

    finally:
        if G.STOP_EVENT.is_set():
            raise sd.CallbackStop()

    