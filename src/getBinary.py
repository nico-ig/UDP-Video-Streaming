import soundfile as sf

def fragment_binary(binary_fragments, blocksize, file_path):
    with sf.SoundFile(file_path) as file:
        try:
            while True: 
                fragment = file.buffer_read(blocksize, dtype='float32')
                if not fragment:
                    break
                binary_fragments.append(fragment)
        except:
            pass

# Example usage
binary_fragments = []   # Array where fragments should be stored
blocksize = 2048        # Size of each fragment
file_path = 'music.mp3' 
fragment_binary(binary_fragments, blocksize, file_path)

print(f"{binary_fragments}")