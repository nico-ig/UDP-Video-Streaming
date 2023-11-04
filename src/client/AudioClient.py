'''
Deals with audio input 
Recieves stream of audio and plays it 
'''

import time
import struct
import sounddevice as sd

from src.client import GlobalClient as gc
from src.utils import Packets
from src.utils import Utils
from src.utils import StreamHeap as sh

file_path = "musics"
file_blocksize = 1024

buffer = None

def callback(outdata, frames, time, status):
    '''
    Callback function to fill the buffer used by sounddevice
    '''
    try:
        seq, stream = buffer.remove_from_buffer()
        print(f'Playing seq {seq}')
        
        if len(stream) < len(outdata):
            outdata[:len(stream)] = stream
            outdata[len(stream):] = b'\x00' * (len(outdata) - len(stream))

        else:
            outdata[:] = stream

    except:
        pass
    
def reproduce_stream(): # Call this function after the "STREAM_PACKET" is received
    try:
        Utils.capture_alsa()

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

            player = sd.RawOutputStream(
                samplerate=sample_rate, blocksize=file_blocksize // 8,
                device=None, channels=channels, dtype='float32',
                callback=callback, finished_callback=None)

            global buffer
            buffer = sh.StreamHeap()
            player.start()

            for stream in audio_streams:
                seq = struct.unpack('Q', stream[:8])[0]
                stream = stream[8:]
                buffer.add_to_buffer(seq, stream)

            # ---------- REMOVE THIS BLOCK AFTER TESTING -----------
            time.sleep(10)
            player.close()
            print(f'Finished')
            time.sleep(1)
            # ----------------- END OF BLOCK ----------------

    except KeyboardInterrupt:
        print('\nInterrupted by user')

    except Exception as e:
        print("An error occurred: %s", str(e))

    finally:
        Utils.restore_alsa()
        
        
reproduce_stream()