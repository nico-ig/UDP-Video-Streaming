import soundfile as sf
import struct
import numpy as np

def fragment_binary(binary_fragments, blocksize, file_path):
    with sf.SoundFile(file_path) as file:
        try:
            full_blocks = len(file) // blocksize
            last_blocksize = len(file) % blocksize
            blocksize_to_read = blocksize

            for i in range(0, full_blocks + 1 , 1):

                if i == full_blocks + 1:
                    print(blocksize_to_read)
                    blocksize_to_read = last_blocksize

                fragment = file.buffer_read(blocksize_to_read, dtype='float32')
                fragment = np.array(fragment, dtype='float32')
                packet = struct.pack('Q', i) + struct.pack('f' * len(fragment), *fragment)
                binary_fragments.append(packet)
            
        except Exception as e:
            pass

# Example usage
binary_fragments = []   # Array where fragments should be stored
blocksize = 1024       # Size of each fragment
file_path = './music.mp3' 
fragment_binary(binary_fragments, blocksize, file_path)
print(len(binary_fragments))