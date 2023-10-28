import heapq
import threading

import sounddevice as sd
import soundfile as sf

filename = "music.mp3"
blocksize = 2048
h = []
event = threading.Event()

def callback(outdata, frames, time, status):
    try:
        data = h[0][1]
        heapq.heappop(h)
    except IndexError:
        print("Heap is empty, cannot pop an element.")
    if len(data) < len(outdata):
        outdata[:len(data)] = data
        outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
        raise sd.CallbackStop
    else:
        outdata[:] = data

try:
    with sf.SoundFile(filename) as f:
        i = 0
        while True:
            data = f.buffer_read(blocksize, dtype='float32')
            if not data:
                break
            heapq.heappush(h, (i, data))  # Pre-fill queue
            i += 1
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
