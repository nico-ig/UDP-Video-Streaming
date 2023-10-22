import threading
import queue
import Socket

class Network:
    def __init__(self, host, port):
        _ = self
        _._host = host
        _._port = port
        _._start_network()

    def _start_network(_):
        _._callbacks = {}
        _._packet_queue = queue.Queue()
        _._packet_received = threading.Event()
        _._socket = Socket.Socket(_._host, _._port, _._packet_received, _._packet_queue)
        _._start_threads()

    def _start_threads(_):

        _._handle_thread = threading.Thread(target=_._handle_packets)
        _._handle_thread.daemon = True
        _._handle_thread.start()

    def _handle_packets(_):
        while True:
            _._packet_received.wait()
            packet_type, packet_data = _._packet_queue.get()

            if packet_type in _._callbacks:
                _._callbacks[packet_type](packet_data)

    def register_callback(_, packet_type, function):
        _._callbacks[packet_type] = function

    def send(_, addr, port, packet):
        _._socket.send(addr, port, packet)
