# Deals with audio input 
# Recieves stream of audio and plays it 

import heapq
import threading
import struct
import sounddevice as sd

from src.client import GlobalClient as gc
from src.utils import StreamHeap
from src.utils import Packets
from src.utils import Utils

file_path = "musics"
file_blocksize = 2048   # Power of two that fits in MTU = 1500
h = []
event = threading.Event()

def callback(outdata, frames, time, status):
    data = h[0][1]
    heapq.heappop(h)
    print(data)
    if len(data) < len(outdata):
        outdata[:len(data)] = data
        outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
    try:
        data = h[0][1]
        print(f"Playing segment {h[0][0]}")
        heapq.heappop(h)
        if len(data) < len(outdata):
            outdata[:len(data)] = data
            outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
            raise sd.CallbackStop
        else:
            outdata[:] = data
    except:
        raise sd.CallbackStop
    else:
        outdata[:] = data
    
player = StreamHeap.stream_player()
 
def reproduce_stream(): # Call this function after the "STREAM_PACKET" is received
    try:
        packet = []
        packets = Packets.create_musics_packets(file_blocksize, file_path)
        for packet in packets:
            config = packet[0]
            audio_streams = packet[1]

            packet_type = config[0]
            print(f"Type: {packet_type}")

            config = config[1:]

            name, config = Utils.deserialize_str(config)
            print(f"Name: {name}")

            sample_rate = struct.unpack('Q', config[:8])[0]
            print(f"Sample rate: {sample_rate}")
            config = config[8:]

            channels = struct.unpack('Q', config)[0]
            print(f"Channles: {channels}")

            for stream in audio_streams:
                key = struct.unpack('Q', stream[:8])[0]
                stream = stream[8:]
                print(stream)
                heapq.heappush(h, (key, stream))
            

            
        stream = sd.RawOutputStream(
            samplerate=sample_rate, blocksize=file_blocksize // 8,
            device=None, channels=channels, dtype='float32',
            callback=callback, finished_callback=event.set)
        with stream:
            event.wait()  # Wait until playback is finished
    except KeyboardInterrupt:
        print('\nInterrupted by user')
    except Exception as e:
        print(type(e).__name__ + ': ' + str(e))


reproduce_stream()