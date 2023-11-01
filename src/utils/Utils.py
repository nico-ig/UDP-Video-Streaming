'''
 Auxiliar functions for the project
'''

import struct
import threading
import socket

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

def start_thread(callback, args_callback = '', daemon=False):
    if args_callback == '':
        thread = threading.Thread(target=callback)
    else:
        thread = threading.Thread(target=callback, args=(args_callback, ))
        
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