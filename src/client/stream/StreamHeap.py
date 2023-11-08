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
out_of_order = 0
expected_next = -1
last_played_key = -1      
heap_lock = threading.Lock()

def insert(key, item):
    '''
    Adds a new segment, only if its it has an id bigger than the last 
    (avoids duplication and reproduction of a past segment if it arrives)
    '''
    try:
        global last_played_key, expected_next, out_of_order
        if key not in keys_set:
            keys_set.add(key)

            if key != expected_next:
                out_of_order += 1                                
            expected_next = key + 1

            if key > last_played_key:
                with heap_lock:
                    heapq.heappush(heap, (key, item))
                    last_played_key = key

    except Exception as e:
        raise e

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

def get_missing_keys_cnt():
    return last_key + 1 - len(keys_set)

def get_out_of_order_cnt():
    return out_of_order

def is_empty():
    return len(heap) == 0