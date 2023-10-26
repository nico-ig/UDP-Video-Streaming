from pydub import AudioSegment
import sounddevice as sd
import numpy as np
import threading
import streamHeap as sh

# Load your MP3 file
mp3_file = "music.mp3"
audio = AudioSegment.from_file(mp3_file, format="mp3")


# Determine the duration of each segment
segment_duration = 2  # in seconds

# Split the audio into segments
audioSegments = sh.streamPlayer()

for i in range(0, len(audio), segment_duration * 1000):
    segment = audio[i:i + segment_duration * 1000]
    audioSegments.addToStream(i, segment)

# Function to play the audio segments
def play_audio_segments():
    while audioSegments.streamHeap:
        segment = audioSegments.removeFromStream()

        # Convert the segment to a NumPy array with the correct data type
        audio_data = np.array(segment.get_array_of_samples(), dtype=np.int16)

        # Play the audio segment
        sd.play(audio_data, 90000)
        sd.wait()

# Create a thread for playing audio segments
audio_thread = threading.Thread(target=play_audio_segments)
audio_thread.daemon = True  # The thread will exit when the main program exits

# Start the audio thread
audio_thread.start()

# Wait for the audio thread to finish (remove this line if not needed)
audio_thread.join()

