# Deals with the parsing of the packets (incoming and outgoing) for the server

from src.server import GlobalServer

def parse_new_client(data, source):
    '''
    Parse the requests to start a new stream
    '''
    try:
        if len(data) != 0:
            return

        GlobalServer.LOGGER.info("Parse new client from %s received", source)
        GlobalServer.CLIENTS_QUEUE.put(source)
    
    except Exception as e:
        GlobalServer.LOGGER.error("An error occurred: %s", str(e))
