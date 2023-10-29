import Network
import Packets

def send_audio_packet(music_packets, network, client, seq):
        packet = music_packets[seq]
        network.send(client, packet)


        
