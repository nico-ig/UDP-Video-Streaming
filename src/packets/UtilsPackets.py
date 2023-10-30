"""
Auxiliar packets functions
"""


def mount_byte_packet(byte):
    """
    Mount a packet with a single byte.
    """
    packet = bytes([byte])
    return packet
    
