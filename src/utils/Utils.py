'''
 Auxiliar functions for the project
'''

import os
import glob
import struct
import socket
import threading
from datetime import datetime

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

def start_thread(callback, daemon=False):
    thread = threading.Thread(target=callback)
    thread.daemon = daemon
    thread.start()

    return thread

def resolve_name(name):
    '''
    Gets the ip address for a given name
    '''
    try:
        ip_addr = socket.gethostbyname(name)
    except:
        ip_addr = name
    finally:
        return ip_addr

def is_same_ip(ip1, ip2):
    '''
    Verify if two given ip address are the same, 
    despite being a name or a ip address
    '''
    return resolve_name(ip1) == resolve_name(ip2)

def is_same_address(addr1, addr2):
    '''
    Verify if the two address are the same ip address and port
    '''
    addr1_ip, addr1_port = addr1
    addr2_ip, addr2_port = addr2

    return is_same_ip(addr1_ip, addr2_ip) and (addr1_port == addr2_port)

def timestamp():
    '''
    Returns a string with the current timestamp
    '''
    return datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

def delete_older_files(path, keep=2):
    '''
    Delete older files, value in keep is how many most recent
    files shouldn't be deleted
    '''
    files = glob.glob(os.path.join(path, "*.log"))
    files.sort(key=lambda file: os.path.getctime(file))

    if keep > 0:
        files = files[:-keep]

    for file in files:
        try:
            os.remove(file)
        except:
            continue