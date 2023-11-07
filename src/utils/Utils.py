'''
 Auxiliar functions for the project
'''

import os
import glob
import threading
from datetime import datetime

def start_thread(callback, daemon=False):
    try:
        thread = threading.Thread(target=callback)
        thread.daemon = daemon
        thread.start()

        return thread

    except Exception as e:
        raise Exception("Couldn't start thread: %s", str(e))

def timestamp():
    '''
    Returns a string with the current timestamp
    '''
    return datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

def delete_older_files(path, keep=2):
    '''
    Delete older files, value in keep is how many most recent
    files shouldn't be deleted
    '''
    try:
        files = glob.glob(os.path.join(path, "*.log"))
        files.sort(key=lambda file: os.path.getctime(file))

        if keep > 0:
            files = files[:-keep]

        for file in files:
            try:
                os.remove(file)
            except:
                continue

    except Exception as e:
        raise Exception("Couldn't delete older files: %s", str(e))

def get_audio_titles(path):
    '''
    Format the audio filename to a string with better presentation
    '''
    try:
        titles = []
        files = get_audio_files(path)

        for file in files:
            parts = file.replace('.mp3', '').split('_') 
            
            autor = parts[0].replace('-', ' ').title()
            audio = parts[1].replace('-', ' ').title()
            title = autor + ': ' + audio
            titles.append(title)

        return titles

    except Exception as e:
        raise Exception("Couldn't get audio titles: %s", str(e))

def get_audio_files(path):
    '''
    Returns an array with the audio file names avaiable
    '''
    return [file for file in os.listdir(path) if file.endswith('.mp3')]