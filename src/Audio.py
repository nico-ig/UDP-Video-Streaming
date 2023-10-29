import heapq
import threading
import struct

import getBinary
import sounddevice as sd

file_path = "music.mp3"
file_blocksize = 2048   # Power of two that fits in MTU = 1500
h = []
event = threading.Event()

def callback(outdata, frames, time, status):
    try:
        data = h[0][1]
        print(f"Playing segment {h[0][0][0]}")
        heapq.heappop(h)
        if len(data) < len(outdata):
            outdata[:len(data)] = data
            outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
            raise sd.CallbackStop
        else:
            outdata[:] = data
    except:
        raise sd.CallbackStop
    
try:
    packets_array = []
    file_samplerate, file_channels = getBinary.create_sound_packets(packets_array, file_blocksize, file_path)
    for i in range(0, len(packets_array), 1):
        packet = packets_array[i]
        seq = struct.unpack('Q', packet[:8])
        data = packet[8:]
        heapq.heappush(h, (seq, data)) # Change to streamheap 

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
