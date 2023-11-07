'''
 Auxiliar functions for the project
'''

import os
import glob
import threading
from datetime import datetime

def start_thread(callback, daemon=False):
    thread = threading.Thread(target=callback)
    thread.daemon = daemon
    thread.start()

    return thread

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
    files = glob.glob(os.path.join(path, "*.log"))
    files.sort(key=lambda file: os.path.getctime(file))

    if keep > 0:
        files = files[:-keep]

    for file in files:
        try:
            os.remove(file)
        except:
            continue

def get_audio_titles(path):
    '''
    Format the audio filename to a string with better presentation
    '''
    titles = []
    files = get_audio_files(path)

    for file in files:
        parts = file.replace('.mp3', '').split('_') 
        
        autor = parts[0].replace('-', ' ').title()
        audio = parts[1].replace('-', ' ').title()
        title = autor + ': ' + audio
        titles.append(title)

    return titles

def get_audio_files(path):
    '''
    Returns an array with the audio file names avaiable
    '''
    return [file for file in os.listdir(path) if file.endswith('.mp3')]