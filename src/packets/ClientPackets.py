# Deals with the parsing of the packets (incoming and outgoing)
def mount_new_port_request_packet():
    packet = bytes([1])
    return packet

def mount_port_ok_packet():
    packet = bytes([3])
    return packet