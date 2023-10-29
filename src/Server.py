import Watchdog
import Network
import Streaming
import threading
import signal
import struct
import sys
import multiprocessing
import os
import Musics

dict_client = {}
dict_watchdog = {}
children = {}
musics = {}
blocksize = 1024 # Power of two that fits in MTU = 1500

host = ""
port = 0
network = None

def sigint_handler(signum=0, frame=''):
    if network != None:
        network.stop()

    for child in children.values():
        child.terminate()

    for child in children.values():
        child.join()

def child_process(host, lider, musics):
    Streaming.Streaming(host, lider, musics)

def start_new_streaming(source):
    global children

    if source in children:
        children[source].terminate()
        children[source].join()

    children[source] = multiprocessing.Process(target=child_process, args=(host, source, musics))
    children[source].start()

def new_port_request(data, source):
    if len(data) != 0:
        return

    start_new_streaming(source)

def main():
    if len(sys.argv) < 3:
        print("Usage: python Server.py <hostname> <port>")
        exit()

    signal.signal(signal.SIGINT, sigint_handler)

    global host, port, network, musics

    host = sys.argv[1]
    port = sys.argv[2]

    musics_folder = "../musics"
    musics = Musics.Musics(blocksize, musics_folder)

    network = Network.Network(host, port)
    network.register_callback(1, new_port_request)

main()
