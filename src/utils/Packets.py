import soundfile as sf
import struct
from src.utils import Utils
import os

subtype_to_bit_depth = {
        'PCM_16': 16,
        'PCM_24': 24,
        'PCM_32': 32,
        'PCM_U8': 8,
        'FLOAT32': 32,
        'FLOAT64': 64,
        'ALAW_16': 16,
        'MULAW_16': 16,
        'MPEG_LAYER_III': 24
        # Add more subtypes as needed
    }

def get_bit_depth(file):
    return subtype_to_bit_depth[file.subtype]

def mount_music_packets(blocksize, file_path):
    with sf.SoundFile(file_path) as file:
        try:
            packets_array = []
            filename = file_path.split('/')[-1]
            music_config_packet = bytes([6]) + Utils.serialize_str(filename) + struct.pack('Q', file.samplerate) + struct.pack('Q', file.channels)
            bit_depth = get_bit_depth(file)
            full_blocks = (os.path.getsize(file_path) * bit_depth) // blocksize
            for i in range(full_blocks + 1):
                fragment = bytearray(blocksize)
                file.buffer_read_into(fragment, dtype='float32')
                packet = struct.pack('Q', i) + fragment
                packets_array.append(packet)
            
            return (music_config_packet, packets_array)
        except Exception as e:
            print(type(e).__name__ + ': ' + str(e))

def create_musics_packets(musics, blocksize, folder_path):
    try:
        for filename in os.listdir(folder_path):
            file_path = folder_path + '/' + filename
            music = mount_music_packets(blocksize, file_path)
            musics.append(music)
        return musics
    except Exception as e:
        print(type(e).__name__ + ': ' + str(e))

# Example usage
#blocksize = 1024     # Size of each fragment
#musics_folder = '../musics' 
#musics = create_musics_packets(blocksize, musics_folder)