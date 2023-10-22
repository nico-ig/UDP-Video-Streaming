import threading
import socket

class Socket:
    def __init__(self, host, port, recv_event, recv_queue):
        _ = self;
        _._host = host 
        _._port = port
        _._recv_event = recv_event
        _._recv_queue = recv_queue
        _._start_socket()

    def _start_socket(_):
        _._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _._socket.bind((_._host, _._port))
        _._start_threads()
    
    def _start_threads(_):
        _._receive_thread = threading.Thread(target=_._receive_packets)
        _._receive_thread.daemon = True
        _._receive_thread.start()

    def _parse_packet(_, packet):
        if len(packet) < 2:
            return None, None

        packet_type = packet[0]
        packet_data = packet[1:]
        
        return packet_type, packet_data

    def _receive_packets(_):
        i = 0
        while True:
            packet, origin = _._socket.recvfrom(1024)

            if not packet:
                pass

            packet_type, packet_data = _._parse_packet(packet)
            _._recv_queue.put((packet_type, packet_data))
            _._recv_event.set()

    def send(_, addr, port, packet):
        _._socket.sendto(packet, (addr, port))

