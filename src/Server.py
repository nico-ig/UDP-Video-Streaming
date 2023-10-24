import Watchdog
import Network
import Utils
import threading
import signal
import struct

dict_client = {}
dict_watchdog = {}

host = "127.0.0.1"
port = 12345

network = Network.Network(host, port)

def sigint_handler(signum=0, frame=''):
    network.stop()
    for (client_network, client_watchdog) in dict_client.values():
        client_network.stop()
        client_watchdog.stop()

def client_timedout(self):
    source_ip = dict_watchdog[self]

    client_network, client_watchdog = dict_client[source_ip]
    client_network.stop()
    client_watchdog.stop()

    del dict_client[source_ip]
    del dict_watchdog[self]

def mount_port_allocated_packet():
    packet = bytes([2])
    return packet

def new_port_request(data, source):
    if len(data) != 0:
        return

    source_ip, source_port = source

    if source_ip not in dict_client:
        client_network = Network.Network(host)
        client_watchdog = Watchdog.Watchdog(5, client_timedout)
        dict_client[source_ip] = (client_network, client_watchdog)
        dict_watchdog[client_watchdog] = source_ip

    client_network, client_watchdog = dict_client[source_ip]
    client_watchdog.kick()
    packet = mount_port_allocated_packet()

    client_network.send(source, packet)

def parse_port_ok_nok_packet(data):
    port = data[0:2]
    port = struct.unpack("!H", port)
    status = data[2]
    return port[0], status

def new_port_ok_nok(data, source):
    if len(data) != 3:
        return

    source_ip, source_port = source
    client_network, client_watchdog = dict_client[source_ip]

    port, status = parse_port_ok_nok_packet(data)
    if client_network.get_port() != port:
        return

    client_watchdog.stop()

    if status == 1:
        print("Should start transmission but not implemented yet")
        packet = bytes([4]) + Utils.serialize_str("Testing sending a packet to client through the dedicated port")
        source_ip, source_port = source
        source = (source_ip, source_port)
        client_network.send(source, packet)

    #Mover isso para junto do client_watchdog.stop() depois
    client_network.stop()

def main():
    signal.signal(signal.SIGINT, sigint_handler)
    network.register_callback(1, new_port_request)
    network.register_callback(3, new_port_ok_nok)

main()
