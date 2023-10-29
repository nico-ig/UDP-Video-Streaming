
from src.packets import ClientPackets

def send_registration_packet(destination):
    packet = bytes([4])
    print(f"Sending packet {packet} to {destination}")
    network.send(destination, packet)

def port_allocated(data, source):
    if len(data) != 0:
        return

    server_timer.kick()
    packet = ClientPackets.mount_port_ok_packet()
    network.send(source, packet)
##### Desrregistrar o tipo 2
    send_registration_packet(source)

def send_port_request(network, server):
    packet = ClientPackets.mount_new_port_request_packet()
    network.send(server, packet)

def client_handshake(network, server, server_timer, logger, option):
    if option == 'join':
        send_registration_packet(network, server)

    else:
        send_port_request(network, server)
        network.register_callback(2, port_allocated)