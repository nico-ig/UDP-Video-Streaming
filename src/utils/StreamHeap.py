# Deals with stream heap management
import heapq
from pydub import AudioSegment
from pydub.playback import play

# This file deals with the Stream Heap
# The Stream Heap is a min heap of tuples (key, item)
# The key is the order of the segment in the file
# The item is the segment itself
class stream_player:
    def __init__(self):
        self.stream_heap = []
        self.last_heap = -1      

    # Adds a new segment, only if its it has an id bigger than the last 
    # (avoids duplication and reproduction of a past segment if it arrives)
    def add_to_stream(self, key, item):
        if key > self.last_heap:
            heapq.heappush(self.stream_heap, (key, item))
            self.last_heap = key

    # Removes a segment from the stream and returns it to be played
    def remove_from_stream(self):
        key = self.stream_heap[0][0]
        segment = self.stream_heap[0][1]
        self.lastPlayed = self.stream_heap[0][0]
        heapq.heappop(self.stream_heap)
        return (key, segment)

    # Plays a single segment of the stream
    def play_segment(self, segment):
        play(segment)
