'''
Creates the audio packets
'''

import os
import struct
import soundfile as SF

from src.utils import Logger as L
from src.network import Utils as NU

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

def mount_single_audio_file_packet(blocksize, file_path):
    try:
        with SF.SoundFile(file_path) as file:
            packets_array = []
            filename = file_path.split('/')[-1]

            audio_config_packet = bytes([NU.AUDIO_CONFIG]) + NU.serialize_str(filename) + struct.pack('Q', file.samplerate) + struct.pack('Q', file.channels) + struct.pack('Q', blocksize)

            bit_depth = get_bit_depth(file)
            full_blocks = (os.path.getsize(file_path) * bit_depth) // blocksize

            for i in range(full_blocks + 1):
                fragment = bytearray(blocksize)
                file.buffer_read_into(fragment, dtype='float32')

                packet = bytes([NU.STREAM]) + struct.pack('Q', i) + fragment
                packets_array.append(packet)
            
            return (audio_config_packet, packets_array)

    except Exception as e:
        L.LOGGER.error("Error while mouting packet for single file: %s", str(e))
        raise Exception("Couldn't mount audio packet for single file")

def mount_audio_packets(blocksize, folder_path):
    try:
        audios = []
    
        for filename in os.listdir(folder_path):
            file_path = folder_path + '/' + filename

            L.LOGGER.info(f"Creating packets for {file_path}")
            packets = mount_single_audio_file_packet(blocksize, file_path)

            audios.append(packets)

        return audios

    except Exception as e:
        L.LOGGER.error("Error while mouting audio packets: %s", str(e))
        raise Exception("Couldn't mount audio packets")