import threading
import queue
import socket

class Network:
    def __init__(self, port):
        _ = self
        _._start_network(port)

    def register_callback(_, packet_type, function):
        _.callbacks[packet_type] = function

    def _start_network(_, port):
        _.callbacks = {}
        _.packet_queue = queue.Queue()
        _.packet_received = threading.Event()
        _._start_socket(port)
        _._start_network_threads()

    def _start_socket(_, port):
        _.host = "0.0.0.0"
        _.port = port
        _._my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _._my_socket.bind((_.host, _.port))

    def _start_network_threads(_):
        _.network_thread = threading.Thread(target=_._receive_packets)
        _.network_thread.start()

        _.handle_thread = threading.Thread(target=_._handle_packets)
        _.handle_thread.start()

    def _parse_packet(_, packet):
        if len(packet < 2):
            return None, None

        packet_type = packet[0]
        packet_data = packet[1:]
        
        return packet_type, packet_data

    def _receive_packets(_):
        i = 0
        while True:
            packet = _._my_socket.recvfrom(1024)

            if not packet:
                pass

            _.packet_queue.put((packet_type, packet_data))
            _.packet_received.set()

    def _handle_packets(_):
        while True:
            _.packet_received.wait()
            packet_type, packet_data = _.packet_queue.get()

            if packet_type in _.callbacks:
                _.callbacks[packet_type](packet)

def func_a(packet):
    print(f"Received packet: {packet}")

network = Network(12345)
network.register_callback("1", func_a)
