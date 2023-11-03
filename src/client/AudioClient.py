# Deals with audio input 
# Recieves stream of audio and plays it 

import os
import shutil
import heapq
import threading
import struct
import sounddevice as sd

from src.client import GlobalClient as gc
from src.utils import StreamHeap
from src.utils import Packets
from src.utils import Utils

file_path = "musics"
file_blocksize = 1024
h = []
event = threading.Event()
heap_lock = threading.Lock()

def callback(outdata, frames, time, status):
    try:
        with heap_lock:
            seq, stream = heapq.heappop(h)
            
        if len(stream) < len(outdata):
            outdata[:len(stream)] = stream
            outdata[len(stream):] = b'\x00' * (len(outdata) - len(stream))

            raise sd.CallbackStop

        else:
            outdata[:] = stream
    except:
        raise sd.CallbackStop
    
player = StreamHeap.stream_player()
 
def capture_alsa():
    try:
        if os.path.isfile('~/.asoundrc'):
            shutil.copy('~/.asoundrc', '~/.asoundrc_bkp')

        os.system('cat ./config/asoundrc >> ~/.asoundrc')

        with open('~/.asoundrc', "rw") as config_file:
            alsa_config = config_file.read()
            output_device = sd.query_devices(kind='output', query='default')
            print(alsa_config)
            alsa_config = alsa_config.replace("<device>", output_device)
            print(alsa_config)
            config_file.write(alsa_config)

    except:
        pass

def restore_alsa():
    try:
        if os.path.isfile('~/.asoundrc_bkp'):
            shutil.copy('~/.asoundrc_bkp', '~/.asoundrc')
            os.remove('~/.asoundrc_bkp')
        else:
            os.remove('~/.asoundrc')

    except:
        pass

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

            #capture_alsa()
            player = sd.RawOutputStream(
                samplerate=sample_rate, blocksize=file_blocksize // 8,
                device=None, channels=channels, dtype='float32',
                callback=callback, finished_callback=event.set)


            for stream in audio_streams:
                seq = struct.unpack('Q', stream[:8])[0]
                stream = stream[8:]
                # Não sei e precisa, mas é pra evitar adicionar um pacote com a callback fazendo o pop
                with heap_lock:
                    heapq.heappush(h, (seq, stream))

            with player:
                event.wait()  # Wait until playback is finished
                print("Finished")
                event.clear()

    except KeyboardInterrupt:
        print('\nInterrupted by user')

    except Exception as e:
        print(type(e).__name__ + ': ' + str(e))

    # finally:
    #     restore_alsa()
        
        
reproduce_stream()