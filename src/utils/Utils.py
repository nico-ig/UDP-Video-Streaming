'''
 Auxiliar functions for the project
'''

import os
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

def capture_alsa():
    '''
    Change the alsa config
    '''
    pass
    # try:
    #     asoundrc_path = os.path.expanduser('~') + '/.asoundrc'

    #     if os.path.isfile(asoundrc_path):
    #         bkp_path = asoundrc_path + '_bkp'
    #         os.system(f'cp {asoundrc_path} {bkp_path}')

    #     os.system(f'cat ./config/asoundrc >> {asoundrc_path}')

    #     with open(asoundrc_path, "r") as config_file:
    #         log_path = os.getcwd() + '/logs/alsa/' + timestamp()
    #         os.system(f'touch {log_path}')
    #         alsa_config = config_file.read()
    #         alsa_config = alsa_config.replace("<log_path>", log_path)

    #     with open(asoundrc_path, "w") as config_file:
    #         config_file.write(alsa_config)

    # except Exception as e:
    #     print("An error occurred: %s", str(e))

def restore_alsa():
    '''
    Restore the alsa config
    '''
    pass
    # try:
    #     asoundrc_path = os.path.expanduser('~') + '/.asoundrc'
    #     bkp_path = asoundrc_path + '_bkp'

    #     if os.path.isfile(bkp_path):
    #         os.system(f'cp {bkp_path} {asoundrc_path}')
    #         os.remove(bkp_path)
    #     else:
    #         os.remove(asoundrc_path)

    # except Exception as e:
    #     print("An error occurred: %s", str(e))
