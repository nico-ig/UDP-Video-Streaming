# Deals with forwarding packets and incoming packets callbacks

import Socket
from utils import Utils

import threading
import queue
import os

class Network:
    def __init__(self, host='', port=0):
        try:
            self.stop_event = threading.Event()
            self.callbacks = {}
            self.packet_queue = queue.Queue()
            self.packet_received = threading.Event()
            self.socket = Socket.Socket(host, port, self.packet_received, self.packet_queue)
            self.host_ip, self.host_port = self.socket.get_address()
            self.handle_thread = Utils.start_thread(self.handle_packets)

        except:
            raise

    def handle_packets(self):
        while not self.stop_event.is_set():
            self.packet_received.wait()
            packet_type, packet_data, source = self.packet_queue.get()

            if packet_type in self.callbacks:
                self.callbacks[packet_type](packet_data, source)

    def register_callback(self, packet_type, function):
        self.callbacks[packet_type] = function

    def unregister_callback(self, packet_type):
        del self.callbacks[packet_type]

    def send(self, destination, packet):
        self.socket.send(destination, packet)

    def get_port(self):
        return self.port

    def stop(self):
        self.socket.stop()
        self.stop_event.set()
        self.packet_queue.put((-1, 0, 0))
        self.packet_received.set()
        self.handle_thread.join()
