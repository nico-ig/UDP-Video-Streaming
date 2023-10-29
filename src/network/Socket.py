# Deals directly with the socket management

from utils import Utils

import threading
import socket
import os

def resolve_name(name):
    try:
        ip_addr = socket.gethostbyname(name)
    except:
        ip_addr = name
    finally:
        return ip_addr

def parse_packet(packet):
    if len(packet) < 1:
        return None, None

    packet_type = packet[0]
    packet_data = packet[1:]
        
    return packet_type, packet_data

def creates_socket():
    try:
        socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host_ip = socket.gethostbyname(host)
        socket.bind((host_ip, host_port))
        host_ip, host_port = socket.getsockname()
        return host_ip, host_port, socket
        
    except:         
        raise

class Socket:
    def __init__(self, host, port, recv_event, recv_queue):
        self.host_name = host 
        self.recv_event = recv_event
        self.recv_queue = recv_queue
        self.stop_event = threading.Event()
        self.host_ip, self.host_port, self.socket = creates_socket(host, int(port))
        self.receive_thread = Utils.start_thread(self.receive_packets)

    def receive_packets(self):
        i = 0
        self.socket.setblocking(False)
        while not self.stop_event.is_set():
            try:
                packet, source = self.socket.recvfrom(1024)
                packet_type, packet_data = self.parse_packet(packet)
                self.recv_queue.put((packet_type, packet_data, source))
                self.recv_event.set()

            except:
                pass

    def send(self, destination, packet):
        destination_host, destination_port = destination
        destination_port = int(destination_port)
        destination_ip = resolve_name(destination_host)
        self.socket.sendto(packet, (destination_ip, destination_port))

    def get_address(self):
        return self.host_ip, self.host_port

    def stop(self):
        self.socket.close()
        self.stop_event.set()
        self.receive_thread.join()