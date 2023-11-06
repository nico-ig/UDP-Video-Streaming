'''
Deals directly with the socket management
'''

import socket
import threading

from src.utils import Logger
from src.utils import Utils

def parse_packet(packet):
    '''
    Gets the type and the payload from packet
    '''
    try:
        if len(packet) < 1:
            return None, None

        packet_type = packet[0]
        packet_payload = packet[1:]
            
        return packet_type, packet_payload
    
    except Exception as e:
        raise e


def creates_socket(host, port, ipv4):
    '''
    Binds a socket to the desired port
    '''
    try:
        if ipv4 == True:
            local_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            local_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

        host_ip = Utils.resolve_name(host, ipv4)
        local_socket.bind((host_ip, port))
        host_ip, host_port = local_socket.getsockname()[:2]
        return host_ip, host_port, local_socket
            
    except Exception as e:
        raise e

class Socket:
    '''
    Creates and manage a socket
    '''
    def __init__(self, host, port, recv_queue, ipv4=False, buffer_size=1024):
        try:
            self.host_name = host 
            self.recv_queue = recv_queue
            self.buffer_size = buffer_size

            self.host_ip, self.host_port, self.local_socket = creates_socket(host, int(port), ipv4)

            self.stop_event = threading.Event()
            self.receive_thread = Utils.start_thread(self.receive_packets)
            Logger.LOGGER.debug("Binded to address %s", (self.host_ip, self.host_port))

        except Exception as e:
            Logger.LOGGER.error("An error occurred: %s", str(e))
            exit()

    def receive_packets(self):
        '''
        Callback function that receives the packets and stores them in a queue
        '''
        self.local_socket.setblocking(False)

        while not self.stop_event.is_set():
            try:
                packet, source = self.local_socket.recvfrom(self.buffer_size)
                packet_type, packet_payload = parse_packet(packet)

                self.recv_queue.put((packet_type, packet_payload, source[:2]))

                Logger.LOGGER.debug('Packet received: source: %s, type: %d, payload len: %d', source[:2], packet_type, len(packet_payload))
            except BlockingIOError:
                pass

            except Exception as e:
                Logger.LOGGER.error("An error occurred: %s", str(e))


    def send(self, destination, packet, ipv4=False):
        '''
        Sends though the socket the packet to the destination
        '''
        try:
            if self.stop_event.is_set():
                return
            
            destination_host, destination_port = destination

            destination_port = int(destination_port)
            destination_ip = Utils.resolve_name(destination_host, ipv4)

            self.local_socket.sendto(packet, (destination_ip, destination_port))
            Logger.LOGGER.debug('Packet send: destination: %s', destination)
            
        except Exception as e:
            Logger.LOGGER.error("An error occurred: %s", str(e))

    def get_address(self):
        '''
        Gets the address associated with the socket
        '''
        try:
            return self.host_ip, self.host_port
        except:
            pass

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
            Logger.LOGGER.error("An error occurred: %s", str(e))