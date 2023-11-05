'''
 Auxiliar functions for the project
'''

import re
import os
import glob
import struct
import socket
import threading
from datetime import datetime

# Regex for ipv4 and ipv6 addressess
# SRC: https://gist.github.com/syzdek/6086792
IPV4SEG  = f'(25[0-5]|(2[0-4]|1{{0,1}}[0-9]){{0,1}}[0-9])'
IPV4ADDR = f'(IPV4SEG\\.){{3,3}}{IPV4SEG}'
IPV6SEG  = f'[0-9a-fA-F]{{1,4}}'
IPV6ADDR = r'''
    (?: # Start of non-capturing group for IPv6
        (?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4} | # Full IPv6 address
        (?:[0-9a-fA-F]{1,4}:){1,7}: | # IPv6 address with double colons, excluding IPv4
        (?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4} | # IPv6 address with double colons, and one segment
        (?:[0-9a-fA-F]{1,4}:){1,5}:(?:[0-9a-fA-F]{1,4}:){1,2} | # IPv6 address with double colons, and two segments
        (?:[0-9a-fA-F]{1,4}:){1,4}:(?:[0-9a-fA-F]{1,4}:){1,3} | # IPv6 address with double colons, and three segments
        (?:[0-9a-fA-F]{1,4}:){1,3}:(?:[0-9a-fA-F]{1,4}:){1,4} | # IPv6 address with double colons, and four segments
        (?:[0-9a-fA-F]{1,4}:){1,2}:(?:[0-9a-fA-F]{1,4}:){1,5} | # IPv6 address with double colons, and five segments
        [0-9a-fA-F]{1,4}:(?::[0-9a-fA-F]{1,4}){1,6} | # IPv6 address with a single colon, followed by six segments
        ::1 | # IPv6 loopback address
        ::ffff:(0\d{1,3}|1\d{1,3}|2[0-4]\d|25[0-5])\.\d{1,3}\.\d{1,3}\.\d{1,3} | # IPv4-mapped IPv6 address
        (?:[0-9a-fA-F]{1,4}:){1,4}:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} | # IPv4-embedded IPv6 address
        :[0-9a-fA-F]{1,4} # IPv6 address with a single colon, followed by one segment
    ) # End of non-capturing group
''' 

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

def is_valid_ip_address(address, ipv4):
    '''
    Verify if a address is an ip address, shortened adrresses are not supported
    '''
    if ipv4 == True:
        ip_pattern = IPV4ADDR
    else:
        ip_pattern = IPV6ADDR

    return bool(re.match(ip_pattern, address))

def resolve_name(name, ipv4):
    '''
    Gets the ipv6 address for a given name
    '''
    try:
        if name == '':
            return 'localhost'
        
        if is_valid_ip_address(name, ipv4):
            return name

        if ipv4 == True:
            socket_type = socket.AF_INET

        else:
            socket_type = socket.AF_INET6

        addrinfo = socket.getaddrinfo(name, None, socket_type, socket.SOCK_DGRAM)[0]
        return addrinfo[4][0]

    except:
        raise Exception

def is_same_ip(ip1, ip2, ipv4):
    '''
    Verify if two given ip address are the same, 
    despite being a name or a ip address
    '''
    return resolve_name(ip1, ipv4) == resolve_name(ip2, ipv4)

def is_same_address(addr1, addr2, ipv4):
    '''
    Verify if the two address are the same ip address and port
    '''
    addr1_ip, addr1_port = addr1
    addr2_ip, addr2_port = addr2

    return is_same_ip(addr1_ip, addr2_ip, ipv4) and (addr1_port == addr2_port, ipv4)

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

def get_audio_titles(path):
    titles = []
    files = get_audio_files(path)

    for file in files:
        parts = file.replace('.mp3', '').split('_') 
        
        autor = parts[0].replace('-', ' ').title()
        audio = parts[1].replace('-', ' ').title()
        title = autor + ': ' + audio
        titles.append(title)

    return titles

def get_audio_files(path):
    '''
    Returns an array with the audio file names avaiable
    '''
    return [file for file in os.listdir(path) if file.endswith('.mp3')]