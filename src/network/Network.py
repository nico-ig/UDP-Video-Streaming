'''
Deals with forwarding packets and incoming packets callbacks
'''
import queue
import threading

from src.utils import Utils
from src.network import Socket
from src.utils import Logger as L
from src.network import Utils as NU

class Network:
    '''
    Creates and manages the network interface
    '''
    def __init__(self, ipv4=False, host='::', port=0):
        try:
            NU.IPV4 = ipv4

            self.stop_event = threading.Event()
            self.callbacks = {}
            self.packet_queue = queue.Queue()
            self.packet_received = threading.Event()
            
            host = host if host != '' else NU.get_wildchar_addr()
            self.socket = Socket.Socket(host, port, self.packet_queue, ipv4)
            self.host_ip, self.host_port = self.socket.get_address()

            self.handle_thread = Utils.start_thread(self.handle_packets)

        except Exception as e:
            L.LOGGER.error("Error while starting network instanse: %s", str(e))
            raise Exception("Couldn't start network instanse")

    def handle_packets(self):
        '''
        Callback function to handle received packets
        '''
        try:
            while not self.stop_event.is_set():

                packet_type, packet_data, source = self.packet_queue.get()

                if packet_type in self.callbacks:
                    self.callbacks[packet_type](packet_data, source)

        except Exception as e:
            L.LOGGER.error(f"Error in network callback: {str(e)}")
            raise Exception("Couldn't execute network callback")

    def register_callback(self, packet_type, function):
        '''
        Register a callback function for a given type
        '''
        try:
            self.callbacks[packet_type] = function
            L.LOGGER.debug("Callback %s registered for type %d", function.__name__, packet_type)

        except Exception as e:
            L.LOGGER.error(f"Error registering network callback: {str(e)}")
            raise Exception("Couldn't register network callback")

    def unregister_callback(self, packet_type):
        '''
        Unregister a callback function for a given type
        '''
        try:
            del self.callbacks[packet_type]
            L.LOGGER.debug("Callback unregistered for type %d", packet_type)

        except Exception as e:
            L.LOGGER.error(f"Error unregistering network callback: {str(e)}")
            raise Exception("Couldn't unregister network callback")

    def send(self, destination, packet):
        '''
        Sends a packet to a destination
        '''
        try:
            if self.stop_event.is_set():
                return

            self.socket.send(packet, destination)

        except Exception as e:
            L.LOGGER.error("Error in network while sending packet: %s", str(e))
            raise Exception("Network couldn't send packet")

    def get_port(self):
        '''
        Gets the port associate with the network interface
        '''
        ip, port = self.socket.get_address()
        return port
    
    def get_buffer_size(self):
        '''
        Gets the current buffer size for incoming packets
        '''
        return self.socket.get_buffer_size()
    
    def set_buffer_size(self, new_size):
        '''
        Changes the buffer size of incoming packets
        '''
        self.socket.set_buffer_size(new_size)

    def set_send_buffer_size(self, new_size):
        '''
        Changes the size of send buffer
        '''
        self.socket.set_send_buffer_size(new_size)


    def stop(self):
        '''
        Stops the network interface
        '''
        try:
            self.stop_event.set()
            self.packet_received.set()
            self.packet_queue.put((-1, 0, 0))
            self.handle_thread.join()
            self.socket.stop()

        except Exception as e:
            L.LOGGER.error("Error stoping network instanse: %s", str(e))
            raise Exception("Couldn't stop network instanse")
