import os
import Packets

class Musics:
    def __init__(self, blocksize, folder_path):
        self.musics = Packets.create_musics_packets(blocksize, folder_path)

