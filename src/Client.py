import Watchdog
import Network
import Utils
import threading

def callback(data):
    watchdog.kick_watchdog()
    Utils.print_func(data)

server_addr = "127.0.0.1"
port = 12345

network = Network.Network("127.0.0.1", 12346)
watchdog = Watchdog.Watchdog(5)

network.register_callback(1, callback)
packet = Utils.serialize_str("Pacote enviado pelo cliente")
network.send(server_addr, port, packet)
