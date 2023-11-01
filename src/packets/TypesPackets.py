'''
Packets types and it's types value
'''

NEW_PORT_REQUEST = 1    # Client -> Server
PORT_ALLOCATED = 2      # Server -> Client
PORT_ACK = 3            # Client -> Server
REGISTER = 4            # Client -> Server
REGISTER_ACK = 5        # Server -> Client
STREAM_PACKET = 6       # Server -> Client
AVAILABLE_MUSICS = 7    # Server -> Client
MUSIC_REQUEST = 8       # Client -> Server