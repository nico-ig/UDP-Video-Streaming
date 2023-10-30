# Deals with recieving packets and adding them to the stream_heap

def callbacks(packet):
    packet_type = packet[0]
    
    '''
    Descobrir como fazer um switch case em python
    '''
    if packet_type == 1:
        #port_request()
        pass
    elif packet_type == 2:
        #port_allocated()
        pass
    elif packet_type == 3:
        #port_ok_nok()
        pass
    elif packet_type == 4:
        #registration
        pass
    elif packet_type ==5:
        print_available_musics(packet[1])
    elif packet_type == 6:
        # Music Choice 
        # send_music_choice()
        pass

def print_available_musics(music_list):
    print("Available musics:")


#### Dont forget to unregister from other packet types no longer relevants