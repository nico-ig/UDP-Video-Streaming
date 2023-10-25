import Watchdog
import Network
import Utils
import threading
import signal
import struct
import os
import sys

network = None
server_watchdog = None
server = None

def sigint_handler(signum=0, frame=''):
    if server_watchdog != None:
        server_watchdog.stop()

    if network != None:
        network.stop()

def mount_new_port_request_packet():
    packet = bytes([1])
    return packet

def mount_port_ok_packet():
    packet = bytes([3])
    return packet

def send_registration_packet(destination):
    packet = bytes([4])
    print(f"Sending packet {packet} to {destination}")
    network.send(destination, packet)

def port_allocated(data, source):
    if len(data) != 0:
        return

    server_watchdog.kick()
    packet = mount_port_ok_packet()
    network.send(source, packet)
##### Desrregistrar o tipo 2
    send_registration_packet(source)

def send_port_request():
    packet = mount_new_port_request_packet()
    network.send(server, packet)

def main():
    if len(sys.argv) < 3:
        print("Usage: python Client.py <Server Name> <Server Port> -j")
        exit()

    signal.signal(signal.SIGINT, sigint_handler)

    global host, port, network, server_watchdog, server

    server_name = sys.argv[1]
    server_port = sys.argv[2]
    server = (server_name, server_port)
    
    network = Network.Network()
    server_watchdog = Watchdog.Watchdog(5, sigint_handler)

    if len(sys.argv) == 4 and sys.argv[3] == "-j":
        send_registration_packet(server)

    else:
        send_port_request()
        network.register_callback(2, port_allocated)

main()
