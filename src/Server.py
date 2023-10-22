import Watchdog
import Network
import Utils
import threading

def callback(data):
    watchdog.kick_watchdog()
    Utils.print_func(data)
    packet = Utils.serialize_str("Pacote enviado pelo servidor")
    network.send(host, 12346, packet)

host = "127.0.0.1"
port = 12345

this_thread = threading.current_thread

network = Network.Network(host, port)
watchdog = Watchdog.Watchdog(5)
network.register_callback(1, callback)
