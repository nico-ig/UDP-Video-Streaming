import sounddevice as sd
from pydub import AudioSegment
import numpy as np

# Load the MP3 file
audio = AudioSegment.from_file("music.mp3", format="mp3")

# Convert the audio to raw PCM format
audio_data = np.array(audio.get_array_of_samples(), dtype=np.int16)
sample_width = audio.sample_width
frame_rate = audio.frame_rate
channels = audio.channels

# Define a callback function to play the audio
def callback(outdata, frames, time, status):
    global audio_data, sample_width, frame_rate, channels
    print(status)
    if len(audio_data) > 0:
        chunk_size = frames * sample_width
        outdata[:] = audio_data[:chunk_size]
        audio_data = audio_data[chunk_size:]

# Start audio playback
with sd.OutputStream(callback=callback, channels=channels, dtype="int16", samplerate=frame_rate):
    pass

