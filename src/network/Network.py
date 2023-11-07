'''
Deals with forwarding packets and incoming packets callbacks
'''
import threading
import queue

from src.utils import Logger
from src.utils import Utils
from src.network import Socket
from src.network import Utils as NU

class Network:
    '''
    Creates and manages the network interface
    '''
    def __init__(self, ipv4=False, host='', port=0):
        try:
            self.stop_event = threading.Event()
            self.callbacks = {}
            self.packet_queue = queue.Queue()
            self.packet_received = threading.Event()

            self.socket = Socket.Socket(host, port, self.packet_queue, ipv4)
            self.host_ip, self.host_port = self.socket.get_address()

            self.handle_thread = Utils.start_thread(self.handle_packets)
        except Exception as e:
            Logger.LOGGER.error("An error occurred: %s", str(e))
            raise Exception("Couldn't start network")

    def handle_packets(self):
        '''
        Callback function to handle received packets
        '''
        try:
            while not self.stop_event.is_set():

                packet_type, packet_data, source = self.packet_queue.get()

                if packet_type in self.callbacks:
                    self.callbacks[packet_type](packet_data, source)
        except:
            pass

    def register_callback(self, packet_type, function):
        '''
        Register a callback function for a given type
        '''
        try:
            self.callbacks[packet_type] = function
            Logger.LOGGER.debug("Callback %s registered for type %d", function.__name__, packet_type)
        except:
            pass

    def unregister_callback(self, packet_type):
        '''
        Unregister a callback function for a given type
        '''
        try:
            del self.callbacks[packet_type]
            Logger.LOGGER.debug("Callback unregistered for type %d", packet_type)
        except:
            pass

    def send(self, destination, packet):
        '''
        Sends a packet to a destination
        '''
        try:
            if self.stop_event.is_set():
                return

            self.socket.send(destination, packet)
        except:
            pass

    def get_port(self):
        '''
        Gets the port associate with the network interface
        '''
        try:
            ip, port = self.socket.get_address()
            return port
        except:
            pass

    
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
            Logger.LOGGER.error("An error occurred: %s", str(e))
