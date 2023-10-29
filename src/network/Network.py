"""
Deals with forwarding packets and incoming packets callbacks
"""

import Socket
from utils import Logger
from utils import Utils

import threading
import queue

class Network:
    """
    Creates and manages the network interface
    """
    def __init__(self, host='', port=0):
        try:
            self.logger = Logger.get_logger('network')

            self.stop_event = threading.Event()
            self.callbacks = {}
            self.packet_queue = queue.Queue()
            self.packet_received = threading.Event()

            self.socket = Socket.Socket(host, port, self.packet_received, self.packet_queue)
            self.host_ip, self.host_port = self.socket.get_address()

            self.handle_thread = Utils.start_thread(self.handle_packets)

        except Exception as e:
            error_message = 'Error creating network interface - ' + type(e)+ ': ' + str(e)
            self.logger.error(error_message)

    def handle_packets(self):
        """
        Callback function to handle received packets
        """
        try:
            while not self.stop_event.is_set():
                self.packet_received.wait()
                packet_type, packet_data, source = self.packet_queue.get()

                if packet_type in self.callbacks:
                    self.callbacks[packet_type](packet_data, source)
        except:
            pass

    def register_callback(self, packet_type, function):
        """
        Register a callback function to a given type
        """
        try:
            self.callbacks[packet_type] = function
            message = f"{function.__name__} registered for type {packet_type}"
            self.logger.info(message)
        except:
            pass

    def unregister_callback(self, packet_type):
        """
        Unregister a callback function to a given type
        """
        try:
            del self.callbacks[packet_type]
            message = f"{function.__name__} unregistered for type {packet_type}"
            self.logger.info(message)
        except:
            pass

    def send(self, destination, packet):
        """
        Sends a packet to a destination
        """
        try:
            self.socket.send(destination, packet)
        except:
            pass

    def get_port(self):
        """
        Gets the port associate with the network interface
        """
        try:
            return self.port
        except:
            pass

    def stop(self):
        """
        Stops the network interface
        """
        try:
            self.socket.stop()
            self.stop_event.set()
            self.packet_queue.put((-1, 0, 0))
            self.packet_received.set()
            self.handle_thread.join()
        except Exception as e:
            error_message = 'Error stopping network interface - ' + type(e)+ ': ' + str(e)
            self.logger.error(error_message)
