import threading
import queue
import Socket

class Network:
    def __init__(self, host='', port=0):
        _ = self
        _._host = host
        _._port = port
        _._stop_event = threading.Event()
        _._start_network()

    def _start_network(_):
        try:
            _._callbacks = {}
            _._packet_queue = queue.Queue()
            _._packet_received = threading.Event()

            _._socket = Socket.Socket(_._host, _._port, _._packet_received, _._packet_queue)
            _._host, _._port = _._socket.get_address()
            _._start_threads()

        except:
            raise

    def _start_threads(_):
        _._handle_thread = threading.Thread(target=_._handle_packets)
        _._handle_thread.start()

    def _handle_packets(_):
        while not _._stop_event.is_set():
            _._packet_received.wait()
            packet_type, packet_data, source = _._packet_queue.get()

            if packet_type in _._callbacks:
                _._callbacks[packet_type](packet_data, source)

    def register_callback(_, packet_type, function):
        _._callbacks[packet_type] = function

    def send(_, destination, packet):
        _._socket.send(destination, packet)

    def get_port(_):
        return _._port

    def stop(_):
        _._socket.stop()
        _._stop_event.set()
        _._packet_queue.put((-1, 0, 0))
        _._packet_received.set()
        _._handle_thread.join()

