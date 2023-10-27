

import heapq
from pydub import AudioSegment
from pydub.playback import play
import io
import time

# This file deals with the Stream Heap
# The Stream Heap is a min heap of tuples (key, item)
# The key is the order of the segment in the file
# The item is the segment itself
class stream_player:
    def __init__(self):
        self.streamHeap = []
        self.lastPlayed = -1
        self.lastHeap = -1

    # Adds a new segment, only if its it has an id bigger than the last 
    # (avoids duplication and reproduction of a past segment if it arrives)
    def add_to_stream(self, key, item):
        if key > self.lastHeap:
            heapq.heappush(self.streamHeap, (key, item))
            self.lastHeap = key

    # Removes a segment from the stream and returns it to be played
    def remove_from_stream(self):
        segment = self.streamHeap[0][1]
        self.lastPlayed = self.streamHeap[0][0]
        heapq.heappop(self.streamHeap)
        return segment

    # Plays a single segment of the stream
    def play_segment(self, segment):
        play(segment)



