import Watchdog
import Network
import Utils
import threading
import signal
import struct
import os

is_waiting = False
retries = 0
retries_limit = 10

def sigint_handler(signum=0, frame=''):
    server_watchdog.stop()

    if dedicated_network != None:
        dedicated_network.stop()

    network.stop()

def mount_new_port_request_packet():
    packet = bytes([1])
    return packet

def mount_port_ok_nok_packet(port, status):
    packet = bytes([3]) + struct.pack("!H", port)
    if status == "ok":
        packet += bytes([1])
    else:
        packet += bytes([0])

    return packet

def port_allocated(data, source):
    global retries, is_waiting, retries_limit, dedicated_network
    if len(data) != 0 or is_waiting == False:
        return

    try:
        source_ip, source_port = source
        # MUDAR ISSO QUANDO N FOR LOCALHOST OU ACHAR UM JEITO MAIS INTELIGENTE
        dedicated_network = Network.Network('', source_port+1)
        
        server_watchdog.kick()

        retries = 0
        is_waiting = False

        packet = mount_port_ok_nok_packet(source_port, "ok")
        network.send(server, packet)

    except:
        retries += 1
        if retries < retries_limit:
            server_watchdog.kick()
            packet = mount_port_ok_nok_packet(source_port, "nok")
            network.send(source, packet)
            send_port_request()
        else:
            os.kill(os.getpid(), signal.SIGINT)

def send_port_request():
    packet = mount_new_port_request_packet()
    network.send(server, packet)

    global is_waiting
    is_waiting = True

def main():
    signal.signal(signal.SIGINT, sigint_handler)
    network.register_callback(2, port_allocated)
    network.register_callback(4, Utils.print_func)
    send_port_request()

server = ("127.0.0.1", 12345)
dedicated_network = None
network = Network.Network()
server_watchdog = Watchdog.Watchdog(5, sigint_handler)

main()
