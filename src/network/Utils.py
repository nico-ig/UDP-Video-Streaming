'''
Auxiliar packets functions and flags
'''

import re
import socket
import struct

IPV4 = False

# Packets types and it's types value
OPEN_STREAM_REQUEST = 1 # Client -> Server
STREAM_OPENED = 2       # Server -> Client
AUDIO_ACK = 3           # Client -> Server
REGISTER = 4            # Client -> Server
REGISTER_ACK = 5        # Server -> Client
AUDIO_CONFIG = 6        # Server -> Client
AUDIO_CONFIG_ACK = 7    # Server -> Client
STREAM = 8              # Server -> Client

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

def is_valid_ip_address(address):
    if IPV4 == True:
        ip_pattern = IPV4ADDR
    else:
        ip_pattern = IPV6ADDR
    
    return bool(re.match(ip_pattern, address))

def resolve_name(name):
    '''
    Gets the ipv6 address for a given name
    '''
    try:
        if name == '':
            return '0.0.0.0' if IPV4 == True else '::1'
        if is_valid_ip_address(name):
            return name

        socket_type = socket.AF_INET if IPV4 == True else socket.AF_INET6

        addrinfo = socket.getaddrinfo(name, None, socket_type, socket.SOCK_DGRAM)[0]
        return addrinfo[4][0]

    except Exception as e:
        raise e

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

def parse_packet(packet):
    '''
    Gets the type and the payload from packet
    '''
    try:
        if len(packet) < 1:
            return None, None

        packet_type = packet[0]
        packet_payload = packet[1:]
            
        return packet_type, packet_payload
    
    except Exception as e:
        raise e


def creates_socket(host, port, ipv4):
    '''
    Binds a socket to the desired port
    '''
    try:
        if ipv4 == True:
            local_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            local_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

        host_ip = resolve_name(host)
        local_socket.bind((host_ip, port))
        host_ip, host_port = local_socket.getsockname()[:2]
        return host_ip, host_port, local_socket
            
    except Exception as e:
        raise e

def send_packet_to_clients(network, clients, packet, event=None):
    '''
    Sends a packet to every client
    '''
    try:
        for client in clients:
            network.send(client, packet)

        if event != None:
            event.set()

    except Exception as e:
        raise e