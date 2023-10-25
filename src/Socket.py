import threading
import socket
import os

class Socket:
    def __init__(self, host, port, recv_event, recv_queue):
        _ = self;
        _._host = host 
        _._host_ip = socket.gethostbyname(_._host)
        _._port = int(port)
        _._recv_event = recv_event
        _._recv_queue = recv_queue
        _._stop_event = threading.Event()
        _._start_socket()

    def _start_socket(_):
        try:
            _._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            _._socket.bind((_._host_ip, _._port))
            _._host_ip, _._port = _._socket.getsockname()
            _._start_threads()
        
        except:         
            raise

    def _start_threads(_):
        _._receive_thread = threading.Thread(target=_._receive_packets)
        _._receive_thread.start()

    def _parse_packet(_, packet):
        if len(packet) < 1:
            return None, None

        packet_type = packet[0]
        packet_data = packet[1:]
        
        return packet_type, packet_data

    def _receive_packets(_):
        i = 0
        _._socket.setblocking(False)
        while not _._stop_event.is_set():
            try:
                packet, source = _._socket.recvfrom(1024)
                print(f"Packet received by process {os.getpid()} in port {_._port}")
                packet_type, packet_data = _._parse_packet(packet)
                _._recv_queue.put((packet_type, packet_data, source))
                _._recv_event.set()

            except:
                pass

    def resolve_name(_, name):
        try:
            ip_addr = socket.gethostbyname(name)
        except:
            ip_addr = name
        finally:
            return ip_addr

    def send(_, destination, packet):
        destination_host, destination_port = destination
        destination_port = int(destination_port)
        destination_ip = _.resolve_name(destination_host)
        _._socket.sendto(packet, (destination_ip, destination_port))

    def get_address(_):
        return _._host, _._port

    def stop(_):
        _._socket.close()
        _._stop_event.set()
        _._receive_thread.join()

