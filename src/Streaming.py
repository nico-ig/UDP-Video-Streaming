import Network
import Watchdog
import threading
import signal
import struct
import os

class Streaming:
    def __init__(self, host, lider, musics):
        self.host = host
        self.lider = lider
        self.musics = musics
        self.clients = set()
        self.start_event = threading.Event()
        self.network = Network.Network(self.host)
        signal.signal(signal.SIGINT, self.sigint_handler)
        self.start()

    def start(self):
        self.send_port_allocated()
        self.network.register_callback(3, self.new_port_ok)
        self.network.register_callback(4, self.new_client)
        self.start_streaming()

    def send_port_allocated(self):
        packet = self.mount_port_allocated_packet()
        self.network.send(self.lider, packet)
        self.watchdog = Watchdog.Watchdog(5, self.sigint_handler)

    def mount_port_allocated_packet(self):
        packet = bytes([2])
        return packet

    def new_port_ok(self, data, source):
        if len(data) != 0:
            return

        source_ip, source_port = source
        lider_ip, lider_port = self.lider

        if source_ip != lider_ip:
            self.sigint_handler()

###### Derregistrar o tipo 3
        self.watchdog.stop()
        self.watchdog = Watchdog.Watchdog(15, self.register_finished)

    def new_client(self, data, source):
        if len(data) != 0:
            return

        self.clients.add(source)
        packet = bytes([5])
        self.network.send(source, packet) 

    def register_finished(self, self_watchdog):
        self.network.stop()
        self.start_event.set()

    def start_streaming(self):
        while not self.start_event.is_set():
            pass

        print("Should start streaming, clients registered are:")
        for (music_config, music_packet) in self.musics:
            print(music_config)
        for client in self.clients:
            print(client)
        self.watchdog.stop()

    def sigint_handler(self, self_watchdog=""):
        self.network.stop()
