import heapq
import threading

import getBinary
import sounddevice as sd

file_path = "music.mp3"
blocksize = 2048
binary_fragments = []
h = []
event = threading.Event()

def callback(outdata, frames, time, status):
    data = h[0][1]
    heapq.heappop(h)
    if len(data) < len(outdata):
        outdata[:len(data)] = data
        outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
        raise sd.CallbackStop
    else:
        outdata[:] = data

try:
    getBinary.fragment_binary(binary_fragments, blocksize, file_path)
    for i in range(0, len(binary_fragments), 1):
        fragment = binary_fragments[i] 
        heapq.heappush(h, (i, fragment))  # Pre-fill queue

    stream = sd.RawOutputStream(
        samplerate=f.samplerate, blocksize=blocksize,
        device=None, channels=f.channels, dtype='float32',
        callback=callback, finished_callback=event.set)
    with stream:
       event.wait()  # Wait until playback is finished
except KeyboardInterrupt:
    print('\nInterrupted by user')
except Exception as e:
    print(type(e).__name__ + ': ' + str(e))
