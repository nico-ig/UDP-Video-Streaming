'''
Functions to interact with ALSA
'''

import os
import ctypes
import subprocess

logger = None
alsa_log_file = './logs/alsa/'

class error_handler_t(ctypes.Structure):
    '''
    Define the structure representing the snd_lib_error_handler_t struct
    '''
    _fields_ = [
        ("file", ctypes.c_char_p),
        ("line", ctypes.c_int),
        ("function", ctypes.c_char_p),
        ("err", ctypes.c_int),
        ("fmt", ctypes.c_char_p)
    ]

def set_error_handler(caller_logger):
    '''
    Redirect the error messages from ALSA
    '''
    try:
        global logger
        logger = caller_logger

        if not os.path.exists(alsa_log_file):
            os.system(f'touch {alsa_log_file}')

        ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p)
        c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

        alsa_lib = get_alsa_lib()
        alsa_lib.snd_lib_error_set_handler(c_error_handler)

        logger.debug(f'ALSA error function changed')

    except Exception as e:
        logger.error(f'Error setting alsa error handler: {str(e)}')

def py_error_handler(filename, line, function, err, fmt):
    '''
    Writes ALSA errors to log file
    '''
    try:
        logger.error(f'Error {err} supressed')

    except:
        pass

def get_alsa_lib():
    '''
    Gets the path to ALSA shared library
    '''
    try:
        command = "find / -name libasound.so 2>/dev/null"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        alsa_paths = result.stdout.splitlines()
        if len(alsa_paths) < 1:
            raise FileNotFoundError('Alsa library not found')

        return ctypes.CDLL(alsa_paths[0])

    except Exception as e:
        logger.error("Error getting alsa library file: %s", str(e))
        raise FileNotFoundError("Couldn't get alsa library file")
