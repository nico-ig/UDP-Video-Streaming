

import heapq
from pydub import AudioSegment
from pydub.playback import play
import io
import time

# This file deals with the Stream Heap
# The Stream Heap is a min heap of tuples (key, item)
# The key is the order of the segment in the file
# The item is the segment itself
class streamPlayer:
    def __init__(self):
        self.streamHeap = []
        self.lastPlayed = -1
        self.lastHeap = -1

    def addToStream(self, key, item):
        if key > self.lastHeap:
            print(self.lastPlayed)
            heapq.heappush(self.streamHeap, (key, item))
            self.lastHeap = key

    def removeFromStream(self):
        segment = self.streamHeap[0][1]
        heapq.heappop(self.streamHeap)
        return segment

    def playStream(self):
        if(len(self.streamHeap)>0):
            segment = AudioSegment.from_mp3(io.BytesIO(self.streamHeap[0][1]))
            print("Playing segment " + str(self.streamHeap[0][0]))
            play(segment)
            self.lastPlayed = self.streamHeap[0][0]
            heapq.heappop(self.streamHeap)

    def playSegment(self, segment):
        play(segment)

# Example of usage (without the client-server part)
# In this case output/output(0-3).mp4 are the fragments of bogos.mp3
player = streamPlayer()

