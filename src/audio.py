from pydub import AudioSegment
import sounddevice as sd
import numpy as np
import threading

# Load your MP3 file
mp3_file = "music.mp3"
audio = AudioSegment.from_file(mp3_file, format="mp3")

# Determine the duration of each segment
segment_duration = 10  # in seconds

# Split the audio into segments
audio_segments = []
for i in range(0, len(audio), segment_duration * 1000):
    segment = audio[i:i + segment_duration * 1000]
    audio_segments.append(segment)

# Function to play the audio segments
def play_audio_segments():
    while audio_segments:
        segment = audio_segments.pop(0)

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

