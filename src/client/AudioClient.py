'''
Deals with audio input 
Recieves stream of audio and plays it 
'''

import sounddevice as sd

from src.utils import Logger
from src.utils import AlsaUtils
from src.utils import StreamHeap as sh

from src.client import GlobalClient

def callback(outdata, frames, time, status):
    '''
    Callback function to fill the buffer used by sounddevice
    '''
    try:
        seq, stream = GlobalClient.AUDIO_BUFFER.remove_from_buffer()

        if len(stream) < len(outdata):
            outdata[:len(stream)] = stream
            outdata[len(stream):] = b'\x00' * (len(outdata) - len(stream))

        else:
            outdata[:] = stream

    except:
        pass
    
def start_player():
    '''
    Start the stream player
    '''
    try:
        alsa_logger = Logger.get_logger('alsa')
        AlsaUtils.set_error_handler(alsa_logger)

        samplerate = GlobalClient.AUDIO_SAMPLERATE
        channels = GlobalClient.AUDIO_CHANNELS
        blocksize = GlobalClient.AUDIO_BLOCKSIZE

        player = sd.RawOutputStream(
            samplerate=samplerate, blocksize=blocksize // 8,
            device=None, channels=channels, dtype='float32',
            callback=callback, finished_callback=None)

        GlobalClient.AUDIO_BUFFER = sh.StreamHeap()

        player.start()
        Logger.LOGGER.info("Player started, waiting for stream to start")
        
    except Exception as e:
        Logger.LOGGER.error("An error occurred: %s", str(e))
        GlobalClient.CLOSE_CLIENT()
