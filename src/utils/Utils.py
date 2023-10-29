# Auxiliar functions for the project

import struct
import threading

def serialize_str(stri):
    data = struct.pack('Q', len(stri))
    data += stri.encode("utf-8")
    return data

def deserialize_str(packet):
    length = struct.unpack('Q', packet[:8])[0]
    packet = packet[8:]
    msg = packet[:length].decode("utf-8")
    packet = packet[length:]
    return msg, packet

def start_thread(callback, args_callback = ''):
    thread = threading.Thread(target=callback, args=(args_callback, ))
    thread.start()
    return thread