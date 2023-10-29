import soundfile as sf
import struct
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

def create_sound_packets(packets_array, blocksize, file_path):
    with sf.SoundFile(file_path) as file:
        try:
            bit_depth = get_bit_depth(file)
            full_blocks = (os.path.getsize(file_path) * bit_depth) // blocksize
            for i in range(full_blocks + 1):
                fragment = bytearray(blocksize)
                file.buffer_read_into(fragment, dtype='float32')
                packet = struct.pack('Q', i) + fragment
                packets_array.append(packet)
                    
        except:
            pass

        return (file.samplerate, file.channels)

# Example usage
#packets_array = []   # Array where fragments should be stored
#blocksize = 1024     # Size of each fragment
#file_path = './music.mp3' 
#create_sound_packets(packets_array, blocksize, file_path)
