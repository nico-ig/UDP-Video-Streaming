"""
Deals directly with the socket management
"""

from utils import Logger
from utils import Utils

import threading
import socket

def resolve_name(name):
    """
    Gets the ip address for a given name
    """
    try:
        ip_addr = socket.gethostbyname(name)
    except:
        ip_addr = name
    finally:
        return ip_addr

def parse_packet(packet):
    """
    Gets the type and the payload from packet
    """
    try:
        if len(packet) < 1:
            return None, None

        packet_type = packet[0]
        packet_payload = packet[1:]
            
        return packet_type, packet_payload
    
    except Exception as e:
        raise e


def creates_socket(host, port):
    """
    Binds a socket to the desired port
    """
    try:
        socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host_ip = socket.gethostbyname(host)
        socket.bind((host_ip, port))
        host_ip, host_port = socket.getsockname()
        return host_ip, host_port, socket
            
    except Exception as e:
        raise e

class Socket:
    """
    Creates and manage a socket
    """
    def __init__(self, host, port, recv_event, recv_queue):
        try:
            self.logger = Logger.get_logger('socket')

            self.host_name = host 
            self.recv_event = recv_event
            self.recv_queue = recv_queue

            self.host_ip, self.host_port, self.socket = creates_socket(host, int(port))

            self.stop_event = threading.Event()
            self.receive_thread = Utils.start_thread(self.receive_packets)

        except Exception as e:
            error_message = 'Error creating socket - ' + type(e)+ ': ' + str(e)
            self.logger.error(error_message)

    def receive_packets(self):
        """
        Callback function that receives the packets and stores them in a queue
        """
        try:
            i = 0
            self.socket.setblocking(False)

            while not self.stop_event.is_set():
                packet, source = self.socket.recvfrom(1024)
                packet_type, packet_data = self.parse_packet(packet)

                self.recv_queue.put((packet_type, packet_data, source))
                self.recv_event.set()

                self.logger.info('Packet received, source: %s, type: %d, content: %s', source, packet_type, packet_data)

        except:
            pass

    def send(self, destination, packet):
        """
        Sends though the socket the packet to the destination
        """
        try:
            destination_host, destination_port = destination

            destination_port = int(destination_port)
            destination_ip = resolve_name(destination_host)

            self.socket.sendto(packet, (destination_ip, destination_port))

        except Exception as e:
            error_message = 'Error sending packet - ' + type(e)+ ': ' + str(e)
            self.logger.error(error_message)

    def get_address(self):
        """
        Gets the address associated with the socket
        """
        try:
            return self.host_ip, self.host_port
        except:
            pass

    def stop(self):
        """ 
        Stops the socket
        """
        try:
            self.socket.close()
            self.stop_event.set()
            self.receive_thread.join()

        except Exception as e:
            error_message = 'Error stopping socket - ' + type(e)+ ': ' + str(e)
            self.logger.error(error_message)