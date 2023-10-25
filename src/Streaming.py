import Network
import Watchdog
import threading
import signal
import struct
import os

class Streaming:
    def __init__(self, host, lider):
        _ = self
        _._host = host
        _._lider = lider
        _.clients = set()
        _.start_event = threading.Event()
        _._network = Network.Network(_._host)
        signal.signal(signal.SIGINT, _.sigint_handler)
        _._start()

    def _start(_):
        _._send_port_allocated()
        _._network.register_callback(3, _.new_port_ok)
        _._network.register_callback(4, _.new_client)
        _._start_streaming()

    def _send_port_allocated(_):
        packet = _._mount_port_allocated_packet()
        _._network.send(_._lider, packet)
        _._watchdog = Watchdog.Watchdog(5, _.sigint_handler)

    def _mount_port_allocated_packet(_):
        packet = bytes([2])
        return packet

    def new_port_ok(_, data, source):
        if len(data) != 0:
            return

        source_ip, source_port = source
        lider_ip, lider_port = _._lider

        if source_ip != lider_ip:
            _.sigint_handler()

###### Derregistrar o tipo 3
        _._watchdog.stop()
        _._watchdog = Watchdog.Watchdog(15, _.register_finished)

    def new_client(_, data, source):
        if len(data) != 0:
            return

        _.clients.add(source)
        packet = bytes([5])
        _._network.send(source, packet) 

    def register_finished(_, self):
        _._network.stop()
        _.start_event.set()

    def _start_streaming(_):
        while not _.start_event.is_set():
            pass

        print("Should start streaming, clients registered are:")
        for client in _.clients:
            print(client)
        _._watchdog.stop()

    def sigint_handler(_, self=""):
        _._network.stop()
