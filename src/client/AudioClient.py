# Deals with audio input 
# Recieves stream of audio and plays it 

import heapq
import threading
import struct
import sounddevice as sd

from src.client import GlobalClient as gc
from src.utils import StreamHeap as sh
from src.utils import Packets

file_path = "../musics/musics.mp3"
file_blocksize = 2048   # Power of two that fits in MTU = 1500
# h = []
event = threading.Event()

def callback(outdata, frames, time, status):
    try:
        data = gc.STREAM[0][1]
        # print(f"Playing segment {gc.STREAM[0][0][0]}")
        sh.remove_from_stream()
        if len(data) < len(outdata):
            outdata[:len(data)] = data
            outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
            raise sd.CallbackStop
        else:
            outdata[:] = data
    except:
        raise sd.CallbackStop
    
def reproduce_stream(): # Call this function after the "STREAM_PACKET" is received
    try:
        packets_array = []
        file_samplerate, file_channels = Packets.create_musics_packets(packets_array, file_blocksize, file_path)
        for i in range(0, len(packets_array), 1):
            packet = packets_array[i]
            seq = struct.unpack('Q', packet[:8])
            data = packet[8:]
            sh.add_to_stream(seq, data)

        stream = sd.RawOutputStream(
            samplerate=file_samplerate, blocksize=file_blocksize // 8,
            device=None, channels=file_channels, dtype='float32',
            callback=callback, finished_callback=event.set)
        with stream:
            event.wait()  # Wait until playback is finished
    except KeyboardInterrupt:
        print('\nInterrupted by user')
    except Exception as e:
        print(type(e).__name__ + ': ' + str(e))


reproduce_stream()