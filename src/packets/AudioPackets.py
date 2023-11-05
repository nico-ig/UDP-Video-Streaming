'''
Creates the audio packets
'''

import os
import struct
import soundfile as sf

from src.utils import Utils

from src.packets import TypesPackets

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
    with sf.SoundFile(file_path) as file:
        packets_array = []
        filename = file_path.split('/')[-1]

        audio_config_packet = bytes([TypesPackets.AUDIO_CONFIG]) + Utils.serialize_str(filename) + struct.pack('Q', file.samplerate) + struct.pack('Q', file.channels) + struct.pack('Q', blocksize)

        bit_depth = get_bit_depth(file)
        full_blocks = (os.path.getsize(file_path) * bit_depth) // blocksize

        for i in range(full_blocks + 1):
            fragment = bytearray(blocksize)
            file.buffer_read_into(fragment, dtype='float32')

            packet = bytes([TypesPackets.STREAM]) + struct.pack('Q', i) + fragment
            packets_array.append(packet)
        
        return (audio_config_packet, packets_array)

def mount_audio_packets(blocksize, folder_path, logger):
    audios = []

    for filename in os.listdir(folder_path):
        file_path = folder_path + '/' + filename

        logger.info(f"Creating packets for {file_path}")
        packets = mount_single_audio_file_packet(blocksize, file_path)

        audios.append(packets)

    return audios
