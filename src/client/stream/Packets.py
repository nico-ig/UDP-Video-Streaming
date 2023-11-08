'''
Deals with the stream packets
'''

import struct
import threading

from src.utils import Logger as L
from src.client import Globals as G
from src.network import Utils as NU
from src.client.stream import StreamHeap as SH

STREAM_STARTED = threading.Event()
G.STOP_EVENTS.append(STREAM_STARTED)

def parse_stream_packets(payload, source):
    '''
    Add a packet to the stream buffer
    '''
    try:
        if not NU.is_same_address(G.SERVER, source):
            return

        if len(payload) < 9:
            return

        seq = struct.unpack('Q', payload[:8])[0]
        SH.insert(seq, payload[8:])

        STREAM_STARTED.set()

        if G.STREAM_TIMER != None:
            G.STREAM_TIMER.kick()

    except Exception as e:
        L.LOGGER.error("Error parsing stream packet: %s", str(e))