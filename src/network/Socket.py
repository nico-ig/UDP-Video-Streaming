'''
Deals directly with the socket management
'''

import socket
import threading

from src.utils import Utils
from src.utils import Logger as L
from src.network import Utils as NU

class Socket:
    '''
    Creates and manage a socket
    '''
    def __init__(self, host, port, recv_queue, ipv4=False, buffer_size=1024):
        try:
            self.ipv4 = ipv4
            self.host_name = host 
            self.recv_queue = recv_queue
            self.buffer_size = buffer_size
    
            self.host_ip, self.host_port, self.local_socket = NU.creates_socket(host, int(port), ipv4)

            self.stop_event = threading.Event()
            self.receive_thread = Utils.start_thread(self.receive_packets)
            L.LOGGER.debug("Binded to address %s", (self.host_ip, self.host_port))

        except Exception as e:
            L.LOGGER.error("Error while starting socket instanse: %s", str(e))
            raise Exception("Couldn't start socket instanse")

    def receive_packets(self):
        '''
        Callback function that receives the packets and stores them in a queue
        '''
        self.local_socket.setblocking(False)

        while not self.stop_event.is_set():
            try:
                packet, source = self.local_socket.recvfrom(self.buffer_size)
                packet_type, packet_payload = NU.parse_packet(packet)

                self.recv_queue.put((packet_type, packet_payload, source[:2]))

                L.LOGGER.debug('Packet received: source: %s, type: %d, payload len: %d', source[:2], packet_type, len(packet_payload))

            except BlockingIOError:
                pass

            except Exception as e:
                L.LOGGER.error("Error while receiving packets: %s", str(e))


    def send(self, destination, packet):
        '''
        Sends though the socket the packet to the destination
        '''
        try:
            if self.stop_event.is_set():
                return
            
            destination_host, destination_port = destination

            destination_port = int(destination_port)
            destination_ip = NU.resolve_name(destination_host)

            self.local_socket.sendto(packet, (destination_ip, destination_port))
            L.LOGGER.debug('Packet send: destination: %s', destination)
            
        except Exception as e:
            L.LOGGER.error("Error in socket while sending packet: %s", str(e))
            raise Exception("Socket couldn't send packet")

    def get_address(self):
        '''
        Gets the address associated with the socket
        '''
        return self.host_ip, self.host_port

    def get_buffer_size(self):
        '''
        Gets the current buffer size for incoming packets
        '''
        return self.buffer_size
    
    def set_buffer_size(self, new_size):
        '''
        Changes the buffer size of incoming packets
        '''
        self.buffer_size = new_size

    def stop(self):
        ''' 
        Stops the socket
        '''
        try:
            self.stop_event.set()
            self.receive_thread.join()
            self.local_socket.close()

        except Exception as e:
            L.LOGGER.error("Error stoping socket instanse: %s", str(e))
            raise Exception("Couldn't stop socket instanse")
