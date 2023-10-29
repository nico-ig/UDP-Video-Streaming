# Auxiliar functions for the project

def start_threads(callback, args_callback = ''):
    thread = threading.Thread(target=callback, args=(args_callback, ))
    thread.start()
    return thread