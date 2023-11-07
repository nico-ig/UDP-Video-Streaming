'''
This file deals with the Stream Heap
The Stream Heap is a min heap of tuples (key, item)
The key is the order of the segment in the file
The item is the segment itself
'''

import heapq
import threading

heap = []
keys_set = set()
last_key = -1      
heap_lock = threading.Lock()

def insert(key, item):
    '''
    Adds a new segment, only if its it has an id bigger than the last 
    (avoids duplication and reproduction of a past segment if it arrives)
    '''
    global last_key
    if key > last_key and key not in keys_set:
        with heap_lock:
            heapq.heappush(heap, (key, item))
            keys_set.add(key)
            last_key = key

def remove():
    '''
    Removes a segment from the heap and returns it to be played,
    if the heap is empty, returns seq as -1 and segment with a 0 byte
    '''
    try:
        with heap_lock:
            key, segment = heapq.heappop(heap)
            global last_key
            last_key = key

    except:
        key = -1
        segment = b'\x00'

    finally:
        return (key, segment)