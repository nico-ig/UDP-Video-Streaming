'''
Deals directly with the socket management
'''

import threading
import socket

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


def creates_socket(host, port):
    '''
    Binds a socket to the desired port
    '''
    try:
        local_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host_ip = socket.gethostbyname(host)
        local_socket.bind((host_ip, port))
        host_ip, host_port = local_socket.getsockname()
        return host_ip, host_port, local_socket
            
    except Exception as e:
        raise e

class Socket:
    '''
    Creates and manage a socket
    '''
    def __init__(self, host, port, recv_queue):
        try:
            self.host_name = host 
            self.recv_queue = recv_queue

            self.host_ip, self.host_port, self.local_socket = creates_socket(host, int(port))

            self.stop_event = threading.Event()
            self.receive_thread = Utils.start_thread(self.receive_packets)
            Logger.LOGGER.debug("Binded to address %s", host)

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
                packet, source = self.local_socket.recvfrom(1024)
                packet_type, packet_payload = parse_packet(packet)

                self.recv_queue.put((packet_type, packet_payload, source))

                Logger.LOGGER.debug('Packet received: source: %s, type: %d', source, packet_type)
            except BlockingIOError:
                pass

            except Exception as e:
                Logger.LOGGER.error("An error occurred: %s", str(e))


    def send(self, destination, packet):
        '''
        Sends though the socket the packet to the destination
        '''
        try:
            if self.stop_event.is_set():
                return
            
            destination_host, destination_port = destination

            destination_port = int(destination_port)
            destination_ip = Utils.resolve_name(destination_host)

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