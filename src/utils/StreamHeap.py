# Deals with stream heap management
import heapq
import threading

# This file deals with the Stream Heap
# The Stream Heap is a min heap of tuples (key, item)
# The key is the order of the segment in the file
# The item is the segment itself
class StreamHeap:
    def __init__(self):
        self.stream_heap = []
        self.last_heap = -1      
        self.heap_lock = threading.Lock()

    def add_to_buffer(self, key, item):
        '''
        Adds a new segment, only if its it has an id bigger than the last 
        (avoids duplication and reproduction of a past segment if it arrives)
        '''
        if key > self.last_heap:
            with self.heap_lock:
                heapq.heappush(self.stream_heap, (key, item))
                self.last_heap = key

    def remove_from_buffer(self):
        '''
        Removes a segment from the stream and returns it to be played,
        if the heap is empty, returns seq as -1 and segment with a 0 byte
        '''
        key = -1
        segment = b'\x00'
        try:
            with self.heap_lock:
                key, segment = heapq.heappop(self.stream_heap)
                self.last_heap = key

        except:
            pass

        finally:
            return (key, segment)